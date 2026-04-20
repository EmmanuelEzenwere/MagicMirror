import os
import cv2
import numpy as np
from datetime import datetime
from app.pages.hairstyleFeed import HairstyleFeed
from app.pages.userProfile import UserProfile
from computer_vision.hairSwap import FaceSwap
from app.pages.relevancyScore import RelevancyScore



def upload_hairstyle(request_obj):
    """
    """
    if 'selfie' not in request_obj.files and 'gender' not in request_obj.form and 'category' not in request_obj.form and 'style' not in request_obj.form:
        return "failed status.HTTP_400_BAD_REQUEST"

    # selfie is assumed to be of type bytes
    selfie = request_obj.files['selfie']
    username = request_obj.form['username']
    gender = request_obj.form['gender']
    category = request_obj.form['category']
    style = request_obj.form['style']

    hair_model_path = os.path.dirname(__file__) + '/file_storage/trash/temp_files/hair_model.jpg'

    # if a file is currently stored at the users_face_path delete file
    if os.path.isfile(hair_model_path):
        os.remove(hair_model_path)

    if type(selfie) == np.ndarray:
        # no need for type conversion.
        cv2.imwrite(hair_model_path, selfie)
        pass
    else:
        # selfie is of type bytes. Store at the users_face_path location.
        selfie.save(hair_model_path)

    UserProfile(username).upload_hairstyle(hair_model_path, gender, category, style)

    return "saved"


def perform_swap(request_obj):
    """
    :param request_obj: Dictionary containing selfie & hair_model images as bytes.
    :return: bytes, swapped hairstyle image of the user.
    """
    # ****************************** Possible Security Layer *************************************
    # to ensure that the user accessing the hairswap feature has permission/ in the user data base
    # using an API key will be preferred, also match against username and email address.
    if 'username' not in request_obj.form and 'uploader' not in request_obj.form and 'selfie' not in request_obj.files and 'hair_model' not in request_obj.files:
        return "failed status.HTTP_400_BAD_REQUEST"
    # ********************************************************************************************

    # clean up operation
    # selfie storage
    # new hairstyle storage.

    uploader = request_obj.form['uploader']
    username = request_obj.form['username']
    save_dir = os.path.dirname(__file__) + '/file_storage/trash/hairswaps/'
    index = int(count(save_dir)/3) + 1
    hair_model_path = save_dir + str(index) + '_' + str(uploader) + '.jpg'
    selfie_path = save_dir + str(index) + '_' + str(username) + '.jpg'
    swap_path = save_dir + str(index) + '_' + str(uploader) + "-->" + str(username) + '.jpg'
    selfie = request_obj.files['selfie']
    hair_model = request_obj.files['hair_model']

    # Extract Selfie as openCV array
    if type(selfie) == np.ndarray:
        pass
    else:
        if os.path.isfile(selfie_path):
            os.remove(selfie_path)
        selfie.save(selfie_path)
        selfie = cv2.imread(selfie_path)

    # Extract hair_model as open.CV. array
    if type(hair_model) == np.ndarray:
        pass
    else:
        if os.path.isfile(hair_model_path):
            os.remove(hair_model_path)
        hair_model.save(hair_model_path)
        hair_model = cv2.imread(hair_model_path)

    # perform swap.
    new_look = FaceSwap(hair_model, selfie).swap()
    if os.path.isfile(swap_path):
        os.remove(swap_path)
    cv2.imwrite(swap_path, new_look)

    return swap_path


def increment_rScore(request_obj):
    """
    :param request_obj: a request object containing 'style', 'username', 'category' & 'index'
    :return string: status indicating 'success' or 'failure'.
    """
    if 'hair_model_id' not in request_obj.form and 'username' not in request_obj.form:
        return "failed status.HTTP_400_BAD_REQUEST"

    username = request_obj.form['username']
    hair_model_id = request_obj.form['hair_model_id']

    return RelevancyScore(username).update(hair_model_id)


def stream_feed(request_obj):
    if 'username' not in request_obj.form and 'N' not in request_obj.form and 'start' not in request_obj.form and 'category' not in request_obj.form and 'style' not in request_obj.form and 'index' not in request_obj.form:
        return "failed status.HTTP_400_BAD_REQUEST FORMAT"
    username = request_obj.form['username']
    category = request_obj.form['category']
    style = request_obj.form['style']
    index = request_obj.form['index']
    num_of_images = request_obj.form['N']
    start = request_obj.form['start']

    feed = HairstyleFeed(username, category, style, index).stream(num_of_images, start)

    return feed