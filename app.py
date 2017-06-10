# ********************************** | Malicha ai | Father, Ai scientist: Nuel.Ezenwere *****************************************************
#                                                    6 June 2017

from database import Database
from Enigma import Enigma
from hairSwap import *
from post import Post
from flask import Flask, render_template, Blueprint
import json
from sync_test import query
import jsonify

__author__ = 'nuelsian'

# Blueprint("main page", __name__, template_folder="templates")

app = Flask(__name__)


# app.config.from_object('config')


@app.route('/cognify/')
def malicha_brain():
    """

    :return:
    """
    json_requests = query()
    return Post(json_requests).get_post() 


@app.route('/') # www.malicha-ai.herokuapp.com/')
def welcome_page():
    """

    :return:
    """
    return render_template("base.html")

if __name__ == '__main__':
    app.run()
