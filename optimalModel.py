from database import Database
from faceComplexion import FaceComplexion, display
from Enigma import Enigma
from hairSwap import FaceSwap
import cv2
import numpy as np

__author__ = 'Ezenwere.Nuel'


class OptimalModel(object):
    def __init__(self, selfie, hairstyle_name):
        """

        :param selfie: numpy array representation of an image.
        :param hairstyle_name: hairstyle : eg. weavon_blue3
        """
        self.selfie = selfie.copy()
        self.hairstyle_name = hairstyle_name

    def getOptimalModel(self):
        """
        :return: _id of optimal hair model.
        """

        complexion_instance = FaceComplexion(self.selfie.copy())

        # 3 entry tuple e.g (128, 128, 128)
        facecolor = complexion_instance.complexion()
        hairstyle = self.hairstyle_name.split('_')[0]
        # iterable mongodb hairstyle cursor eg. weavon collection :  {'name': str(hairstyle_name):hairstyle_name, "image_encoding": image_encoding,.. }
        Database.initialize()
        hairstyle_docs = Database.from_hairstyles_get(collection=hairstyle, query={})
        dict_ = {}
        count = 0
        for hairstyle_dict in hairstyle_docs:
            image_encoding = hairstyle_dict["image_encoding"]
            shape = hairstyle_dict["shape"]

            # ******* computational expensive section **************
            hair_model = Enigma.decodeInput(image_encoding, shape)
            # ******************************************************

            model_id = hairstyle_dict["_id"]
            color_code = FaceComplexion(hair_model).complexion()

            similarity = complexion_instance.euclidean_distance(facecolor, color_code)
            dict_[model_id] = similarity
            count += 1

        # model_id corresponding with the optimal hair model.
        optimal_hairmodel = FaceComplexion.min_contrast(dict_)

        return optimal_hairmodel
