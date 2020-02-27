from neomodel import (
    StringProperty,
    StructuredNode,
    RelationshipFrom,
    Relationship
)

from .serializer import NodeSerializer

class Entity(StructuredNode, NodeSerializer):
    name                     = StringProperty()
    sourceID                 = StringProperty()
    status                   = StringProperty()
    node_id                  = StringProperty(index = True)

    # Relationships
    articles                 = RelationshipFrom('.article.Article', 'ARTICLE_OF')
    species           = RelationshipFrom('.species.Species', 'SPECIES_OF')
    entities                 = Relationship('.entity.Entity', None)

    @property
    def serialize(self):
        return {
            'node_properties': {
                'name': self.name,
                'sourceID': self.sourceID,
                'status': self.status,
                'node_id': self.node_id,
            },
        }


    @property
    def serialize_connections(self):
        return [
            {
                'nodes_type': 'Species',
                'nodes_related': self.serialize_relationships(self.species.all()),
            },
            {
                'nodes_type': 'Article',
                'nodes_related': self.serialize_relationships(self.articles.all()),
            },
            {
                'nodes_type': 'Entity',
                'nodes_related': self.serialize_relationships(self.entities.all())
            },
        ]
