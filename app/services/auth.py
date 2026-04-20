import os
from app.pages.userProfile import UserProfile

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