from database import Database
from Enigma import Enigma
from hairSwap import FaceSwap
from highestScores import HighestScores
from faceComplexion import FaceComplexion
from optimalModel import OptimalModel
import cv2


class NewLook(object):
    # collection to be used.
    collections = "hairModels"

    def __init__(self):
        """

        """

    @staticmethod
    def get_hairdetail():
        """

        :return: string
        """
        return None

    @staticmethod
    def model_from_mongo():
        """
        :return: a list of dictionaries of all hair styles and their corresponding id in the hairStyles collection
        """
        # collect all entries in all collections in the hairStyles collection in the Malicha mongo database.
        # list of all dictionaries containing each and every hair detail. eg [{'id':_____,'hairstyle':_______,'shape':_____},...]

        return [{"id": dict_entry["_id"], "hairstyle": dict_entry["hairstyle"], "shape": dict_entry["shape"]} for
                dict_entry in Database.find(collection='hairstyles', query={})]

    def recommendation(self, selfie):
        """
        :param   selfie: numpy_array representation of the user's selfie.
        :return: dictionary, top choice for hairstyles and their details.
                [{'name':_____, 'cost':______', 'newlook': image_array,...}...]
        """
        # list of all dictionaries containing each and every hair detail. eg [{'id':_____,'image_encoding':_______,'shape':_____},...]
        collections = self.model_from_mongo()

        # [{'id':_____, 'newlook': numpy_array},...]
        recommended = HighestScores(selfie).gethighestScored(collections)

        # [{'hair_name':_____, 'newlook': numpy_array, 'cost': _____, ...}...]
        return Enigma.restructureRecommendation(recommended)

    @staticmethod
    def tryModel(selfie, hairstyle_name):
        """
        :param   selfie: numpy_array representation of the user's selfie.
        :param   hairstyle_name: type str, name of hair style. eg. weavon_black
        :return: [{'newlook': image_array, 'name':_____, 'cost':______', ,...}]
        """
        # hairstyle_name, format= name_color_index eg. weavon_blue

        # model_id corresponding to the optimal hairmodel
        model_id = OptimalModel(selfie, hairstyle_name).getOptimalModel()
        # hairstyle eg. weavon
        hairstyle = hairstyle_name.split('_')[0]
        hairstyle_dict = list(Database.from_hairstyles_get(collection=hairstyle, query={"_id": model_id}))[0]
        hair_model = hairstyle_dict["image_encoding"]
        shape = hairstyle_dict["shape"]

        # ************** computational expensive section **********
        hairmodel = Enigma.decodeInput(hair_model, shape)
        # *********************************************************

        # dictionary containing details of the specific hairstyle.
        hair_details = hairstyle_dict["details"]

        newlook = FaceSwap(hairmodel, selfie).swap()
        newlook = FaceComplexion(newlook).reshapen()
        cv2.imwrite("newlook.jpg", newlook.copy())

        return [{**{"newlook": newlook}, **hair_details}]

    def getNewlook(self, selfie, hairstyle_name, category):
        """
        :param selfie: numpy array representation of user's image.
        :param hairstyle_name: string, eg weavon_black
        :param category: TryModels or Recommender
        :return: list of dictionaries containing the user's new look . . .
        """
        if category == "Recommender" or category == "recommendation" or category == "recommend":
            # one or more high scoring images with hair details
            return self.recommendation(selfie)

        # essentially different transcribed  variations of the concept of "trying model"
        elif category == "TryModel" or category == "tryModel" or "ry" in category:
            return self.tryModel(selfie, hairstyle_name)

        else:
            return "error in obtaining category of use"
