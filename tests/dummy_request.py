# **************************************************************************************************
# Copyright: © MagicMirror.ai, 6 June 2017
# Author: Nuel Ezenwere
# Description: Computer Vision Engineer at MagicMirror.ai
# **************************************************************************************************
# 
import os
import cv2


class DummyRequest(object):

    file_path1 = os.path.dirname(__file__)+'/file_storage/trash/round/white/round_kupton4.jpg'
    file_path2 = os.path.dirname(__file__)+'/file_storage/trash/round/white/round_dlovato0.jpg'
    selfie = cv2.imread(file_path2)
    hair_model = cv2.imread(file_path1)
    files = {'selfie': selfie, 'hair_model': hair_model}
    form = {'username': 'Jessica', 'uploader': 'dlovato'}


class DummySignUp(object):

    file_path1 = os.path.dirname(__file__)+'/file_storage/trash/heart/white/jessica_livingston.jpg'
    selfie = cv2.imread(file_path1)  # this should be in bytes format.
    files = {'selfie': selfie}
    form = {'username': 'Jessica', 'password': 'jessy101', 'gender': 'female'}


class DummyUploadHairstyle(object):
    file_path1 = os.path.dirname(__file__)+'/file_storage/trash/heart/white/heart_cpablo0.jpg'
    selfie = cv2.imread(file_path1)  # this should be in bytes format.
    files = {'selfie': selfie}
    form = {'username': 'Jessica', 'category': 'weavon', 'gender': 'female', "style": 'starwars'}


class DummyIncrement_rScore(object):
    form = {'username': 'Jessica', 'hair_model_id': "59bd1861e978f32187864c34"}


class DummyStreamFeed(object):
    form = {'username': 'Jessica', 'category': 'All', 'style': 'All', 'index': 'All', 'N': 50, 'start': -1}
