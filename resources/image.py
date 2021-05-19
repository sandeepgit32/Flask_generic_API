import os
import traceback
from flask_restful import Resource
from flask import send_from_directory, request
from werkzeug.utils import secure_filename
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)

from libs import image_helper
from libs.strings import gettext


class ImageUpload(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        """
        This endpoint is used to upload an image file. It uses the
        JWT to retrieve user information and save the image in the user's folder.
        If a file with the same name exists in the user's folder, name conflicts
        will be automatically resolved by appending a underscore and a smallest
        unused integer. (eg. filename.png to filename_1.png).
        """
        # check if the post request has the file part
        if 'image' not in request.files:
            return {"message": gettext("no_image_selected")}, 400
        file = request.files['image']

        current_user = get_jwt_identity()
        folder = f"uploads/images/{current_user}"
        # Create directory if it does not exist
        if not os.path.exists(folder):
            os.makedirs(folder)

        if image_helper.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(folder, filename))
            return {"message": gettext("image_uploaded").format(filename)}, 201
        else:  # forbidden file type
            extension = image_helper.get_extension(data["image"])
            return {"message": gettext("image_illegal_extension").format(extension)}, 400


class Image(Resource):
    @classmethod
    @jwt_required()
    def get(cls, basefilename: str):
        """
        This endpoint returns the requested image if exists. It will use JWT to
        retrieve user information and look for the image inside the user's folder.
        """
        current_user = get_jwt_identity()
        folder = f"uploads/images/{current_user}"
        if not os.path.exists(folder):
            os.makedirs(folder)
        # check if basefilename is URL secure
        if not image_helper.is_basefilename_safe(basefilename):
            return {"message": gettext("image_illegal_file_name").format(basefilename)}, 400
        
        # try to send the requested file to the user with status code 200
        filename = image_helper.find_image_any_format(folder, basefilename)
        if filename:
            return send_from_directory(folder, filename)
        else:
            return {"message": gettext("image_not_found").format(basefilename)}, 404


    @classmethod
    @jwt_required()
    def delete(cls, filename: str):
        """
        This endpoint is used to delete the requested image under the user's folder.
        It uses the JWT to retrieve user information.
        """
        current_user = get_jwt_identity()
        folder = f"uploads/images/{current_user}"
        if not os.path.exists(folder):
            os.makedirs(folder)
        # check if basefilename is URL secure
        if not image_helper.is_basefilename_safe(basefilename):
            return {"message": gettext("image_illegal_file_name").format(basefilename)}, 400

        try:
            os.remove(image_helper.get_path(folder, filename))
            return {"message": gettext("image_deleted").format(filename)}, 200
        except FileNotFoundError:
            return {"message": gettext("image_not_found").format(filename)}, 404
        except:
            traceback.print_exc()
            return {"message": gettext("image_delete_failed")}, 500
