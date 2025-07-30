#Dependencias
import json #Libreria para el manejo de mensajes en formato JSON
import pika #Libreria para el uso de la cola de mensajes RabbitMQ
import time #Libreria para realizar delays

#Funcion para conectar el worker con el RabbitMQ
def connect_rabbitmq():
    for i in range(20): #Realiza 20 intentos 
        #Intenta realizar la conexion
        try:
            print(f"[WORKER] Intentando conectar a RabbitMQ (intento {i+1})...", flush=True)
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq')) #Crea la conexion con el RabbitMQ
            # Si la conexión es exitosa, retornar la el objeto que representa la conexion
            return connection 
        #Si hubo un error, imprime un mensaje en consola indicando que hubo un error al conectar en conjunto con el detalle error que hubo
        except Exception as e:
            print(f"[WORKER] Error al conectar:{e}. Reintentando nuevamente", flush=True)
            time.sleep(3) #Inicia un delay de 3 segundos
    #Si despues de los 20 intentos, levanta un error indicando que RabbitMQ no pudo conectarse
    raise Exception("[WORKER] Conexion fallida")

#Funcion la cual se va a ejecutar cuando el worker recibe un mensaje en cola
def callback(ch, method, properties, body):
    task = json.loads(body) # Carga el mensaje JSON y lo transforma en un diccionario de datos en PYTHON
    print(f"[WORKER] Recibido: {task}", flush=True) # Imprime el diccionario de datos recibido
    print(f"[WORKER] Procesando tarea '{task['task']}' del productor {task['producer']}...", flush=True)
    time.sleep(3) #Realiza un delay simulando el procesamiento de una tarea
    print(f"[WORKER] Tarea {task['id']} completada", flush=True)
    ch.basic_ack(delivery_tag=method.delivery_tag) #Envia un acknowledgment confirmando que el mensaje fue recibido y procesado

# Funcion Principal del worker
def main():
    print("[WORKER] Iniciando...", flush=True)
    connection = connect_rabbitmq() # Establece e inicializa la conexion con RabbitMQ
    channel = connection.channel() # Crea un canal de comunicacion dentro de la conexion
    channel.queue_declare(queue="IoT_Tasks", durable=True) # Declara una cola de mensajes, en este caso, IoT_Tasks e indica que los mensajes dentro de la cola sea durable 
    channel.basic_qos(prefetch_count=1) # Configuracion qos para indicar que el worker solo puede procesar un mensaje a la vez
    channel.basic_consume(queue="IoT_Tasks", on_message_callback=callback) # Indica que funcion se debe ejecutar para procesar mensajes, cuando reciba mensajes de la cola de mensajes IoT_Tasks

    print("[WORKER] Esperando tareas...", flush=True)
    try:
        #Inicia una bucle de manera indefinida para el consumo de mensajes
        channel.start_consuming()
    #Si se da una error, detiene el consumo de mensajes y la comunicacion
    except Exception as e:
        print(f"[WORKER] Detenido por {e}", flush=True)
        #Indica que debe detener el bucle, por lo tanto, el consumo de mensaje
        channel.stop_consuming()
    finally:
        #Cierra el canal de comunicacion
        channel.close()


if __name__ == "__main__":
    main()
    