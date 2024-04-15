import os
import json
import time
import paho.mqtt.client as mqtt
from watchdog.observers import Observer
#from watchdog.events import FileSystemEventHandler
from elasticsearch import Elasticsearch

# FUNCIONES ------------------------------------------------------------------------------------------------------------------------------

# Función para cargar la configuración desde el archivo JSON
def parse_config_file(config_file_path):
    with open(config_file_path, 'r') as config_file: # Abre el archivo en modo lectura
        config_data = json.load(config_file) # Carga el JSON en un diccionario
    return config_data # Devuelve el diccionario


# Función para publicar el archivo JSON detectado en un tema MQTT
def publish_json_file(client, topic, file_path):
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            message = json.dumps(data)
            client.publish(topic, message)
    except json.decoder.JSONDecodeError as e: # Manejar errores de JSON
        print(f"Error al cargar el archivo JSON: {e}")
    except FileNotFoundError as e: # Manejar errores de archivo no encontrado
        print(f"Error: No se pudo encontrar el archivo: {file_path}")
        

# Función para manejar la suscripción a un topic
def subscribe_to_topic(client, topic):
    subscribed = False
    while not subscribed: # Mientras no esté suscrito al tema
        try:
            # Intentar suscribirse al tema
            client.subscribe(topic)
            print(f"Subscrito al tema {topic}")
            subscribed = True
        except Exception as e:
            # Manejar cualquier excepción y esperar antes de intentar de nuevo
            print(f"No se pudo suscribir al tema {topic}. Error: {e}")
            print("Intentando nuevamente en 5 segundos...")
            time.sleep(5)


# Función para subir el mensaje a Elasticsearch
def upload_to_elasticsearch(payload):
    try:
        # Parsear el JSON recibido
        json_data = json.loads(payload)

        # Conectar a Elasticsearch
        es = Elasticsearch(hosts=["http://localhost:9200"])

        # Subir el JSON a Elasticsearch
        res = es.index(index="topology", body=json_data)
        print("Documento subido correctamente a Elasticsearch:", res)
        
    except Exception as e:
        print("Error al subir el documento a Elasticsearch:", e)
        
        
# Función de callback para manejar los mensajes recibidos
def on_message(client, userdata, message):
    print(f"Mensaje recibido en el tema '{message.topic}': {str(message.payload.decode())}")
    # Subir el mensaje a Elasticsearch
    upload_to_elasticsearch(message.payload.decode())
    

# MAIN -----------------------------------------------------------------------------------------------------------------------------------

# Parsear el archivo de configuración
config = parse_config_file("config.json")

# Configurar las variables
topology_path = config["topology_path"]
behaviour_path = config["behaviour_path"]
#mgmt_path = config["mgmt_path"]

mqtt_broker_ip = config["mqtt_broker_ip"]
mqtt_broker_port = config["mqtt_broker_port"]

mqtt_topic = "TOPOLOGY"  # Nombre del tema MQTT al que se suscribirá

# Crear un cliente MQTT
client = mqtt.Client()

# Asignar la función de callback
client.on_message = on_message

# Conectar al broker MQTT
client.connect(mqtt_broker_ip, mqtt_broker_port, 60)

# Ejecutar la función para suscribirse al tema TOPOLOGY
subscribe_to_topic(client, mqtt_topic)

# Mantener la conexión activa y procesar los mensajes entrantes
client.loop_forever()
