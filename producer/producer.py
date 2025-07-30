#Dependencias
import json #Libreria para el manejo de mensajes en formato JSON
import pika #Libreria para el uso de la cola de mensajes RabbitMQ
import time #Libreria para realizar delays


#Funcion para conectar el producer con el RabbitMQ
def connect_rabbitmq():
    #Realiza 20 intentos
    for i in range(20):
        try:
            print(f"[PRODUCER] Intentando conectar a RabbitMQ (intento {i+1})...", flush=True)
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq')) #Crea la conexion con el RabbitMQ
            # Si la conexión es exitosa, retornar el objeto connection
            return connection
                #Si hubo un error, imprime un mensaje en consola indicando que hubo un error al conectar en conjunto con el detalle error que hubo
        except Exception as e:
            print(f"[PRODUCER] Error al conectar:{e}. Reintentando nuevamente",flush=True)
            time.sleep(3) # Inicializa un delay de 3 segundos al programa
    #Si dentro de los 20 intentos no hubo ningun exito de comunicacion, envia error de Conexion Fallida
    raise Exception("[PRODUCER] Conexion Fallida")

#Funcion Principal del productor 
def main():
    connection = connect_rabbitmq() # Establece la comunicacion con RabbitMQ
    channel = connection.channel() # Crea un canal de comunicacion dentro de la conexion
    channel.queue_declare(queue="IoT_Tasks", durable=True) # Declara una cola de mensajes IoT_Tasks dentro del canal de comunicacion
    sensors = ["sensor-01","sensor-2","sensor-03"] # Lista para la simulacion de sensores
    tasks = ["Procesar Imagenes","Actualizar firmware","Analizar metricas"] # Posibles tareas que puede mandar cada sensor
    # Bucle para mandar de manera constante tareas
    num_task = 0 
    while True:
            #Va a enviar de cada sensor una tarea diferent
            for i in range(3):
                # Crea un diccionario de datos que va a contener los datos de la tarea
                num_task+=1 # Indica que numero de tarea es
                task = {
                'id' : num_task, # ID de la tarea
                'task': tasks[i], # Tarea
                'producer': sensors[i] # Sensor que la mando a la cola de mensajes
                }
                #Publica mensajes dentro de la cola
                channel.basic_publish(exchange='', # Usa un exchange directo
                          routing_key='IoT_Tasks', # Nombre de la cola destino
                          body=json.dumps(task), # Transforma el diccionario de datos a formato Json
                          properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent)) # Indicar que los mensajes sean persitentes
                time.sleep(5)
                # Espera despues de cada 5 segundo para mandar el otro mensaje
                print(task,flush=True)


if __name__ == '__main__':
    main()
    