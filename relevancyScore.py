# import os
from bson.objectid import ObjectId
from database import Database
import datetime as dt


class RelevancyScore(object):
    default_relevancyScore = 1  # modify as necessary, a modification here is effected in all usage instances, domino effect.

    def __init__(self, user_name):
        self.user_name = user_name
        # initialize hairstyle database.
        Database.initialize()

    @staticmethod
    def profile(hair_model_id):
        """
        :return profile document: type dictionary, users face shape, skin_color.
        # we could extend the user's profile to include other details in the future such as appearance rating, make up metrics, ...
        """
        profile_dict = Database.find_one('hairstyles', {'_id': ObjectId(hair_model_id)})

        return profile_dict

    @staticmethod
    def age(date1, date2):
        """

        :param date1:
        :param date2:
        :return: Total Number of seconds between
        """
        date2_min = date1  # ** convert date1 to minutes
        date1_min = date2  # ** convert date2 to minutes
        age_ = date2_min - date1_min

        return age_

    def update(self, hair_model_id):
        """            
                                          | The Almighty algorithm |
        using the chronological date  and the number of likes of a hairstyle model this algorithm assigns a score to all hairstyles under a given
        category (eg. afro, ...) = a dictionary with keys as hairstyle model ids and values as relevancy score.

        - Sort the hairstyles into a list, according to their relevancy score.
        - Stream the sorted hairstyles available to the a user in a Hairstyle.feed.
        - Decides the order of uploads to ensure premium quality hairstyles are presented first. 
        - Remove terrible hairstyle uploads from the hairstyle stream. (future support)
        - Keeps users satisfied with the quality of the Hairstyle Feed.
        
        Each time a user likes a hairstyle post, it's relevancy score is updated.

        :return: Reach into hairstyle database, copy current relevancy score then increment.
        """
        hairstyle_profile = self.profile(hair_model_id)
        # get parameters to update relevancy score (rScore)
        rScore = hairstyle_profile['relevancy_score']
        # number of likes for the hair model
        likes = hairstyle_profile['likes']
        created_date = hairstyle_profile['created_date']
        current_date = dt.datetime.now()
        age_sec = (current_date - created_date).total_seconds()
        rScore += likes / age_sec
        # update relevancy score.
        hairstyle_profile['relevancy_score'] = rScore
        query = {'_id': ObjectId(hair_model_id)}
        updated_profile = hairstyle_profile
        Database.update('hairstyles', query, updated_profile)

        return "success"
