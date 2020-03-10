#!/usr/bin/python
import spacy, re
import pandas as pd
from nltk.corpus import wordnet as wn
import json
import collections
import getopt
import codecs
import struct
import timeit
import pickle
import math
import nltk
import sys
import os
import re

from neo4j import GraphDatabase, basic_auth
neoDriver = GraphDatabase.driver("bolt://139.88.179.199:7687", auth=basic_auth("neo4j", "testing"))


# Process
# Count word occurrences in articles and build a lexicon or list of english words.
# The index will map from a word in the lexicon to an article
# that has that word in its hit list at a high frequency

class Indexer():


def create_index():
    index = {}
    f_crawled = open("crawled.txt", "r")

    for line in f_crawled.readlines():
        line = line.replace('\n', '')
        url = line
        line = line[7:]
        line = line.replace('/', '-')
        line = line + '.txt'
        f_file = open(line, "r")
        content = f_file.read()

        words = content.split()
        for word in words:
            add(index, word, url)

    return index


def load_dict(path):
    with open(path) as st:
        data = json.load(st)  # open the json containing the thesaurus

    terms = {}

    try:
        for tert in data["tertiary"]:
            terms[tert["engineer"]] = tert["biologist"]
    except KeyError as e:
        print(e.args[0], " is not in the thesaurs")
        raise

    return terms


def add(index, keyword, url):
    if keyword in index:
        if url not in index[keyword]:
            index[keyword].append(url)
    else:
        index[keyword] = [url]


def search(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None


new_index = create_index()
print(new_index)
