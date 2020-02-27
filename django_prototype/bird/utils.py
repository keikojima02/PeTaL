from .endpoints import ORGANISM_NAMES, TITLES

# from .models import (Entity, Species, Article)
from .models import (Species, Article)

""" 
key-value map for each model. 
"""
# the key is the model class name and the value will be the model class itself

MODEL_ENTITIES = {
    # 'Entity': Entity,
    "Species": Species,
    "Article": Article
}

# Query Functions

"""
Helper function that receives a model class and some
filter parameters and returns the corresponding nodeset
"""

# NodeSet object represents a set of nodes matching common query parameters or filters
# Node object is an instance of one of our models.
# node_type is a user defined object that instantiates a node model
# we want to check the search_text against the node property

# def filter_nodes(node_type, search_text, organism_name, title):
def filter_nodes(node_type, organism_name, title):
    node_set = node_type.nodes

    # if node_type.__name__ == "Entity":
    #     node_set.filter(entity__icontains = search_text)
    # else:
    #     node_set.filter(name__icontains = search_text)

    # if node_type.__name__ == "Species":
    #     node_set.filter(organism_name__icontains = search_text)
    #
    # if node_type.__name__ == "Article":
    #     node_set.filter(title__icontains = search_text)

    node_set.filter(organism_name__icontains = organism_name)
    node_set.filter(title__icontains = title)

    return node_set


""" 
Returns a subset of nodes filtered by filter_nodes 
"""
def retrieve_nodes(retrieve_info):
    # retrieve the nodes, read their properties and relationships

    node_type = retrieve_info["node_type"]
    # search_phrase = retrieve_info["name"]

    organism_name = retrieve_info["organism_name"]
    title = retrieve_info["title"]

    limit = retrieve_info["limit"]
    start = ((retrieve_info["page"] - 1) * limit)
    end = start + limit

    node_set = filter_nodes(
        MODEL_ENTITIES[node_type], organism_name, title
        # MODEL_ENTITIES[node_type], search_phrase, organism_name, title
    )

    retrieved_nodes = node_set[start:end]

    return [node.serialize for node in retrieved_nodes]

def retrieve_node_details(node_info):
    node_type = node_info["node_type"]
    # node_id = node_info["node_id"]
    # node_id = node_info[id]
    node = MODEL_ENTITIES[node_type].nodes.get(node_id = id)
    # node = MODEL_ENTITIES[node_type].nodes.get(node_id=node_id)
    node_details = node.serialize

    # Make sure to return an empty array if not connections
    node_details['node_connections'] = []
    if hasattr(node, 'serialize_connections'):
        node_details['node_connections'] = node.serialize_connections

    return node_details


def retrieve_organism_names():
    return ORGANISM_NAMES

def retrieve_titles():
    return TITLES
