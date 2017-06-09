from database import Database
from Enigma import Enigma
from Newlook import NewLook
import json


class Post(object):
    selfie = None
    newlook = None
    hairdetail = None

    def __init__(self, user_request):
        """

        """
        self.user_request = user_request

    def get_post(self):
        """
        :param self:
        :return: string, an encoded string stream containing the newlook of the user.
        """
        user_request = self.user_request

        selfie, hairstyle_name, category = Enigma().extractRequest(user_request)

        # [{'newlook': image_array, 'name':_____, 'cost':______', ,...}]
        post_dict = NewLook().getNewlook(selfie, hairstyle_name, category)[0]

        image_encoding = Enigma.encodeInput("newlook.jpg")
        post_dict['newlook'] = str(image_encoding)

        # {'newlook': image_array, 'name': _____, 'cost': ______', ,...}

        # save selfie, newlook to Malicha_db(mongodb instance)

        # Database.insert(collection='datasets', data={'user': 'sudo', 'newlook': newlook_, 'selfie': selfie_})

        return self.to_json(post_dict)

    @staticmethod
    def to_json(post_dict):
        return json.dumps(post_dict)
