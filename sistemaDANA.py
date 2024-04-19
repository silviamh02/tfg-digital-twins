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
def generate_unique_filename_behaviour():
    # Obtener la marca de tiempo actual
    timestamp = int(time.time()) 
    
    # Generar el nombre de archivo único
    filename = f"BEHA_{timestamp}.json"
    
    return filename


# Función para generar JSON de topología
def generate_topology_json(topology_path, topology_message_file_path):
    # Leer el contenido del archivo message.json
    with open(topology_message_file_path, 'r') as message_file:
        message_data = json.load(message_file)
    
    # Obtener el nombre único del archivo
    filename = generate_unique_filename_topology()
    
    # Combinar el nombre de archivo con el path de topología
    file_path = os.path.join(topology_path, filename)
    
    # Escribir el JSON en el archivo
    with open(file_path, 'w') as json_file:
        json.dump(message_data, json_file, indent=4)
    
    # Devolver la ruta completa del archivo generado
    return file_path


# Función para generar JSON de comportamiento
def generate_behaviour_json(behaviour_path, behaviour_message_file_path):
    # Leer el contenido del archivo message.json
    with open(behaviour_message_file_path, 'r') as message_file:
        message_data = json.load(message_file)
    
    # Obtener el nombre único del archivo
    filename = generate_unique_filename_behaviour()
    
    # Combinar el nombre de archivo con el path de topología
    file_path = os.path.join(behaviour_path, filename)
    
    # Escribir el JSON en el archivo
    with open(file_path, 'w') as json_file:
        json.dump(message_data, json_file, indent=4)
    
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
        print(f"Error al cargar el archivo JSON: {e}.\n")
    except FileNotFoundError as e:
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
            

# Función para verificar el estado del agente
def verificar_estado_agente(mgmt_json_path):
    try:
        with open(mgmt_json_path, 'r') as mgmt_file:
            data = json.load(mgmt_file)
            estado = data.get("estado_agente", None)
            if estado is not None:
                return estado
            else:
                print("Error: El archivo de gestión no contiene el estado del agente.\n")
                return None
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo de gestión en {mgmt_path}.\n")
        return None
    except json.decoder.JSONDecodeError as e:
        print(f"Error al cargar el archivo de gestión JSON: {e}.\n")
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
        print(f"Estado del agente cambiado a: {nuevo_estado}.\n")
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo de gestión en {mgmt_json_path}.\n")
    except json.decoder.JSONDecodeError as e:
        print(f"Error al cargar el archivo de gestión JSON: {e}.\n")


# Función para obtener la lista de elementos de red
def obtener_network_elements(topology_file_path):
    try:
        with open(topology_file_path, 'r') as json_file:
            topology_data = json.load(json_file)
            network_elements = [element["id"] for element in topology_data.get("network_elements", [])]
            return network_elements
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo de topología en {topology_file_path}.")
        return None
    except json.decoder.JSONDecodeError as e:
        print(f"Error al cargar el archivo de topología JSON: {e}.")
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


# Función para trocear el archivo JSON y publicarlo en los temas MQTT correspondientes
def trocear_json(behaviour_json_path, network_elements, mqtt_client, mqtt_topics):
    with open(behaviour_json_path, 'r') as file:
        behaviour_json = json.load(file)
    
    for i, network_element in enumerate(network_elements):
        # Crear un nuevo JSON solo con el network_element actual
        network_element_json = {
            "network_elements": [behaviour_json["network_elements"][i]]
        }
        
        # Publicar el nuevo JSON en el tema MQTT correspondiente
        message = json.dumps(network_element_json)
        mqtt_client.publish(mqtt_topics[i], message)
        print(f"Publicando el JSON troceado en el tema {mqtt_topics[i]}.\n")
        
        # --------------------
        # Obtener el número del network_element que se acaba de publicar
        network_element_number = None
        with open(behaviour_json_path, 'r') as file:
            try:
                json_data = json.load(file)
                network_element_number = obtener_numero_network_element(json_data)
            except json.decoder.JSONDecodeError as e:
                print(f"Error al cargar el archivo JSON: {e}.")
            except Exception as e:
                print(f"Error: {e}")
                
        # Verificar si se obtuvo correctamente el número del network_element
        if network_element_number is not None:
            # Construir el topic con el número del network element
            topic = "BEHA_MANO2DT/AGENT/NET_ELEM_" + str(network_element_number)
            # Subscribirse al tema MQTT
            subscribe_to_topic(client, topic)
        
        
