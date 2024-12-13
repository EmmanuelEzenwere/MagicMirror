from database.database import Database
from app.pages.userProfile import UserProfile
from PIL import Image
from operator import itemgetter

__author__ = 'Ezenwere.Nuel'


class HairstyleFeed(object):

    default_relevancyScore = 1  # this value was hard coded into the user profile file. There should be a better way of ensuring consistency.

    def __init__(self, user_name, hairstyle_category='All', style='All', index='All'):
        """

        :param user_name:
        :param hairstyle_category:
        """
        self.hairstyle_category = hairstyle_category
        self.style = style
        self.index = index
        self.user_name = user_name
        self.user_profile = UserProfile(user_name).profile()

    def stream(self, N=1, start=-1):
        """
        :param N: Number of hairstyle images to be streamed to the user's hairstyle feed. By default we stream one image.
        :param start: integer, starting  hair model id, if start is -1 then we start from the most recent hair model.
        :return: bytes list sorted hairstyle images.
        """
        # fetching hair model paths from the hairstyle db.
        Database.initialize()
        not_specified = 'All'

        if self.hairstyle_category is not_specified:
            if self.style is not_specified:
                if self.index is not_specified:
                    # find all hair models
                    query = {}
                else:
                    # you've specified just the index.
                    query = {'index': self.index}

            elif self.index is not_specified:
                # you've specified just the style.
                query = {'style': self.style}

            else:
                # you've specified just the style and index.
                query = {'style': self.style, 'index': self.index}

        elif self.style is not_specified:
            if self.index is not_specified:
                # you've specified just the category.
                query = {'category': self.hairstyle_category}
            else:
                # you've specified just category and index.
                query = {'category': self.hairstyle_category, 'index': self.index}

        elif self.index is not_specified:
            # you've specified just a category and style.
            query = {'category': self.hairstyle_category, 'style': self.style}

        else:
            # you've specified a category, style and index.
            query = {'category': self.hairstyle_category, 'style': self.style, 'index': self.index}

        if start == -1:
            Database.find('hairstyles', query)  # this should be a cursor, first N. or
            img_cursor = Database.find('hairstyles', query).limit(N)  # this should be a cursor, first N after the first "start".
        else:
            img_cursor = Database.find('hairstyles', query).skip(start).limit(N)  # this should be a cursor, first N after the first "start".
        profiles_list = []
        for hairstyle_profile in img_cursor:
            profiles_list.append(hairstyle_profile)

        feed = self.sort(profiles_list)

        return feed

    @staticmethod
    def sort(dict_list):
        """
        sorts the hairstyles in a given hairstyle collection based on their relevancy score (rScore)
        This implies that only users can influence a sort of the hairstyle feed for a particular category of hairstyles.
        :param: stream_dict: This is a dictionary containing all the file paths to hair models as keys and their corresponding rScore as a value.
        :return:
        """
        hair_model_list = []
        sorted_profile_list = sorted(dict_list, key=itemgetter('relevancy_score'))
        # print("sorted_profile_list:", sorted_profile_list)
        for hairstyle_profile in sorted_profile_list:
            hair_model_path = hairstyle_profile['storage_location']
            hair_model_bytes = Image.open(hair_model_path)
            hair_model_list.append(hair_model_bytes)

        return hair_model_list
