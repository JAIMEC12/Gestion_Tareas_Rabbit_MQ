import json
import pika
import time

def connect_rabbitmq():
    for i in range(20):
        try:
            print(f"[WORKER] Intentando conectar a RabbitMQ (intento {i+1})...", flush=True)
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            print("[WORKER] Conectado a RabbitMQ", flush=True)
            return connection
        except Exception as e:
            print(f"[WORKER] Error al conectar: {e}", flush=True)
            time.sleep(3)
    raise Exception("No se pudo conectar a RabbitMQ")

def callback(ch, method, properties, body):
    task = json.loads(body)
    print(f"[WORKER] Recibido: {task}", flush=True)
    print(f"[WORKER] Procesando tarea '{task['task']}' del productor {task['producer']}...", flush=True)
    time.sleep(3)
    print(f"[WORKER] Tarea {task['id']} completada", flush=True)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    print("[WORKER] Iniciando...", flush=True)
    connection = connect_rabbitmq()
    channel = connection.channel()
    channel.queue_declare(queue="IoT_Tasks", durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="IoT_Tasks", on_message_callback=callback)

    print("[WORKER] Esperando tareas...", flush=True)
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("[WORKER] Detenido manualmente", flush=True)


if __name__ == "__main__":
    print("=== WORKER ARRANCANDO ===", flush=True)
    main()
    