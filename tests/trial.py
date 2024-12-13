from app.utils import utils
import tests.dummy_request as dummy_request


def quick_tests(request_type):
    if request_type == 'sign_up':
        signup_request = dummy_request.DummySignUp
        print(utils.sign_up(signup_request))

    elif request_type == 'perform_swap':
        perform_swap_request = dummy_request.DummyRequest
        print(utils.perform_swap(perform_swap_request))

    elif request_type == 'upload':
        upload_request = dummy_request.DummyUploadHairstyle
        print(utils.upload_hairstyle(upload_request))

    elif request_type == 'increment_rScore':
        increment_rscore_request = dummy_request.DummyIncrement_rScore
        print(utils.increment_rScore(increment_rscore_request))

    elif request_type == 'stream_feed':
        feed_request = dummy_request.DummyStreamFeed
        print(utils.stream_feed(feed_request))

# quick_tests('sign_up')
