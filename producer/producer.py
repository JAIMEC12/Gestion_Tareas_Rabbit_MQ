import json, time
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

channel.queue_declare(queue="IoT_Tasks", durable=True)

def main():
    channel.basic_publish(exchange='',
                          routing_key='IoT_Tasks', body="Update Metrics", 
                          properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent))

    connection.close()

if __name__ == '__main__':
    main()
