from Enigma import Enigma
from hairSwap import *
import json


def query():
    """
    dummy malicha api query

    :return: json string containing output for processed request.
    """
    image_input = cv2.imread("w1.jpg")
    shape = str(image_input.shape)
    image_encoding = str(Enigma.encodeInput(image_input))
    hairstyle_name = "weavon_black_3"
    category = "tryModel"
    user_input = {"image_encoding": image_encoding, "shape": shape, "hairstyle_name": hairstyle_name,
                  "category": category}

    return json.dumps(user_input)
