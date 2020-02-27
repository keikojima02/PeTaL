# bird/organism.py
# Damn King Phillip Came Over From Great Spain
# Domain, Kingdom, Phylum, Class, Order, Family, Genus, Species
from neomodel import (StructuredNode, StringProperty, AliasProperty,
                      UniqueIdProperty, RelationshipTo, Relationship)

from .serializer import NodeSerializer

class Species(StructuredNode, NodeSerializer):

    # names should not be duplicated, so we define it as required
    # name = StringProperty(unique_index = True, required = True)
    # CRITICAL - properties have to be identical to the corresponding properties in neo4j

    Order = StringProperty()
    # organism_order = AliasProperty(to = "Order")

    CatalogSource = StringProperty()
    # catalogue_source = AliasProperty(to = "CatalogSource")

    Phylum = StringProperty()
    # organism_phylum = AliasProperty(to = "Phylum")

    Genus = StringProperty()
    # organism_genus = AliasProperty(to = "Genus")

    Family = StringProperty()
    # organism_family = AliasProperty(to = "Family")

    Class = StringProperty()
    # organism_class = AliasProperty(to = "Class")

    Name = StringProperty(required = True)
    # organism_name = AliasProperty(to = "Name")

    # node_id = StringProperty(index = True)

    # Relationships
    species = Relationship(".species.Species", None)
    articles = RelationshipTo(".article.Article", "MENTIONS_SPECIES")

    @property
    def serialize(self):
        return {
            "node_properties": {
                "order": self.Order,
                "catalogue_source": self.CatalogSource,
                "phylum": self.Phylum,
                "genus": self.Genus,
                "family": self.Family,
                "class": self.Class,
                "name": self.Name,
                # "node_id": self.node_id,
            },
        }

    @property
    def serialize_connections(self):
        return [
            {
                "nodes_type": "Articles",
                "nodes_related": self.serialize_relationships(self.articles.all()),
            },
        ]
