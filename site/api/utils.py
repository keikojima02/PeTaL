from uuid import uuid1

from django.conf import settings
from neomodel import db

def generate_job(job_func, job_param, countdown=0, job_id=None):
    if job_id is None:
        job_id = str(uuid1())
    try:
        return job_func.apply_async(kwargs=job_param, countdown=countdown,
                                    job_id=job_id)
    except (IOError, Exception) as exception:
        raise exception

def collect_request_data(context, expedite_param=None, expand_param=None):
    try:
        request = context['request']
        try:
            expand = request.query_params.get('expand', 'false').lower()
            expedite = request.query_params.get('expedite', "false").lower()
            relations = request.query_params.get(
                'relations', 'primaryKey').lower()
            html = request.query_params.get('html', 'false').lower()
            expand_array = request.query_params.get('expand_attrs', [])
            if html == 'true':
                expand = 'true'
        except AttributeError:
            try:
                expand = request.GET.get('expand', 'false').lower()
                expedite = request.GET.get('expedite', 'false').lower()
                relations = request.GET.get('relations', 'primaryKey').lower()
            except AttributeError:
                expand = 'false'
                expedite = 'false',
                relations = 'primaryKey'
                request = None
            expand_array = []
    except KeyError:
        expand = 'false'
        expedite = 'false'
        relations = "primaryKey"
        request = None
        expand_array = []

    if expedite_param is not None:
        expedite = 'true'
    if expand_param:
        expand = 'true'

    return request, expand, expand_array, relations, expedite
