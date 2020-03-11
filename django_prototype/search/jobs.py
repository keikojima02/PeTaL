import pytz
import logging
from datetime import datetime

from celery import shared_task
from django.conf import settings
from django.core.cache import cache

from .._main.utils import generate_job
from ..petalusers.models import PetalUser
from .models import Query, KeyWord

from neomodel import DoesNotExist, db


# logger = logging.getLogger('loggly_logs')

@shared_task()
def update_search(username, query_param, keywords):
    """
       Creates a search query node then calls the task to create and
       attach keyword nodes to the search query node

       :param username:
       :param query_param:
       :param keywords:
       :return:
       """
    try:
        result, _ = db.cypher_query( "MATCH (a:PetalUser {username:'%s'}) RETURN a" % username)

        if result.one:
            result.one.pull()
            petaluser = PetalUser.inflate(result.one)
        else:
            raise update_search.retry(
                exc = DoesNotExist("That username : " '%s' "does not exist" % username),
                countdown = 3, max_retries = None)
    except IOError as exception:
        raise update_search.retry( exc = exception, countdown = 3, max_retries = None)
    try:
        query = Query.nodes.get(query = query_param)

        if petaluser.searches.is_connected(query):

            related = petaluser.relationship(query)
            related.times_searched += 1
            related.last_searched = datetime.now(pytz.utc)
            related.save()
            return True
        else:
            related = petaluser.searches.connected(query)
            related.save()
            query.searched_by.connect(petaluser)
            return True
    except (Query.DoesNotExist, DoesNotExist):
        query = Query(query = query_param)
        query.save()
        query.searched_by.connect(petaluser)
        related = petaluser.searches.connect(query)
        related.save()

        for keyword in keywords:
            keyword["query_param"] = query_param
            generated = generate_job(job_func = create_keyword, job_param = keyword)

            if isinstance(generated, Exception) is True:
                return generated
        return True
    except IOError as exception:
        raise update_search.retry(exc = exception, countdown = 3, max_retries = None)
    except Exception as exception:
        raise update_search.retry(exc = exception, countdown=3, max_retries = None)

@shared_task()
def create_keyword(search_text, relevance, query_param):
    """
    This function takes

    :param search_text:
    :param relevance:
    :param query_param:
    :return:
    """
    try:
        try:
            query = Query.nodes.get(query = query_param)
        except (Query.DoesNotExist, DoesNotExist) as exception:
            raise create_keyword.retry(exc = exception, countdown = 3, max_retries = None)
        try:
            keyword = KeyWord.nodes.get(keyword = search_text)
            related = query.keywords.connect(keyword)
            related.relevance = relevance
            related.save()
            keyword.queries.connect(query)
            query.save()
            keyword.save()

            return True
        except (KeyWord.DoesNotExist, DoesNotExist):
            keyword = KeyWord(keyword = search_text).save()

        except IOError as exception:
            raise create_keyword.retry(exc = exception, countdown = 3, max_entries = None)

@shared_task()
def update_object(object_uuid, label = None, data = None, index = "search-base"):
    from ..petalusers.serializers import

































