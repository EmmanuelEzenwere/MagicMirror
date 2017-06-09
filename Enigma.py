
import base64
import json
import numpy as np
from database import Database


class Enigma(object):
    def __init__(self):
        """

        """

    def extractRequest(self, json_string):
        """
        :param json_string: api call containing dictionary of encoded selfie,...
                          '{"hairstyle_name":_________, "category":_________, "selfie":__________, "shape":_________}'
        :return: selfie, hairstyle_name, category : array, dictionary & string.
        """
        # api data format : encodedImage+Shape+Category.
        # slice api data to get base64 encoded image string (encoding)

        request_dict = json.loads(json_string)

        # b64 string encoding of user's image.
        encoding = request_dict["image_encoding"]

        # slice api data to get image shape encoded string (encoding)
        image_shape = request_dict["shape"]

        # unique id = hairstyle_color+index eg. weavon_black3
        hairstyle_name = request_dict["hairstyle_name"]

        # recommend or trymodels
        category = request_dict["category"]

        # numpy array representation of user's image.
        selfie = self.decodeInput(encoding, image_shape)

        return selfie, hairstyle_name, category

    @staticmethod
    def encodeInput(image_input):
        """"
        """
        if type(image_input) == str and image_input.split('.')[-1] in ['jpg', 'png', 'jpeg']:
            with open(image_input, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
        else:
            encoded_string = base64.b64encode(image_input)
        return encoded_string

    @staticmethod
    def decodeInput(encoded_image, image_shape):
        """

        :param encoded_image: b64 encoded image
        :param image_shape:
        :return:
        """
        if type(image_shape) == str:
            image_shape = eval(image_shape)
        if type(encoded_image) == str:
            encoded_image = eval(encoded_image)

        decoded_image = base64.b64decode(encoded_image)

        decoded_image = np.array(list(decoded_image), dtype=np.uint8)
        decoded_image = np.reshape(decoded_image, image_shape)

        return decoded_image

    @staticmethod
    def stringStream(input_dict):
        """

        :param input_dict:
        :return:
        """
        # format encoded_image+image_shape+hair_
        return input_dict

    @staticmethod
    def restructureRecommendation(recommendation):
        """
        :param recommendation: list of dictionaries containing recommended hair styles and an id to locate their details
                [{'hairstyle_name':_____, 'newlook': numpy_array},...]

        :return:
               [{'hair_name':_____, 'newlook': numpy_array, 'cost': _____, ...}...]

        """
        # initializations
        recommendation_list = []
        Database.initialize()

        for entry in recommendation:
            newlook = entry["newlook"]

            # hairstyle_name follows the convention *hairstyle_color_index*

            hairstyle_name = entry["hairstyle_name"]
            hairstyle = hairstyle_name.split('_')[0]

            # find hair details in the hairstyles collection of the Malicha mongodb database
            hairstyle_dict = Database.from_hairstyles_getOne(collection=hairstyle, query={"name": hairstyle_name})

            # details in a entry in any hairstyle collection is as follows 'details': {'cost':_____, 'texture':_______, 'color':_______}
            details = hairstyle_dict['details']

            # combine the details dictionary and the newlook dictionary to get a recommended set
            recommendation_list.append({**details, **{'newlook': newlook}})

        return recommendation_list
