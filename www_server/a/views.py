import re
import pika

from django.http import HttpResponse
from django.shortcuts import render
import hashlib
from django.views.decorators.csrf import csrf_exempt
from www_server.utils import string_generator
from django.db import connections

from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'elastic', 'port': 9200}])

HASH_PREFIX_FORMAT = r"^[0-9a-f]+$"

def string_hash_searcher(request):
    return render(request,'a/string_hash_searcher.html')

@csrf_exempt
def brute_force_hash_sync(request):
    hash_prefix = request.GET['prefix']
    
    if ( not re.match(HASH_PREFIX_FORMAT,hash_prefix) ):
        return render(request,'a/brute_force_hash_error.html')

    for i in string_generator():
        s = ''.join(i)
        m = hashlib.sha256()
        m.update(s.encode())
        h = m.hexdigest()
        if (h[0:len(hash_prefix)] == hash_prefix):
            return render(request, 'a/brute_force_hash.html', {'hash_prefix': hash_prefix, 'word': s, 'hash' : h})
    return HttpResponse("Something went wrong")

@csrf_exempt
def brute_force_hash_async(request):
    hash_prefix = request.POST['prefix']
    
    if ( not re.match(HASH_PREFIX_FORMAT, hash_prefix)):
        return render(request,'a/brute_force_hash_error.html')


    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='hash_requests')
    channel.basic_publish(exchange='', routing_key='hash_requests', body=hash_prefix)
    connection.close()

    return string_hash_searcher(request)

@csrf_exempt
def hash_query(request):
    hash_value = request.POST['hash_value'] + '%'
    if hash_value < 'l':
        db = 'rainbow1'
    else:
        db = 'rainbow2'
    with connections[db].cursor() as cursor:
        cursor.execute("SELECT text FROM rainbow WHERE hash LIKE %s", [hash_value]);
        row = cursor.fetchone()
        if row is None:
            row = ''
        else:
            row = row[0]
        return render(request,'a/query.html', {'result' : row})

@csrf_exempt
def elastic(request):
    return render(request,'a/elastic.html', {'result' : []})

@csrf_exempt
def elastic_lookup(request):
    e1 = {}
    for i in range(6):
        if request.POST['sv' + str(i) + 'name']:
            e1[request.POST['sv' + str(i) + 'name']] = request.POST['sv' + str(i) + 'value']
    res = es.search(index='data',body={'query':{'match':e1}})
    r = []
    for re in res['hits']['hits']:
        n = re['_source']['name']
        del re['_source']['name']
        u = (n, re['_source'])
        r.append(u)
    return render(request,'a/elastic.html', {'result' : r})

@csrf_exempt
def elastic_add(request):
    e1 = {'name' : request.POST['ename']}
    for i in range(6):
        if request.POST['v' + str(i) + 'name']:
            e1[request.POST['v' + str(i) + 'name']] = request.POST['v' + str(i) + 'value']
    es.index(index='data',doc_type='data',body=e1)
    return elastic(request)
