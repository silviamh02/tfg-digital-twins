import os
import json
import time
import paho.mqtt.client as mqtt
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# FUNCIONES ------------------------------------------------------------------------------------------------------------------------------

# Función para cargar la configuración desde el archivo JSON
def parse_config_file(config_file_path):
    with open(config_file_path, 'r') as config_file: # Abre el archivo en modo lectura
        config_data = json.load(config_file) # Carga el JSON en un diccionario
    return config_data # Devuelve el diccionario


# Función para generar el nombre único del JSON de topología
def generate_unique_filename_topology():
    # Obtener la fecha y hora actual en una estructura de tiempo
    current_time = time.localtime()
    
    # Convertir la estructura de tiempo a un valor EPOCH
    epoch_time = int(time.mktime(current_time))
    
    # Generar el nombre de archivo único utilizando el valor EPOCH
    filename = f"TOPO_{epoch_time}.json"
    
    return filename


# Función para generar el nombre único del JSON de comportamiento
def generate_unique_filename_behavior():
    # Obtener la marca de tiempo actual
    timestamp = int(time.time()) 
    
    # Generar el nombre de archivo único
    filename = f"BEHA_{timestamp}.json"
    
    return filename

# Función para generar JSON de topología
def generate_topology_json(topology_path):
    # Crear el diccionario con los datos de topología
    topology_json = {
        "message": "JSON topology de prueba" # Añadir los datos de la topología más adelante!!!
    }
    
    # Obtener el nombre único del archivo
    filename = generate_unique_filename_topology()
    
    # Combinar el nombre de archivo con el path de topología
    file_path = os.path.join(topology_path, filename)
    
    # Escribir el JSON en el archivo
    with open(file_path, 'w') as json_file:
        json.dump(topology_json, json_file, indent=4)
    
    # Devolver la ruta completa del archivo generado
    return file_path


# Función para generar JSON de comportamiento
def generate_behavior_json(behavior_path):
    # Crear el diccionario con los datos de comportamiento
    behavior_json = { 
        "message": "JSON behavior de prueba" # Añadir los datos del comportamiento más adelante!!!
    }
    
    # Obtener el nombre único del archivo
    filename = generate_unique_filename_behavior()
    
    # Combinar el nombre de archivo con el path de topología
    file_path = os.path.join(behavior_path, filename)
    
    # Escribir el JSON en el archivo
    with open(file_path, 'w') as json_file:
        json.dump(behavior_json, json_file, indent=4)
    
    # Devolver la ruta completa del archivo generado
    return file_path


# Función para publicar el archivo JSON detectado en un tema MQTT
def publish_json_file(client, topic, file_path):
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            message = json.dumps(data)
            client.publish(topic, message)
    except json.decoder.JSONDecodeError as e:
        print(f"Error al cargar el archivo JSON: {e}")
    except FileNotFoundError as e:
        print(f"Error: No se pudo encontrar el archivo: {file_path}")


# Función para verificar el estado del agente
def verificar_estado_agente(mgmt_json_path):
    try:
        with open(mgmt_json_path, 'r') as mgmt_file:
            data = json.load(mgmt_file)
            estado = data.get("estado_agente", None)
            if estado is not None:
                return estado
            else:
                print("Error: El archivo de gestión no contiene el estado del agente.")
                return None
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo de gestión en {mgmt_path}.")
        return None
    except json.decoder.JSONDecodeError as e:
        print(f"Error al cargar el archivo de gestión JSON: {e}")
        return None


# Función para cambiar el estado del agente en el archivo JSON de gestión
def cambiar_estado_agente(mgmt_json_path, nuevo_estado):
    try:
        with open(mgmt_json_path, 'r+') as mgmt_file:
            data = json.load(mgmt_file)
            data["estado_agente"] = nuevo_estado
            mgmt_file.seek(0)  # Mover el puntero al inicio del archivo
            json.dump(data, mgmt_file, indent=4)
            mgmt_file.truncate()  # Truncar el archivo si es necesario
        print(f"Estado del agente cambiado a: {nuevo_estado}")
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo de gestión en {mgmt_json_path}.")
    except json.decoder.JSONDecodeError as e:
        print(f"Error al cargar el archivo de gestión JSON: {e}")
        
       
