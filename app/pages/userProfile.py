import os
import datetime as dt
from PIL import Image
from database.database import Database


class UserProfile(object):

    def __init__(self, user_name):
        """

        :param user_name: username for the user.
        """
        self.user_name = user_name
        Database.initialize()

    def profile(self):
        """ 
        Get information on the user eg. username.
        
        user's profile to include other details in the future 
        such as appearance rating, make up metrics, ...

        Returns:
            user_profile(dict): users face shape, skin_color.
        """
        user_name = self.user_name
        user_profile = Database.find_one('users', {'users': user_name})
        return user_profile

    def add_user(self, password, gender, users_face_path):
        """
        :param users_face_path: string, full path to an image of the user's face.
        :param password: string, user's password.
        :param gender: string, sex of the user, strictly male or female.
        """

        from core.faceShape import getFaceShape
        face_shape = getFaceShape(users_face_path)
        print("face_shape:", face_shape)

        from core.skinComplexion import SkinComplexion
        skin_complexion = SkinComplexion(users_face_path).identify()

        img_dir = os.path.dirname(__file__) + '/file_storage/users/' + str(gender) + '/'
        no_of_users = self.count(img_dir) + 1

        img_path = img_dir + str(self.user_name) + '.jpg'
        profile_dict = {"user_name": self.user_name, 
                        "password": password, 
                        "gender": gender, 
                        "face_shape": face_shape, 
                        "skin_complexion": skin_complexion, 
                        'index': no_of_users, 
                        'storage_location': img_path}
        
        Database.insert('users', profile_dict)
        selfie = Image.open(users_face_path)
        selfie.save(img_path)
        status = 'user profile created and added to database'

        return status

    def sign_in(self, password):
        """

        :param password: string, user's password.
        :return status: string, authenticated, invalid or sign-in duplicate.
        """
        search_dict = Database.find_one('users', {'username': self.user_name, 
                                                  'password': password}
                                        )
        if len(search_dict) == 1:
            status = 'authenticated'
        elif len(search_dict) == 0:
            status = 'invalid_user'
        else:
            status = 'authenticated, but more that one users share this username & password'

        return status

    @staticmethod
    def ensure_dir(img_dir):
        directory = os.path.dirname(img_dir)
        if not os.path.isdir(directory):
            os.makedirs(directory)

    def construct_path(self, category, style):
        """_summary_

        Args:
            category (_type_): _description_
            style (_type_): _description_

        Returns:
            _type_: _description_
        """
        user_profile = self.profile()
        gender = user_profile['gender']
        face_shape = user_profile['face_shape']
        skin_complexion = user_profile['skin_complexion']
        attributes = face_shape + '/' + skin_complexion + '/' + gender + '/' + category + '/' + style
        img_dir = os.path.dirname(__file__)+'/file_storage/hairstyles/' + attributes

        return img_dir

    def count(self, img_dir):
        """
        :return:int, number of hairstyles in a given brands directory.
        loops over the content of img_dir and establishes a count.
        """
        count = 0
        self.ensure_dir(img_dir)
        for f in os.listdir(img_dir):
            if os.path.isfile(os.path.join(img_dir, f)):
                count += 1
        return count

    @staticmethod
    def retrieve(category, style, index):
        """Goes into the MagicMirror.ai hairstyle database and retrieves a specified hairstyle.
        :param index: this is the index of hairstyle models to be retrieved
        :param category:
        :param style:
        :return: image bytes representation of the given hairstyle

        Args:
            category (_type_): _description_
            style (_type_): _description_
            index (_type_): _description_

        Returns:
            image: image bytes representation of the given hairstyle
        """
        # save hairstyle to database.
        hairstyle_profile = Database.find_one('hairstyles', {'category': category, 'style': style, 'index': index})
        image_path = hairstyle_profile['storage_location']
        try:
            image = Image.open(image_path)
            return image
        except FileNotFoundError:
            return 'requested hairstyle model does not exist'

    def upload_hairstyle(self, hair_model_path, gender, category, style):
        """Saves a newly uploaded hairstyle image to the hairstyle database 
        considering the user's profile. and hairstyle details.

        Args:
            hair_model_path (_type_): _description_
            gender (_type_): _description_
            category (_type_): _description_
            style (_type_): _description_

        Returns:
            _type_: _description_
        """

        from core.faceShape import getFaceShape
        #  hair_model_path is expected to be the full path to the uploaded hair model.
        face_shape = getFaceShape(hair_model_path)

        from core.skinComplexion import SkinComplexion
        skin_complexion = SkinComplexion(hair_model_path).identify()
        hair_attributes = gender + '/' + category + '/' + style + '/' + face_shape + '/' + skin_complexion +'/'
        img_dir = os.path.dirname(
            __file__) + '/file_storage/hairstyles/' + hair_attributes

        self.ensure_dir(img_dir)
        no_of_hairmodels = self.count(img_dir) + 1
        image_path = img_dir + str(no_of_hairmodels) + '.jpg'
        hair_model = Image.open(hair_model_path)
        hair_model.save(image_path)
        created_date = dt.datetime.now()
        default_relevancy_score = 1

        profile_dict = {"category": category, 
                        'style': style, 
                        'index': no_of_hairmodels,
                        "creator": self.user_name, 
                        "gender": gender,
                        "face_shape": face_shape, 
                        "skin_complexion": skin_complexion, 
                        "created_date": created_date,
                        'relevancy_score': default_relevancy_score, 
                        'likes': 1, 
                        'storage_location': image_path}

        # save hairstyle to database.
        Database.insert('hairstyles', profile_dict)

        return 'hair models created and added to database.'

# Feature Request: Dev Notes.

# What are possible information to learn from a users face for Drea.ai personal assistant?
# What Cosmetic products could the user need. This will be used for product recommendation.
