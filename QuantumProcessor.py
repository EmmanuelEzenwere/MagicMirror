import os
import cv2
import numpy as np
from datetime import datetime
from hairstyleFeed import HairstyleFeed
from userProfile import UserProfile
from hairSwap import FaceSwap
from relevancyScore import RelevancyScore


def ensure_dir(img_dir):
    directory = os.path.dirname(img_dir)
    if not os.path.isdir(directory):
        os.makedirs(directory)


def count(img_dir):
    """
    :return:int, number of hairstyles in a given brands directory.
    loops over the content of img_dir and establishes a count.
    """
    count_ = 0
    ensure_dir(img_dir)
    for f in os.listdir(img_dir):
        if os.path.isfile(os.path.join(img_dir, f)):
            count_ += 1

    return count_


def timestamp():
    """

    :rtype: object
    :return: type = string, current date and time
    """
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return date_time


def upload_hairstyle(request_obj):
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
        selfie.save(hair_model_path)
        selfie = cv2.imread(hair_model_path)

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


def sign_up(request_obj):
    """
    Collect and store new user's username, password, profile pic & gender.
    :param request_obj: request object containing the new user's name and gender in a request form.
    :return:
    """
    if 'username' not in request_obj.form and 'gender' not in request_obj.form and 'password' not in request_obj.form and 'selfie' not in request_obj.files:
        return "failed status.HTTP_400_BAD_REQUEST FORMAT"
    username = request_obj.form['username']
    gender = request_obj.form['gender']
    password = request_obj.form['password']
    selfie = request_obj.files['selfie']

    users_face_path = os.path.dirname(__file__) + '/file_storage/trash/temp_files/profile_pic.jpg'

    # if a file is currently stored at the users_face_path delete file
    if os.path.isfile(users_face_path):
        os.remove(users_face_path)

    if type(selfie) == np.ndarray:
        # save to system folder, at the users_face_path location.
        cv2.imwrite(users_face_path, selfie)

    else:
        # save to system folder, at the users_face_path location.
        selfie.save(users_face_path)

    # create an instance of a user with name username and add details of the user.
    UserProfile(username).add_user(password, gender, users_face_path)
    # if successful then
    status = 'success '

    return status


def sign_in(request_obj):
    """
    Collect and store new user's username, password, profile pic & gender.
    :param request_obj: request object containing the new user's name and gender in a request form.
    :return:
    """
    if 'username' not in request_obj.form and 'password' not in request_obj.form:
        return "failed status.HTTP_400_BAD_REQUEST FORMAT"
    username = request_obj.form['username']
    password = request_obj.form['password']
    # create an instance of a user with name username and add details of the user.
    UserProfile(username).sign_in(password)
    # if successful then
    status = 'success '

    return status