# Función watchdog que monitoriza los directorios 
def watchdog(client, mqtt_topic_topology, mqtt_topic_behaviour, mgmt_path, mgmt_json_path, topology_path, behaviour_path):
    # Crear el observador de cambios en el sistema de archivos
    observer = Observer()

    # Diccionario para almacenar las observaciones activas
    observaciones_activas = {}

    # Función para iniciar la observación
    def iniciar_observacion(event, directorio):
        if directorio not in observaciones_activas:
            observer.schedule(event, directorio, recursive=False)
            observaciones_activas[directorio] = True
            print(f"La observación en {directorio} se ha iniciado.")
        else:
            print(f"La observación en {directorio} ya está en ejecución.")

    # # Función para detener la observación
    # def detener_observacion(observer, event_handler, directorio):
    #     if directorio in observaciones_activas:
    #         print(f"Deteniendo observación en el directorio: {directorio}")
    #         observer.unschedule(event_handler)
    #         del observaciones_activas[directorio]
    #         print(f"La observación en {directorio} se ha detenido.")
    #     else:
    #         print(f"No hay observación en {directorio} para detener.")

    # Función para manejar los eventos    
    def handle_directory_change(event):
        nonlocal observer
        if not event.is_directory and event.src_path.endswith('.json'):
            if event.src_path == mgmt_json_path:  # Modificación en el archivo mgmt.json
                estado_agente = verificar_estado_agente(mgmt_json_path)
                if estado_agente == 0:
                    # Programar la observación de topología si no está programada
                    iniciar_observacion(event_handler_topology, topology_path)
                    # Cancelar la observación de comportamiento si está programada
                    #detener_observacion(observer, event_handler_behaviour, behaviour_path)
                elif estado_agente == 1:
                    # Programar la observación de comportamiento si no está programada
                    iniciar_observacion(event_handler_behaviour, behaviour_path)
                    # Cancelar la observación de topología si está programada
                    #detener_observacion(observer, event_handler_topology, topology_path)
            elif event.src_path.startswith(topology_path) and verificar_estado_agente(mgmt_json_path) == 0: 
                publish_json_file(client, mqtt_topic_topology, event.src_path)
                print(f"Publicando el archivo {event.src_path} en el tema {mqtt_topic_topology}.")
                cambiar_estado_agente(mgmt_json_path, 1)
            elif event.src_path.startswith(behaviour_path) and verificar_estado_agente(mgmt_json_path) == 1:
                publish_json_file(client, mqtt_topic_behaviour, event.src_path)
                print(f"Publicando el archivo {event.src_path} en el tema {mqtt_topic_behaviour}.")

    # Instanciar un observador para detectar la modificación de archivos en mgmt_path
    event_handler_mgmt = FileSystemEventHandler()
    event_handler_mgmt.on_modified = handle_directory_change

    # Instanciar un observador para detectar la creación de archivos en topology_path
    event_handler_topology = FileSystemEventHandler()
    event_handler_topology.on_created = handle_directory_change

    # Instanciar un observador para detectar la creación de archivos en behaviour_path
    event_handler_behaviour = FileSystemEventHandler()
    event_handler_behaviour.on_created = handle_directory_change

    # Programar la observación del directorio mgmt_path
    observer.schedule(event_handler_mgmt, mgmt_path, recursive=False)
    
    # Iniciar la observación del directorio topology_path
    iniciar_observacion(event_handler_topology, topology_path)

    observer.start()
    print(f"Inicialmente watchdog está monitoreando los directorios: {mgmt_path}, {topology_path}")

    return observer


# MAIN ------------------------------------------------------------------------------------------------------------------------------

# Parsear el archivo de configuración
config = parse_config_file("config.json")

# Configurar las variables
topology_path = config["topology_path"]
behaviour_path = config["behaviour_path"]
mgmt_path = config["mgmt_path"]
mgmt_json_path = config["mgmt_json_path"]

mqtt_broker_ip = config["mqtt_broker_ip"]
mqtt_broker_port = config["mqtt_broker_port"]

mqtt_topic_topology = "TOPOLOGY"  # Nombre del tema MQTT al que se publicará la topología
mqtt_topic_behaviour = "BEHAVIOUR"  # Nombre del tema MQTT para el comportamiento

# Crear un cliente MQTT
client = mqtt.Client()

# Conectar al broker MQTT
client.connect(mqtt_broker_ip, mqtt_broker_port, 60)

# Inicializar el estado del agente
estado_agente = verificar_estado_agente(mgmt_json_path)
    
# Configurar Watchdog
# observer = watchdog(client, mqtt_topic, topology_path)
observer = watchdog(client, mqtt_topic_topology, mqtt_topic_behaviour, mgmt_path, mgmt_json_path, topology_path, behaviour_path)

# Configurar el intervalo de tiempo en segundos (1 minuto = 60 segundos)
intervalo_tiempo = 60
    
# Bucle principal
while True:
    # Verificar el estado del agente nuevamente en cada iteración
    estado_agente = verificar_estado_agente(mgmt_json_path)
    
    # Estado 0: Generar el JSON de topología
    if estado_agente == 0:
        generate_topology_json(topology_path)
        print(f"Se ha generado un JSON de topología en {topology_path}.")
        
    # Estado 1: Generar el JSON de comportamiento
    if estado_agente == 1:
        generate_behavior_json(behaviour_path)
        print(f"Se ha generado un JSON de comportamiento en {behaviour_path}.")
    # generate_behavior_json(behaviour_path)
    # print(f"Se ha generado un JSON de comportamiento en {behaviour_path}.")
        
    # Esperar el intervalo de tiempo
    time.sleep(intervalo_tiempo)