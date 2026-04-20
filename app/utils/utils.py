"""
"""
import os
from datetime import datetime


def ensure_dir(img_dir):
    """_summary_

    Args:
        img_dir (_type_): _description_
    """
    directory = os.path.dirname(img_dir)
    if not os.path.isdir(directory):
        os.makedirs(directory)


def count(img_dir):
    """
    :return:int, number of hairstyles in a given brands directory.
    loops over the content of img_dir and establishes a count.
    """
    count_ = 0
    ensure_dir(img_dir)
    for f in os.listdir(img_dir):
        if os.path.isfile(os.path.join(img_dir, f)):
            count_ += 1

    return count_


def timestamp():
    """

    :rtype: object
    :return: type = string, current date and time
    """
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return date_time