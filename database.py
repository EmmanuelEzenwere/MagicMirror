#         MagicMirror.ai.       Database Architecture | Architect: Nuel Ezenwere


import pymongo
import os

__author__ = 'Ezenwere.Nuel'


class Database(object):
    URI = "mongodb://NuelEzenwere:Nuel11235813@ds143734.mlab.com:43734/magicmirror"  # release version
    # URI = "mongodb://127.0.0.1:27017"  # local test version
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        # Database.DATABASE = client['MagicMirror']  # local test version
        Database.DATABASE = client['magicmirror']  # release version

        # ************************* database methods ********************************

    @staticmethod
    def insert(collection, data):
        """

        :param collection: database collection to be added to.
        :param data: dictionary object to be added to the collection.
        :return: performs the action.
        For an upgrade this should be extended include a possible errors.
        """
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        """
        :param collection: database collection to be added to.
        :param query: dictionary objects to be obtained from the specified collection.
        :return: performs the action. .
        """
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        """
        :param collection: database collection to be added to.
        :param query: dictionary object to be obtained from the specified collection.
        :return: performs the action.
        """
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection, query, updated_profile):
        """
        :param collection: database collection to be added to.
        :param query: dictionary object to be obtained from the specified collection.
        :param updated_profile: updated document for storage, of type: dictionary
        :return: performs the action.
        """
        return Database.DATABASE[collection].update(query, updated_profile)
