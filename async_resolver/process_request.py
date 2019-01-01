#!/usr/bin/env python
import pika
import hashlib
import sys

def string_generator():
    str = list("")
    while True:
        length = len(str)
        for i in reversed(range(-1,length)):
            if (i == -1):
                str = list("a") + str
                yield str
                break
            if (str[i] != 'z'):
                str[i] = chr(ord(str[i]) + 1)
                yield str
                break
            elif (str[i] == 'z'):
                str[i] = 'a'

while True:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        break
    except:
        continue

channel = connection.channel()
channel.queue_declare(queue='hash_requests')
def callback(ch, method, properties, hash_prefix):
    hash_prefix = hash_prefix.decode()
    print("Got request: " + hash_prefix)
    sys.stdout.flush()
    for i in string_generator():
        s = ''.join(i)
        m = hashlib.sha256()
        m.update(s.encode())
        h = m.hexdigest()
        if (h[0:len(hash_prefix)] == hash_prefix):
            print("Found text: " + s)
            sys.stdout.flush()
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
            channel = connection.channel()
            channel.queue_declare(queue='hash_results')
            channel.basic_publish(exchange='', routing_key='hash_results', body=h + " " + s)
            connection.close()
            return

channel.basic_consume(callback,
                      queue='hash_requests',
                      no_ack=True)
channel.start_consuming()
