#                     Database Architecture | Architect: Nuel Ezenwere

import os

import cv2

from faceShape import getFaceShape
from skinComplexion import SkinComplexion

__author__ = 'Ezenwere.Nuel'


def ensure_dir(img_dir):
    directory = os.path.dirname(img_dir)
    if not os.path.isdir(directory):
        os.makedirs(directory)


def loop_file(folder_path):
    """
    :param folder_path: path to folder containing hair models to be put into the hairstyle
    :return: insert new hairstyles to Malicha db
    """
    count = 0

    source = folder_path

    for root, dirs, filenames in os.walk(source):
        for filename in filenames:
            full_path = os.path.join(source, filename)

            hair_model = cv2.imread(full_path)
            skin_complexion = SkinComplexion(full_path).identify()
            face_shape = getFaceShape(full_path)
            img_dir = os.path.dirname(
                __file__) + '/file_storage/trash/' + face_shape + '/' + skin_complexion + '/' + filename
            ensure_dir(img_dir)
            cv2.imwrite(img_dir, hair_model)
            os.remove(full_path)
            count += 1
            print("No " + str(count) + " : " + filename + "," + face_shape)

    return 'All hair_models added...'

# # Database - Maintenance: local uploads to database.
# files_path = "/home/higgsfield/PycharmProjects/MagicMirror.ai/file_storage/trash"
# print(loop_file(files_path))
