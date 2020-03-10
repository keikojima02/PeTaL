import pytz
from datetime import datetime
from uuid import uuid1
from django.conf import settings

from neomodel import (StructuredNode, IntegerProperty, Relationship,
                      StructuredRel, FloatProperty, RelationshipTo,
                      BooleanProperty, DateTimeProperty, StringProperty,
                      UniqueIdProperty, db)

from neo4j import GraphDatabase, basic_auth
neoDriver = GraphDatabase.driver("bolt://139.88.179.199:7687", auth=basic_auth("neo4j", "testing"))


def get_time():
    return datetime.now(pytz.utc)


def get_long_time():
    return int(datetime.now(pytz.utc).strftime("%s")) * 1000


class PetalObject(StructuredNode):
    object_uuid = UniqueIdProperty(default=uuid1, unique_index=True)
    created = DateTimeProperty(default=get_time)
    timestamp = IntegerProperty(default=get_long_time)

    def get_labels(self):
        query = 'MATCH n WHERE id(n)=%d RETURN DISTINCT labels(n)' % self._id
        result, col = db.cypher_query(query)
        return result[0][0]

    def get_child_label(self):
        return list(set(self.get_labels()) - set(settings.REMOVE_CLASSES))[0]


def test_get_lables():
    from django_prototype.bird.models import Article

    PetalObject.get_labels(Article)
