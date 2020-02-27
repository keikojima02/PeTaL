"""
 Defines the node representing articles in Neo4j
"""

# Articles have organisms that are mentioned by Genus Species syntax

from neomodel import (StructuredNode, StringProperty,
                      RelationshipTo, Relationship)

from .serializer import NodeSerializer

"""
Declares article properties
"""
class Article(StructuredNode, NodeSerializer):
    __abstract_node__ = True
    __label__ = "Article"

    summary = StringProperty()
    images = StringProperty()
    references = StringProperty()
    links = StringProperty()
    title = StringProperty()
    content = StringProperty()
    uuid = StringProperty()
    # node_id = StringProperty(index = True)

    # Relationships
    article = Relationship(".article.Article", None)
    species = RelationshipTo(".species.Species", "MENTIONS_IN_ARTICLE")

    @property
    def serialize(self):
        return {
            "node_properties": {
                "summary": self.summary,
                "images": self.images,
                "references": self.references,
                "links": self.links,
                "title": self.title,
                "content": self.content,
                "uuid": self.uuid,
                # 'node_id': self.node_id,
            },
        }

    @property
    def serialize_connections(self):
        return [
            {
                "nodes_type": "Species",
                "nodes_related": self.serialize_relationships(self.species.all()),
            },
        ]

class WikipediaArticle(Article):
    __label__ = "WikipediaArticle"
    pass