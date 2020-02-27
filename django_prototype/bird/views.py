from neomodel import db
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response

from neo4j import GraphDatabase, basic_auth
from .utils import (retrieve_organism_names, retrieve_titles)


def birdhome(request):
    context = dict(query='')
    return render(request, 'bird/bird_e2b.html', context)

def birdresults(request):
    query = request.GET.get('q')
    # neo_client = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "life"))
    neo_client = GraphDatabase.driver("bolt://139.88.179.199:7667", auth=basic_auth("neo4j", "testing"))
    with neo_client.session() as session:
        result = session.run('MATCH (a:Article) WHERE a.abstract CONTAINS \'{test}\' RETURN a'.format(test=query))
    articles = [article['a'] for article in result.records()]
    # context = dict(query=result, papers=[dict(url='URL', relevancy=0.0, title='An example', abstract='Lorem ipsum imet ')])
    context = dict(papers=articles)
    return render(request, 'bird_results.html', context)


class GetSpecies(APIView):
    def get(self, request):
        species = retrieve_organism_names()
        data = {
            'response': {
                'status': '200',
                'data': species,
            },
        }
        return Response(data)


class GetArticleTitles(APIView):
    def get(self, request):
        titles = retrieve_titles()
        data = {
            'response': {
                'status': '200',
                'data': titles,
            },
        }
        return Response(data)
