#                     Database Architecture | Architect: Nuel Ezenwere
#
# Malicha {db} -|-hairstyles {collection}   : hairstyles_braids : {"name": str(name), "image_encoding":str(image_encoding), "color_code":color_code, "cost": str(cost)}
#                                           : hairstyles_weavon : {"name": str(name), "image_encoding":str(image_encoding), "color_code":color_code, "cost": str(cost)}
#                                           : hairstyles_dreadlocks : {"name": str(name), "image_encoding":str(image_encoding), "color_code":color_code, "cost": str(cost)}
#                                           : hairstyles_curly : {"name": str(name), "image_encoding":str(image_encoding), "color_code":color_code, "cost": str(cost)}


#               |-complexions               : {"name": str(name), "colorcode": str(colorcode)}
#
#
#

import pymongo

__author__ = 'Ezenwere.Nuel'


class Database(object):
    # URI = "mongodb://Nuelsian:#Nuel11235831@ds111922.mlab.com:11922/malicha"
    URI = "mongodb://127.0.0.1:27017"

    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['Malicha']

        # ************************* database methods ********************************

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].findOne(query)

    # ****************************************************************************

    # ************************ hairstyles collections method *********************
    @staticmethod
    def from_hairstyles_get(collection, query):
        collection_ = "hairstyles_" + collection
        return Database.DATABASE[collection_].find(query)

    @staticmethod
    def from_hairstyles_getOne(collection, query):
        return Database.DATABASE["hairstyles_" + collection].findOne(query)

    @staticmethod
    def to_hairstyles_insert(collection, data):
        Database.DATABASE["hairstyles_" + collection].insert(data)

    # ************************ face complexions method ***************************
    @staticmethod
    def from_complexions_get(collection, query):
        return Database.DATABASE["complexions"][collection].find(query)

    @staticmethod
    def from_complexions_getOne(collection, query):
        return Database.DATABASE["complexions"][collection].find(query)

    @staticmethod
    def to_complexions_insert(collection, data):
        Database.DATABASE["complexions"][collection].insert(data)

    # *****************************************************************************

    # ***********************  datasets method ************************************
    @staticmethod
    def to_datasets_insert(collection, data):
        Database.DATABASE["datasets"][collection].insert(data)

    @staticmethod
    def from_datasets_get(collection, query):
        return Database.DATABASE["datasets"][collection].find(query)

    @staticmethod
    def from_datasets_getOne(collection, query):
        return Database.DATABASE["datasets"][collection].findOne(query)

    @staticmethod
    def view_database():
        return Database.DATABASE.getCollectionNames()

    # ******************************************************************************

    @staticmethod
    def mongo_bot(action, collection, query):
        # Future: project mongo-bot
        # Error correcting bot and task assignment bot.
        if action == 'find':
            pass
        elif action == 'insert':
            pass
        elif action == '':
            pass
        else:
            pass
