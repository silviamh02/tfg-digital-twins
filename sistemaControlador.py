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
        print(f"Error al cargar el archivo JSON: {e}.\n")
    except FileNotFoundError as e: # Manejar errores de archivo no encontrado
        print(f"Error: No se pudo encontrar el archivo: {file_path}.\n")
        

# Función para manejar la suscripción a un topic
def subscribe_to_topic(client, topic):
    subscribed = False
    while not subscribed: # Mientras no esté suscrito al tema
        try:
            # Intentar suscribirse al tema
            client.subscribe(topic)
            print(f"Subscrito al topic {topic}.\n")
            subscribed = True
        except Exception as e:
            # Manejar cualquier excepción y esperar antes de intentar de nuevo
            print(f"No se pudo suscribir al tema {topic}. Error: {e}.\n")
            print("Intentando nuevamente en 5 segundos...\n")
            time.sleep(5)


# Función para subir el mensaje a Elasticsearch
def upload_topology_to_elasticsearch(payload):
    try:
        # Parsear el JSON recibido
        json_data = json.loads(payload)

        # Conectar a Elasticsearch
        es = Elasticsearch(hosts=["http://localhost:9200"])

        # Subir el JSON a Elasticsearch
        res = es.index(index="topology", body=json_data)
        print("Documento subido correctamente a Elasticsearch:", res, "\n")
        
    except Exception as e:
        print("Error al subir el documento a Elasticsearch:", e, "\n")
        

# Función para subir el mensaje a Elasticsearch
def upload_behaviour_to_elasticsearch(payload):
    try:
        # Parsear el JSON recibido
        json_data = json.loads(payload)

        # Conectar a Elasticsearch
        es = Elasticsearch(hosts=["http://localhost:9200"])

        # Subir el JSON a Elasticsearch
        res = es.index(index="behaviour", body=json_data)
        print("Documento subido correctamente a Elasticsearch:", res, "\n")
        
    except Exception as e:
        print("Error al subir el documento a Elasticsearch:", e, "\n")
        
# # Función para subir el mensaje a Elasticsearch
# def upload_behaviour_to_elasticsearch(payload):
#     try:
#         # Parsear el JSON recibido
#         json_data = json.loads(payload)

#         # Conectar a Elasticsearch
#         es = Elasticsearch(hosts=["http://localhost:9200"])
        
#         # Convertir el payload a un diccionario
#         payload_dict = json.loads(payload)
            
#         # Obtener el número del network_element, del mensaje original
#         network_element_number = obtener_numero_network_element(payload_dict)
        
#         # Verificar si se obtuvo correctamente el número del network_element
#         if network_element_number is not None:
#             # Construir el index con el número del network element
#             index = "beha_pt2mano-agent-net_elem_" + str(network_element_number)
            
#             # Subir el JSON a Elasticsearch
#             res = es.index(index=index, body=json_data)
#             print("Documento subido correctamente a Elasticsearch:", res, "\n")
#             print(f"El mensaje se ha subido a Elasticsearch en el index {index}.\n")    
            
#         else:
#             print("No se pudo obtener el número del network_element para construir el topic.\n")

#     except Exception as e:
#         print("Error al subir el documento a Elasticsearch:", e, "\n")

 
# Función para obtener la lista de elementos de red
def obtener_network_elements(payload):
    try:
        # Parsear el JSON del payload
        topology_data = json.loads(payload)
        
        # Obtener la lista de elementos de red del JSON
        network_elements = [element["id"] for element in topology_data.get("network_elements", [])]
        return network_elements
    except json.decoder.JSONDecodeError as e:
        print(f"Error al cargar el JSON de topología: {e}.\n")
        return None

          
# Función para construir el tema MQTT 
def construir_temas_MQTT(prefijo, array):
    # Inicializar una lista vacía para almacenar los temas MQTT
    temas_MQTT = []  
    # Iterar sobre todos los elementos del array
    for network_element in array:
        # Dividir el elemento usando '_' como separador y seleccionar la última parte
        numero = network_element.split('_')[-1]
        # Construir el tema MQTT concatenando el prefijo con el número obtenido
        tema_MQTT = prefijo + numero
        # Agregar el tema MQTT a la lista de temas
        temas_MQTT.append(tema_MQTT)
    
    return temas_MQTT


# Función para construir el indice de comportamiento de MQTT 
def construir_indices_elasticsearch(prefijo, array):
    # Inicializar una lista vacía para almacenar los indices de elasticsearch
    indices_elasticsearch = []  
    # Iterar sobre todos los elementos del array
    for network_element in array:
        # Dividir el elemento usando '_' como separador y seleccionar la última parte
        numero = network_element.split('_')[-1]
        # Construir el tema MQTT concatenando el prefijo con el número obtenido
        index_elasticsearch = prefijo + numero
        # Agregar el tema MQTT a la lista de temas
        indices_elasticsearch.append(index_elasticsearch)
    
    return indices_elasticsearch


# # Función para obtener el número del network_element
# def obtener_numero_network_element(json_data):
#     try:
#         # Obtener el único elemento de red del JSON
#         network_element = json_data.get("network_elements", [])[0]

#         # Obtener el id del elemento de red
#         id_elemento = network_element.get("id", "")

#         # Si el id tiene el formato "network_element_XXX"
#         if id_elemento.startswith("network_element_"):
#             # Extraer el sufijo numérico y convertirlo a entero
#             numero = int(id_elemento.split("_")[-1])
#             return numero

#         else:
#             print("El formato del ID del network_element no es válido.\n")
#             return None

#     except Exception as e:
#         print(f"Error al obtener el número del network_element: {e}.\n")
#         return None
    
