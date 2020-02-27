from neomodel import db

organism_names = db.cypher_query(
    '''MATCH (n) RETURN DISTINCT n.Name AS organism_name'''
)[0]

titles = db.cypher_query(
    '''MATCH (n) RETURN DISTINCT n.title AS title'''
)[0]

ORGANISM_NAMES = sorted(
    [organism_name[0] for organism_name in organism_names if isinstance(organism_name[0], str)]
)

TITLES = sorted(
    [title[0] for title in titles if isinstance(title[0], str)]
)
