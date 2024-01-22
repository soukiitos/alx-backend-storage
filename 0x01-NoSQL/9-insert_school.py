#!/usr/bin/env python3
'''Insert a new document in a collection based on kwargs'''
import pymongo


def insert_school(mongo_collection, **kwargs):
    '''Define insert_school'''
    return mongo_collection.insert_one(kwargs).inserted_id
