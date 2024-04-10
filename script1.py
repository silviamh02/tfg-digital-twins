import os
import json
import time
import paho.mqtt.client as mqtt
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# FUNCIONES ------------------------------------------------------------------------------------

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
    # Obtener la fecha y hora actual en una estructura de tiempo
    current_time = time.localtime()
    
    # Convertir la estructura de tiempo a un valor EPOCH
    epoch_time = int(time.mktime(current_time))
    
    # Generar el nombre de archivo único utilizando el valor EPOCH
    filename = f"BEHA_{epoch_time}.json"
    
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


# Clase para manejar los eventos del sistema de archivos
class MyFileSystemEventHandler(FileSystemEventHandler):
    # Constructor de la clase
    def __init__(self, mqtt_client, mqtt_topic): 
    #def __init__(self, mqtt_client, mqtt_topic, state): 
        super().__init__() # Llama al constructor de la clase padre
        self.mqtt_client = mqtt_client # Inicializa el cliente MQTT
        self.mqtt_topic = mqtt_topic # Inicializa el topic MQTT
        #self.state = state # Inicializa el estado del agente
        
    # Función para manejar el evento de creación de archivos
    def on_created(self, event): 
        if event.is_directory: # Verifica si el evento es un directorio
            return # Si es un directorio, no hace nada
        filepath = event.src_path # Obtiene la ruta del archivo creado
        print(f"Nuevo archivo creado: {filepath}") # Imprime un mensaje en consola
        
        # Primera prueba SIN VERIFICACIÓN DE ESTADO
        self.publish_json(filepath) # Llama al método para publicar el contenido del archivo JSON

        # # Verifica el estado del agente
        # if self.state == 0:
        #     self.publish_json(filepath) # Llama al método para publicar el contenido del archivo JSON

    # Función para publicar el contenido del archivo JSON
    def publish_json(self, filepath): 
        # Publicar el contenido del JSON a Elasticsearch vía MQTT
        with open(filepath, 'r') as json_file: # Abre el archivo en modo lectura
            json_content = json.load(json_file) # Carga el contenido JSON en un diccionario
            self.mqtt_client.publish(self.mqtt_topic, json.dumps(json_content)) # Publica el contenido JSON en el topic MQTT

   
# Main function
def main():
    # Parsear el archivo de configuración
    config = parse_config_file("config.json")

    # Configurar las variables
    topology_path = config["topology_path"]
    #behavior_path = config["behavior_path"]
    #mgmt_path = config["mgmt_path"]
    
    mqtt_broker_ip = config["mqtt_broker_ip"]
    mqtt_broker_port = config["mqtt_broker_port"]
    
    # Iniciar el cliente MQTT
    mqtt_client = mqtt.Client()
    mqtt_client.connect(mqtt_broker_ip, mqtt_broker_port)

    # # Verificar el estado del agente
    # agent_state_verifier(mgmt_path, mqtt_client)

    observer = Observer()
    event_handler = MyFileSystemEventHandler(mqtt_client, "TOPOLOGY") 
    observer.schedule(event_handler, topology_path, recursive=True) 
    observer.start() 
    print(f"Watchdog iniciado para el directorio: {topology_path}") 

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Ejecutar la función principal
if __name__ == "__main__":
    main()