# # Función para obtener el número del network_element del nombre del archivo
# def obtener_numero_network_element_from_filename(filename):
#     try:
#         # Dividir el nombre del archivo usando '_' como separador
#         partes_nombre = filename.split("_")
        
#         # Verificar si hay al menos tres partes en el nombre del archivo
#         if len(partes_nombre) >= 3:
#             # Extraer la tercera parte
#             numero = partes_nombre[2]
#             return numero
#         else:
#             print("El nombre del archivo no tiene el formato esperado.\n")
#             return None
#     except Exception as e:
#         print(f"Error al obtener el número del network_element: {e}\n")
#         return None


# Función para obtener el número del network_element 
def obtener_numero_network_element_from_json(json_data):
    try:
        # Parsear el JSON
        data = json.loads(json_data)
        
        # Obtener el valor del campo 'id'
        id_elemento = data.get("net_element", {}).get("id", "")

        # Si el id tiene el formato "network_element_XXX"
        if id_elemento.startswith("network_element_"):
            # Extraer el sufijo numérico y convertirlo a entero
            numero = id_elemento.split("_")[-1]
            return numero
        else:
            print("El formato del ID del network_element no es válido.\n")
            return None
    except Exception as e:
        print(f"Error al obtener el número del network_element: {e}\n")
        return None

       
# Función de callback para manejar los mensajes recibidos
def on_message(client, userdata, message):
    print(f"Mensaje recibido en el topic '{message.topic}'.\n")
    
    global network_elements
    global mqtt_topics

    if message.topic == mqtt_topic_topology:
        # Obtener la lista de network_elements  
        network_elements = obtener_network_elements(message.payload.decode())
        print("El array network_elements contiene:", network_elements,".\n")
                        
        # Obtener los temas MQTT para los network_elements
        mqtt_topics = construir_temas_MQTT("BEHA_PT2MANO/AGENT/NET_ELEM_", network_elements)
        print("El array de temas contiene:", mqtt_topics,".\n")
        
        # Suscribirse a los temas MQTT de los network_elements
        for topic in mqtt_topics:
            subscribe_to_topic(client, topic)
            
        # Subir el mensaje a Elasticsearch
        upload_topology_to_elasticsearch(message.payload.decode())
        print("El mensaje se ha subido a Elasticsearch en el index 'topology'.\n")
                    
    # Si el mensaje proviene de un network_element
    elif message.topic in mqtt_topics:
        try:
            # SUBIR MENSAJE A ELASTICSEARCH -----------------------------------------------------------------------------------------------
            # Copiar el mensaje original
            modified_payload = message.payload
                
            # Convertir el payload a un diccionario
            payload_dict = json.loads(modified_payload)
                
            # Agregar el campo 'comm_channel' al diccionario
            payload_dict['comm_channel'] = 'PT2MANO'
                
            # Convertir el diccionario modificado de vuelta a JSON
            modified_payload = json.dumps(payload_dict)
                
            # Subir el mensaje a Elasticsearch
            upload_behaviour_to_elasticsearch(modified_payload)
            #print("El mensaje se ha subido a Elasticsearch en el index 'behaviour'.\n")
                
            # PUBLICAR MENSAJE EN TOPIC -----------------------------------------------------------------------------------------------
            # # Convertir el payload a un diccionario
            # payload_dict = json.loads(message.payload)
            
            # Convertir el payload a una cadena JSON
            payload_json = message.payload.decode()
            
            # Obtener el número del network_element, del mensaje original
            #network_element_number = obtener_numero_network_element(payload_dict)
            network_element_number = obtener_numero_network_element_from_json(payload_json)
            
            # Verificar si se obtuvo correctamente el número del network_element
            if network_element_number is not None:
                # Construir el topic con el número del network element
                topic = "BEHA_MANO2DT/AGENT/NET_ELEM_" + str(network_element_number)
                
                # Solicitar confirmación al usuario antes de proceder
                while True:
                    respuesta = input(f"¿Desea proceder con la publicación del archivo en el topic '{topic}'? (S/N): ").strip().lower()
                    if respuesta == 's':
                        # Publicar el mensaje original en el topic BEHA_MANO2DT/AGENT/NET_ELEM_XXX
                        client.publish(topic, message.payload)
                        print(f"Mensaje publicado en el topic '{topic}'.\n")
                        print(f"Mensaje original: {str(message.payload.decode())}.\n")
                        break
                    elif respuesta == 'n':
                        print("La publicación del archivo ha sido cancelada.\n")
                        break
                    else:
                        print("Por favor, responda con 'S' para sí o 'N' para no.")
            else:
                print("No se pudo obtener el número del network_element para construir el topic.\n")
        
        except json.decoder.JSONDecodeError as e:
            print(f"Error al decodificar el JSON del mensaje: {e}.\n")
   
    

# MAIN -----------------------------------------------------------------------------------------------------------------------------------

# Parsear el archivo de configuración
config = parse_config_file("config.json")

# Configurar las variables
topology_path = config["topology_path"]
topology_message_file_path = config["topology_message_file_path"]
behaviour_path = config["behaviour_path"]
mgmt_path = config["mgmt_path"]

mqtt_broker_ip = config["mqtt_broker_ip"]
mqtt_broker_port = config["mqtt_broker_port"]

mqtt_topic_topology = "TOPOLOGY"  # Nombre del tema MQTT al que se publicará la topología


# Crear un cliente MQTT
client = mqtt.Client()

# Asignar la función de callback
client.on_message = on_message

# Conectar al broker MQTT
client.connect(mqtt_broker_ip, mqtt_broker_port, 60)

# Ejecutar la función para suscribirse al tema TOPOLOGY
subscribe_to_topic(client, mqtt_topic_topology)

# Mantener la conexión activa y procesar los mensajes entrantes
client.loop_forever()
