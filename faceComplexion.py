# ************************************* faceComplexion class *****************************************************

# complexion categories:

import dlib
import math
import numpy as np
import cv2
from colorthief import ColorThief
import matplotlib.pyplot as plt
from imutils import face_utils
import os

__author__ = 'Ezenwere.Nuel'


class FaceComplexion(object):
    """ FaceComplexion main class  """

    def __init__(self, image):
        """
        :param image: an image(numpy array) containing a single face.
        """
        self.image = image  # define a converter function to ensure the input image is in the required format.
        # make an instance of Mongodb HairStyles database

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

    def reshapen(self):
        """

        :param self:
        :return: A resized image of the newlook
        """
        image = self.image
        face_detector = dlib.get_frontal_face_detector()

        # convert image to grey scale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscale image
        facerects = face_detector(gray, 1)
        # loop over the faces detected
        for (i, facerect) in enumerate(facerects):
            (left, top, width, height) = face_utils.rect_to_bb(facerect)
            bottom = height + top

        croppedface = image.copy()[0:bottom, 0:image.shape[1]]

        return croppedface

    @staticmethod
    def dominant_color(image):
        """
        :param image: numpy array representation of input_image
        :return: tuple, dominant color as a color code ie (R, G, B)
        """
        savepath = "image.jpg"
        cv2.imwrite(savepath, image)
        color_thief = ColorThief(savepath)

        # get the dominant color
        dominant_color = color_thief.get_color(quality=1)

        # delete the file from memory to save memory.
        os.remove('image.jpg')
        return dominant_color

    @staticmethod
    def display_color(dominant_color):
        """

        :param dominant_color:
        :return:
        """
        palette = np.zeros((100, 100, 3), dtype=np.uint8)
        display(cv2.rectangle(palette, (0, 0), (100, 100), dominant_color, -1))

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
        # get key with maximum value
        key = list(dict_.keys())[values.index(min(values))]

        return key

    def complexion(self):
        """
        :return: string(complexion id) class the user's face belongs to.
        """

        croppedface = self.face_detect()

        # RGB tuple : eg (128, 128, 128)
        facecolor = self.dominant_color(croppedface)

        return facecolor


def display(image):
    plt.show(plt.imshow(image))
    return None
