import re
import pika

from django.http import HttpResponse
from django.shortcuts import render
import hashlib
from django.views.decorators.csrf import csrf_exempt
from www_server.utils import string_generator
from django.db import connections

def string_hash_searcher(request):
    return render(request,'a/string_hash_searcher.html')

@csrf_exempt
def brute_force_hash_sync(request):
    hash_prefix = request.GET['prefix']
    
    # pattern = re.compile("^[1-9a-f]+[0-9a-f]*$")
    if ( not re.match(r"^[1-9a-f]+[0-9a-f]*$",hash_prefix) ):
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
    
    # pattern = re.compile("^[1-9a-f]+[0-9a-f]*$")
    if ( not re.match(r"^[0-9a-f]+$",hash_prefix) ):
        return render(request,'a/brute_force_hash_error.html')


    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='hash_requests')
    channel.basic_publish(exchange='', routing_key='hash_requests', body=hash_prefix)
    connection.close()

    return string_hash_searcher(request)

@csrf_exempt
def hash_query(request):
    hash_value = request.POST['hash_value']
    if hash_value < 'l':
        db = 'rainbow1'
    else:
        db = 'rainbow2'
    with connections[db].cursor() as cursor:
        cursor.execute("SELECT text FROM rainbow WHERE hash = %s", [hash_value]);
        row = cursor.fetchone()
        if row is None:
            row = ''
        else:
            row = row[0]
        return render(request,'a/query.html', {'result' : row})


