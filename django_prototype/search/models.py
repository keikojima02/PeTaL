from neo4j import GraphDatabase, basic_auth
neoDriver = GraphDatabase.driver("bolt://139.88.179.199:7687", auth=basic_auth("neo4j", "testing"))

from django_prototype._main.models import PetalObject, get_time, get_long_time

from neomodel import (StructuredNode, StringProperty, IntegerProperty,
                    FloatProperty, ArrayProperty, BooleanProperty, StructuredRel,
                    DateTimeProperty, RelationshipTo, Relationship)

class Page(StructuredNode):
    title = StringProperty()
    content = StringProperty()
    links = StringProperty()
    pagerank = FloatProperty()
    created_at = DateTimeProperty()
    last_indexed = DateTimeProperty()


class KeyWordRel(StructuredRel):
    relevance = FloatProperty(default=0)

class Index(StructuredNode)

class KeyWord(StructuredNode):
    keyword = StringProperty()
    weight = IntegerProperty(default=0)

class Query(StructuredNode):
    weight = IntegerProperty(default = 0)
    search_query = StringProperty(unique_index=True)
    times_searched = IntegerProperty(default = 1)
    last_searched = DateTimeProperty(default = get_time)
    trending = BooleanProperty(default = False)

    # relationships
    searched_by = Relationship('users.models.User', 'SEARCHED_BY')
    keywords = RelationshipTo(KeyWord, 'KEYWORDS', model = KeyWordRel)
    results = RelationshipTo(SearchResult, 'RESULT')

class Searchable(PetalObject):
    search_id = StringProperty()
    populated_es_index = BooleanProperty(default=False)
    view_count = IntegerProperty(default=0)
    summary = StringProperty()

    # relationships
    viewed_by = RelationshipTo('users.models.User', "VIEWED_BY",
                               model = Impression)
