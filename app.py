# # ********************************** | MagicMirror.ai | Ai scientist: Nuel.Ezenwere *****************************************************
# #                                                    6 June 2017
#

from flask import Flask, request, send_file
import QuantumProcessor
__author__ = 'nuelsian'

app = Flask(__name__)


@app.route('/sign_up')
def sign_up():
    """
    :return: string, success if a sign up process was successful. Otherwise, failed.
    """
    status = QuantumProcessor.sign_up(request)
    return status


@app.route('/sign_in')
def sign_in():
    """
    :return: string, success if a sign up process was successful. Otherwise, failed.
    """
    status = QuantumProcessor.sign_in(request)
    return status


@app.route('/hairswap', methods=['GET', 'POST'])
def swap_hairstyle():
    """
    :return: image:bytes , swap hairstyle of in selfie with the hairstyle image.
    """
    filename = QuantumProcessor.perform_swap(request)
    return send_file(filename)


@app.route('/upload', methods=['GET', 'POST'])
def upload_hairstyle():
    """
    :return: post an image of the user with the new hairstyle.
    """
    status = QuantumProcessor.upload_hairstyle(request)
    return status


@app.route('/feedback', methods=['GET', 'POST'])
def update_relevancyScore():
    """
    :return: whenever this end point is accessed the input hairstyle's relevancy score should be incremented.
    """
    status = QuantumProcessor.increment_rScore(request)
    return status


@app.route('/feed', methods=['GET', 'POST'])
def get_hairstylefeed():
    """
    :return: images of hairstyle models from the hairstyle feed.
    """

    feed = QuantumProcessor.stream_feed(request)
    return feed


@app.route('/test')
def test_run():
    """
    :return: image:bytes , swap hairstyle of in selfie with the hairstyle image.
    """
    from dummy_request import DummyRequest
    filename = QuantumProcessor.perform_swap(DummyRequest)
    return send_file(filename)


@app.route('/')
def welcome_page():
    """
    :return:
    """
    return "<h4>MagicMirror.ai Api, the future of fashion. Visit www.magicmirror.ai</h4>"

if __name__ == '__main__':
    app.run()
