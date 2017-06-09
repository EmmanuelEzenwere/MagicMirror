from Enigma import Enigma
from deepHair import DeepHair
from hairSwap import FaceSwap

__author__ = 'Ezenwere.Nuel'


class HighestScores(object):
    def __init__(self, selfie):
        self.selfie = selfie

    def gethighestScored(self, collections):
        """
        :param  collections: # list of all dictionaries containing each and every hair detail.
                [{'name':_____,'image_encoding':_______,'shape':_____},...]

        :return:list of dictionaries containing top scoring hair styles
                [{'name':_____, 'newlook': numpy_array},...]
        """

        # initialize variables.

        predictions = {}
        newlooks = {}

        # search implementation
        for entry in collections:
            # numpy array representation of hair model
            hairstyle_encoding = entry["image_encoding"]
            shape = entry["shape"]
            hairmodel = Enigma().decodeInput(hairstyle_encoding, shape)
            hairstyle_name = entry['name']

            newlook = FaceSwap(hairmodel, self.selfie)
            rating = DeepHair().rate_appearance(
                newlook)  # hair model and the new look are both 3 dimensional vectors, numpy arrays.
            predictions[hairstyle_name] = rating
            newlooks[hairstyle_name] = newlook

        highest_rating = max(list(predictions.values()))
        top_choice = [hairstyle_name for hairstyle_name in predictions if predictions[hairstyle_name] == highest_rating]
        recommendation = [{'name': hairstyle_name, 'newlook': newlooks[hairstyle_name]} for hairstyle_name in
                          top_choice]

        return recommendation
