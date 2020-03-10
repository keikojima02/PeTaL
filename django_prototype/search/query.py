#!/usr/bin/python
import collections
import operator
import getopt
import codecs
import struct
import timeit
import math
import nltk
import sys
import io
import re


def search(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None


def new_search(index, ranks, keyword):
    pages = search(index, keyword)

    for i in pages:
        print(i + " --> " + str(ranks[i]))

    sort(pages, ranks)

    #  sorting the results by page rank
    for i in pages:
        print(i)


def sort(pages, ranks):
    if len(pages) > 1:
        piv = ranks[pages[0]]
        i = 1
        j = 1

        for j in range(1, len(pages)):
            if ranks[pages[j]] > piv:
                pages[i], pages[j] = pages[j], pages[i]
                i += 1

        pages[i - 1], pages[0] = pages[0], pages[i - 1]

        sort(pages[1:i], ranks)
        sort(pages[i + 1:len(pages)], ranks)


def make_rankings(graph):
    d = 0.8
    loops = 10
    ranks = {}
    num_pages = len(graph)

    for page in graph:
        ranks[page] = 1.0 / num_pages
    for i in range(0, loops):
        new_rankings = {}
        for page in graph:
            new_rank = (1 - d) / num_pages
            for node in graph:
                if page in graph[node]:
                    new_rank = new_rank + d * ranks[node] / len(graph[node])
            new_rankings[page] = new_rank
        ranks = new_rankings

    return ranks


ranks = make_rankings(graph)
new_search(index, ranks, "is")
