# ********************************** | Malicha ai | Father, Ai scientist: Nuel.Ezenwere *****************************************************
#                                                    6 June 2017

from database import Database
from Enigma import Enigma
from hairSwap import *
from post import Post
from flask import Flask, render_template, Blueprint
import json
import jsonify

__author__ = 'nuelsian'

# Blueprint("main page", __name__, template_folder="templates")


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


app = Flask(__name__)


# app.config.from_object('config')


@app.route('/cognify/')
def malicha_brain():
    """

    :return:
    """
    json_requests = query()
    return Post(json_requests).get_post()  # render_template("base.html")


@app.route('/') # www.malicha-ai.herokuapp.com/')
def welcome_page():
    """

    :return:
    """
    return render_template("base.html")


# if __name__ == '__main__':
app.run(host='0.0.0.0')