# Función para obtener el número del network_element
def obtener_numero_network_element(json_data):
    try:
        # Obtener el único elemento de red del JSON
        network_element = json_data.get("network_elements", [])[0]

        # Obtener el id del elemento de red
        id_elemento = network_element.get("id", "")

        # Si el id tiene el formato "network_element_XXX"
        if id_elemento.startswith("network_element_"):
            # Extraer el sufijo numérico y convertirlo a entero
            numero = int(id_elemento.split("_")[-1])
            return numero

        else:
            print("El formato del ID del network_element no es válido.\n")
            return None

    except Exception as e:
        print(f"Error al obtener el número del network_element: {e}.\n")
        return None


# Función watchdog que monitoriza los directorios 
def watchdog(client, mqtt_topic_topology, mgmt_path, mgmt_json_path, topology_path, behaviour_path):
    # Crear el observador de cambios en el sistema de archivos
    observer = Observer()

    # Diccionario para almacenar las observaciones activas
    observaciones_activas = {}

    # Función para iniciar la observación
    def iniciar_observacion(event, directorio):
        if directorio not in observaciones_activas:
            observer.schedule(event, directorio, recursive=False)
            observaciones_activas[directorio] = True
            print(f"La observación en {directorio} se ha iniciado.\n")
        else:
            print(f"La observación en {directorio} ya está en ejecución.\n")

    # # Función para detener la observación
    # def detener_observacion(observer, event_handler, directorio):
    #     if directorio in observaciones_activas:
    #         print(f"Deteniendo observación en el directorio: {directorio}.\n")
    #         observer.unschedule(event_handler)
    #         del observaciones_activas[directorio]
    #         print(f"La observación en {directorio} se ha detenido.\n")
    #     else:
    #         print(f"No hay observación en {directorio} para detener.\n")

    # Función para manejar los eventos    
    def handle_directory_change(event):
        nonlocal observer
        global topology_file_path
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
                # Guardar la ruta del archivo JSON de topología
                topology_file_path = event.src_path
                
                # Publicar el archivo JSON
                publish_json_file(client, mqtt_topic_topology, event.src_path)
                print(f"Publicando el archivo {event.src_path} en el tema {mqtt_topic_topology}.\n")
                
                # Cambiar el estado del agente a 1
                cambiar_estado_agente(mgmt_json_path, 1)
                
            elif event.src_path.startswith(behaviour_path) and verificar_estado_agente(mgmt_json_path) == 1:
                # Obtener la lista de network_elements  
                network_elements = obtener_network_elements(topology_file_path)
                print("El array network_elements contiene:", network_elements,".\n")
                  
                # Obtener los temas MQTT para los network_elements
                mqtt_topics = construir_temas_MQTT("BEHA_PT2MANO/AGENT/NET_ELEM_", network_elements)
                print("El array de temas contiene:", mqtt_topics,".\n")
                
                # Trocear el archivo JSON y publicarlo en los temas MQTT
                trocear_json(event.src_path, network_elements, client, mqtt_topics)
                #publish_json_file(client, mqtt_topics, event.src_path)
                #print(f"Publicando el archivo {event.src_path} en el tema {mqtt_topic_behaviour}.\n")
                

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
    #iniciar_observacion(event_handler_topology, topology_path)
    observer.schedule(event_handler_topology, topology_path, recursive=False)

    observer.start()
    print(f"Inicialmente watchdog está monitoreando los directorios: {mgmt_path} y {topology_path}.\n")

    return observer


# MAIN ------------------------------------------------------------------------------------------------------------------------------

# Parsear el archivo de configuración
config = parse_config_file("config.json")

# Configurar las variables
topology_path = config["topology_path"]
topology_message_file_path = config["topology_message_file_path"]

behaviour_path = config["behaviour_path"]
behaviour_message_file_path = config["behaviour_message_file_path"]

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
observer = watchdog(client, mqtt_topic_topology, mgmt_path, mgmt_json_path, topology_path, behaviour_path)

# Configurar el intervalo de tiempo en segundos (1 minuto = 60 segundos)
intervalo_tiempo = 60
    
# Bucle principal
while True:
    # Verificar el estado del agente nuevamente en cada iteración
    estado_agente = verificar_estado_agente(mgmt_json_path)
    
    # Estado 0: Generar el JSON de topología
    if estado_agente == 0:
        # Generar el JSON de topología
        topology_file_path = generate_topology_json(topology_path, topology_message_file_path)
        print(f"Se ha generado un JSON de topología en {topology_path}.\n")
        
    # Estado 1: Generar el JSON de comportamiento
    if estado_agente == 1:
        generate_behaviour_json(behaviour_path, behaviour_message_file_path)
        print(f"Se ha generado un JSON de comportamiento en {behaviour_path}.\n")
            
    # Esperar el intervalo de tiempo
    time.sleep(intervalo_tiempo)