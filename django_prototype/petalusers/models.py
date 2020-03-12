import pytz
from datetime import datetime

from django.conf import settings
from django.core.cache import cache
from django.templatetags.static import static

from neomodel import (StructuredNode, StringProperty, IntegerProperty,
                      DateTimeProperty, RelationshipTo,
                      StructuredRel, BooleanProperty,
                      DoesNotExist)

from neomodel import db

from .._main.models import PetalObject, RelationshipWeight
from ..search.models import Searchable, Impression


def get_current_time():
    return datetime.now(pytz.utc)


# def get_default_profile_pic():
#     return static('images/sage_coffee_grey-01.png')
#
#
# def get_default_wallpaper_pic():
#     return static('images/wallpaper_western.jpg')


class SearchCount(StructuredRel):
    times_searched = IntegerProperty(default = 1)
    last_searched = DateTimeProperty(default = lambda: datetime.now(pytz.utc))

class OauthUser(PetalObject):
    web_address = StringProperty(default=settings.WEB_ADDRESS + '/o/token/')
    access_token = StringProperty()
    expires_in = IntegerProperty()
    refresh_token = StringProperty()
    last_modified = DateTimeProperty(default=get_current_time)
    token_type = StringProperty(default="Bearer")

class PetalUser(Searchable):
    sex = StringProperty()
    # oauth_token = StringProperty()
    username = StringProperty(unique_index = True)
    first_name = StringProperty()
    last_name = StringProperty()
    middle_name = StringProperty()
    email = StringProperty(index = True)
    date_of_birth = DateTimeProperty()
    # profile_pic = StringProperty(default=get_default_profile_pic)
    is_admin = BooleanProperty(default = False)
    is_verified = BooleanProperty(default = True)
    search_index = StringProperty()
    employer = StringProperty()
    occupation = StringProperty()
    # base_index_id is the plebs id in the base search index
    base_index_id = StringProperty()
    email_verified = BooleanProperty(default=False)
    initial_verification_email_sent = BooleanProperty(default=False)

    # Relationships
    # privileges = RelationshipTo('sb_privileges.neo_models.Privilege', 'HAS',
    #                             model = ActionActiveRel)
    # actions = RelationshipTo('sb_privileges.neo_models.SBAction', 'CAN',
    #                          model = ActionActiveRel)
    # restrictions = RelationshipTo('sb_privileges.neo_models.Restriction',
    #                               'RESTRICTED_BY', model = RestrictionRel)

    # oauth = RelationshipTo("plebs.neo_models.OauthUser", "OAUTH_CLIENT")

    viewed = RelationshipTo('search.models.Searchable', "VIEWED",
                                model = Impression)

    # user_weight = RelationshipTo('PetalUser', 'WEIGHTED_USER',
    #                              model = UserWeightRelationship)
    object_weight = RelationshipTo(
        'sb_base.neo_models.SBContent', 'OBJECT_WEIGHT',
        model = RelationshipWeight)
    searches = RelationshipTo('sb_search.neo_models.SearchQuery', 'SEARCHED',
                              model = SearchCount)
    accessed_results = RelationshipTo('sb_search.neo_models.SearchResult',
                                     'ACCESSED_RESULT')
    url_content = RelationshipTo('sb_uploads.neo_models.URLContent',
                                 'URL_CONTENT')

    @classmethod
    def get(cls, username, cache_buster = False):
        profile = None
        if username is None:
            return None
        if cache_buster is False:
            profile = cache.get(username)
        if profile is None or cache_buster:
            res, _ = db.cypher_query(
                "MATCH (a:%s {username:'%s'}) RETURN a" % (
                    cls.__name__, username))
            if res.one:
                res.one.pull()
                profile = cls.inflate(res.one)
            else:
                raise DoesNotExist('Profile with username: %s '
                                   'does not exist' % username)
            cache.set(username, profile)
        return profile

    def deactivate(self):
        pass

    def get_actions(self, cache_buster = False):
        actions = cache.get("%s_actions" % self.username)
        if actions is None or cache_buster is True:
            query = 'MATCH (a:PetalUser {username: "%s"})-' \
                    '[:CAN {active: true}]->(n:`PetalAction`) ' \
                    'RETURN n.resource' % self.username
            result, column = db.cypher_query(query)
            actions = [row[0] for row in result]
            cache.set("%s_actions" % self.username, actions)
        return actions

    # def get_privileges(self, cache_buster = False):
    #     privileges = cache.get("%s_privileges" % self.username)
    #     if privileges is None or cache_buster is True:
    #         query = 'MATCH (a:PetalUser {username: "%s"})-' \
    #                 '[:HAS {active: true}]->(n:`Privilege`) ' \
    #                 'RETURN n.name' % self.username
    #         result, column = db.cypher_query(query)
    #         privileges = [row[0] for row in result]
    #         cache.set("%s_privileges" % self.username, privileges)
    #     return privileges
    #
    # def get_full_name(self):
    #     return str(self.first_name) + " " + str(self.last_name)