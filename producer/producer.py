import json, time
import pika


def connect_rabbitmq():
    for i in range(20):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            return connection
        except:
            print("Reconexion con RABBITMQ")
            time.sleep(3)
    raise Exception("Conexion Fallida")


def main():
    connection = connect_rabbitmq()
    channel = connection.channel()
    channel.queue_declare(queue="IoT_Tasks", durable=True)
    sensors = ["sensor-01","sensor-2","sensor-03"]
    tasks = ["Process Images","Update firmware","Process metrics"]
    for i in range(3):
         task = {
             'id' : i+1,
             'task': tasks[i],
             'producer': sensors[i]
         }
         channel.basic_publish(exchange='',
                          routing_key='IoT_Tasks', body=json.dumps(task), 
                          properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent))
         time.sleep(5)
         print(task)
    connection.close()

if __name__ == '__main__':
    main()
