#!/usr/bin/env python
import sqlite3
import sys
import pika

while True:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        break
    except:
        continue

channel = connection.channel()
channel.queue_declare(queue='hash_results')
def callback(ch, method, properties, hash_prefix):
    a = hash_prefix.split()
    h = a[0].decode()
    s = a[1].decode()
    print("About to insert text: " + s)
    sys.stdout.flush()
    if h < 'l':
        conn = sqlite3.connect('rainbow1.sqlite3')
    else:
        conn = sqlite3.connect('rainbow2.sqlite3')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO rainbow VALUES('" + h + "', '" + s + "')")
    conn.commit();
    conn.close();
    print("Inserted text: " + s)
    sys.stdout.flush()
    return

channel.basic_consume(callback,
                      queue='hash_results',
                      no_ack=True)
channel.start_consuming()
