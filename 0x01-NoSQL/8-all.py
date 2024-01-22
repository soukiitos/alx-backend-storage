#!/usr/bin/env python3
'''List all documents in a collection'''
import pymongo


def list_all(mongo_collection):
    '''Define list_all'''
    if not mongo_collection:
        return []
    return list(mongo_collection.find())
