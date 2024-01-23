#!/usr/bin/env python3
'''Provide some stats about Nginx logs stored in MongoDB'''
from pymongo import MongoClient


def get_stat():
    '''Define get_stat'''
    client = MongoClient('mongodb://127.0.0.1:27017')
    get_logs = client.logs.nginx
    tot_logs = get_logs.count_document({})
    get_meth = get_logs.count_document({"method": "GET"})
    post_meth = get_logs.count_document({"method": "POST"})
    put_meth = get_logs.count_document({"method": "PUT"})
    patch_meth = get_logs.count_document({"method": "PATCH"})
    delete_meth = get_logs.count_document({"method": "DELETE"})
    path_meth = get_logs.count_document({"method": "GET", "path": "/status"})
    print(f"{tot_logs} logs")
    print("Methods:")
    print(f"\tmethod GET: {get_meth}")
    print(f"\tmethod POST: {post_meth}")
    print(f"\tmethod PUT: {put_meth}")
    print(f"\tmethod PATCH: {patch_meth}")
    print(f"\tmethod DELETE: {delete_meth}")
    print(f"{path_meth} status check")


if __name__ == "__main__":
    get_stat()
