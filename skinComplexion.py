# ************************************* faceComplexion class *****************************************************

# complexion categories:

import math
import os

import cv2
import dlib
import matplotlib.pyplot as plt
import numpy as np
from colorthief import ColorThief
# from PIL import Image
from imutils import face_utils

__author__ = 'Ezenwere.Nuel'


class SkinComplexion(object):
    """ FaceComplexion main class  """

    def __init__(self, image, file_type='path'):
        """
        :param image: image_path (string) or an image(numpy array) containing a single face.
        :param file_type: string. if an image(numpy array) is used then supply 'image' otherwise ignore and image_path is assumed.

        """
        if file_type == 'image':
            self.image = image.copy()
        else:
            self.image = cv2.imread(image)

    def face_detect(self):
        """
        return: image: (numpy array) with the face cropped from the image.
        """
        image = self.image
        face_detector = dlib.get_frontal_face_detector()

        # convert image to grey scale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscale image
        face_rects = face_detector(gray, 1)
        # loop over the faces detected
        for (i, face_rect) in enumerate(face_rects):
            (left, top, width, height) = face_utils.rect_to_bb(face_rect)
            cv2.rectangle(image, (left, top), (left + width, top + height), (0, 255, 0), 2)
            right = width + left
            bottom = height + top

            cropped_face = image.copy()[top:bottom, left:right]

        return cropped_face

    @staticmethod
    def dominant_color(image):
        """
        :param image: numpy array representation of input_image
        :return: tuple, dominant color as a color code ie (R, G, B)
        """
        savepath = os.path.dirname(__file__)
        savepath = savepath.replace('/src', '') + '/file_storage/trash/image.jpg'
        cv2.imwrite(savepath, image)
        color_thief = ColorThief(savepath)

        # get the dominant color
        dominant_color = color_thief.get_color(quality=1)

        # delete the file from memory to save memory.
        os.remove(savepath)

        return dominant_color

    @staticmethod
    def display_color(dominant_color):
        """

        :param dominant_color:
        :return:
        """
        palette = np.zeros((100, 100, 3), dtype=np.uint8)

        image = cv2.rectangle(palette, (0, 0), (100, 100), dominant_color, -1)
        # import matplotlib.pyplot as plt
        # plt.show(plt.imshow(image))

        return image

    @staticmethod
    def euclidean_distance(point1, point2):

        vector1 = np.matrix([point1]).T
        vector2 = np.matrix([point2]).T
        dv = vector1 - vector2

        distance = math.sqrt(dv.T * dv)

        return distance

    @staticmethod
    def min_contrast(dict_):
        """
        :param dict_: With keys as strings and keys as numbers.
                      {model_id: contrast, model_id: contrast, ...}
        :return: model_id of type Object id, The key of the dictionary that corresponds to the minimum contrast.
        """
        values = list(dict_.values())
        # get key with minimum contrast value.
        key = list(dict_.keys())[values.index(min(values))]

        return key

    def complexion(self):
        """
        :return: string(complexion id) class the user's face belongs to.
        """

        cropped_face = self.face_detect()

        # RGB tuple : eg (128, 128, 128)
        face_color = self.dominant_color(cropped_face)

        return face_color

    def identify(self):
        """
        :return: string(complexion id) class the user's face belongs to.
        """
        face_color = self.complexion()
        color_vector = np.matrix([face_color])
        complexion = math.sqrt(color_vector * color_vector.T)

        # As an upgrade consider conducting a research of an approximate number of distinct face shapes & using Convolutional Neural Networks
        # Experimental values.
        chocolate_threshold = 215
        white_threshold = 245

        if complexion >= white_threshold:
            return 'white'

        elif complexion >= chocolate_threshold:
            return 'chocolate'

        else:
            return 'dark'

    @staticmethod
    def complexion_threshold():
        """

        :return:
        """
        complexion_list = []
        directory = os.path.dirname(__file__)
        database = 'file_storage'
        search_directory = directory + '/' + database + '/datasets/'

        count = 1
        for file_name in os.listdir(search_directory):
            full_path = os.path.join(search_directory, file_name)
            hair_model = cv2.imread(full_path)
            face_color = SkinComplexion(hair_model).complexion()
            color_vector = np.matrix([face_color])
            complexion_value = math.sqrt(color_vector * color_vector.T)
            complexion_list.append(complexion_value)

            # print('complexion value '+str(count)+' :', complexion_value)
            count += 1

        complexion_matrix = np.matrix(complexion_list)
        mean = np.mean(complexion_matrix)  # using complexion list
        diff_matrix = complexion_matrix - mean
        absolute_deviation = np.mean(abs(diff_matrix))

        return "absolute deviation: " + str(int(absolute_deviation)) + ", mean: " + str(int(mean))


def plot_images(image, Caption1):
    # plt.close()

    plt.rcParams['text.usetex'] = False
    plt.rcParams['font.size'] = 10
    plt.rcParams['font.family'] = 'Dejavu Sans'

    fig, ax = plt.subplots(1, 1)
    ax.imshow(image)
    xlabel = Caption1
    ax.set_xlabel(xlabel)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()
