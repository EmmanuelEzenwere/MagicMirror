#                     Database Architecture | Architect: Nuel Ezenwere
#
# Malicha {db} -|-hairstyles {collection}   : braids : {"name": str(name), "image_encoding":str(image_encoding), "color_code":color_code, "cost": str(cost)}
#                                           : weavon : {"name": str(name), "image_encoding":str(image_encoding), "color_code":color_code, "cost": str(cost)}
#                                           : dreadlocks : {"name": str(name), "image_encoding":str(image_encoding), "color_code":color_code, "cost": str(cost)}
#                                           : curly : {"name": str(name), "image_encoding":str(image_encoding), "color_code":color_code, "cost": str(cost)}


#               |-complexions               : {"name": str(name), "colorcode": str(colorcode)}
#
#

import os
import cv2
from common.database import Database
from Enigma import Enigma

__author__ = 'Ezenwere.Nuel'


def loop_file(folder_path):
    """
    :param folder_path: path to folder containing hair models to be put into the hairstyle
    :return: insert new hairstyles to Malicha db
    """
    count = 0

    source = folder_path

    for root, dirs, filenames in os.walk(source):
        for file in filenames:
            fullpath = os.path.join(source, file)

            # numpy representation of the hair model image.
            hairmodel = cv2.imread(fullpath, cv2.IMREAD_COLOR)  # hair model
            quantized_path = fullpath.split('/')

            # weavon_black1
            hairstyle_name = quantized_path[len(quantized_path) - 1].split('.')[0]

            # eg. weavon
            hairstyle = hairstyle_name.split('_')[0]
            shape = str(hairmodel.shape)
            image_encoding = Enigma().encodeInput(hairmodel)
            details = {'color': hairstyle_name.split('_')[-1][0:-1], 'cost': 0}

            pseudo_json = {'name': hairstyle_name, 'image_encoding': image_encoding, 'shape': shape, 'details': details}

            Database.initialize()
            Database.to_hairstyles_insert(collection=hairstyle, data=pseudo_json)
            count += 1

    return 'hair_models added...'

# Database - Maintenance: local uploads to database.
# files_path = "/home/higgs-field/Desktop/MalichaDB/hairstyles/weavons"
# print(loop_file(files_path))
