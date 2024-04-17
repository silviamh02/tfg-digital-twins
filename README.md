# Escenario para la comunicación entre el Physical Twin (PT) y el Digital Twin (DT)
## Introducción
El despliegue de este escenario está formado por tres sistemas: sistema DANA, sistema controlador y sistema de gestión. 

**Componentes del repositorio:**
1. Directorio de gestión: tfg-digital-twins/mgmt
    json configuración sistema monitorización: tfg-digital-twins/mgmt/mgmt.json
2. Directorio de topología: tfg-digital-twins/topology
    jsons datos topología: tfg-digital-twins/topology/TOPO_*.json
3. Directorio de comportamiento: tfg-digital-twins/behaviour
    jsons datos comportamiento: tfg-digital-twins/behaviour/BEHA_*.json
4. Fichero de configuración: config.json
5. Fichero de requerimientos: requirements.txt
6. Script de python del sistema DANA: sistemaDANA.py
7. Script de python del sistema Controlador: sistemaControlador.py

En el directorio de gestión se encuentra almacenado el fichero json de configuración del sistema de monitorización, y en los directorios de topología y comportamiento, se almacenan los ficheros json que contienen los datos de topología y comportamiento, respectivamente.

El escenario cuenta con un archivo de configuración (config.json) en el que se definen campos como el path de los JSON de topología, el path de los JSON de comportamiento, la IP del Broker MQTT, el puerto MQTT a utilizar, entre otros valores necesarios. También dispone de un archivo de requerimientos (requirements.txt), utilizado para especificar las dependencias del proyecto, y por último de dos scripts de Python (sistemaDANA.py y sistemaControlador.py).

### Descripción del escenario
![Diagrama del escenario](assets/images/escenario.png)

**Sistema de gestión**

En el contexto de este escenario, el "sistema de gestión" se refiere a un conjunto de componentes y contenedores Docker que se encargan de coordinar y gestionar las operaciones de los sistemas desplegados, así como de administrar los servicios y recursos necesarios para su funcionamiento adecuado. Este sistema se encarga de asegurar que todos los componentes del escenario estén configurados y operativos según las necesidades del proyecto.

El sistema de gestión incluye:

**- Mosquitto MQTT (broker MQTT):** Este servicio actúa como el broker MQTT para la comunicación entre los distintos elementos del sistema, permitiendo la transferencia de mensajes y datos entre ellos. Se configura con el puerto 1883 y sin utilizar SSL/TLS.

**- Elasticsearch:** Funciona como un motor de búsqueda y análisis de datos distribuido, encargado de almacenar y procesar grandes volúmenes de datos generados por el sistema. Se configura con el puerto 9200 y sin utilizar SSL/TLS.

**- Kibana:** Es una plataforma de visualización y análisis de datos que se integra con Elasticsearch, permitiendo explorar y visualizar los datos almacenados en Elasticsearch a través de paneles interactivos y gráficos. Se configura con el puerto 5601 y sin utilizar SSL/TLS.

Tal y como se ha comentado previamente, el sistema de gestión también incluye un archivo llamado "mgmt.json" ubicado en el directorio "tfg-digital-twins/mgmt". Este archivo contiene información crítica sobre la configuración del sistema, incluido el estado actual del agente y la configuración de los servicios Mosquitto MQTT, Elasticsearch y Kibana.

En conjunto, el sistema de gestión asegura la correcta operación y gestión efectiva del entorno desplegado, proporcionando los servicios necesarios para la comunicación, almacenamiento y visualización de datos en el sistema.

**Sistema DANA**
El Sistema DANA es una herramienta diseñada para la emulación del comportamiento de un sistema en el Gemelo Físico (PT).

El sistema hace uso de la biblioteca watchdog, que se encarga de monitorizar los paths definidos en el archivo de configuración. Inicialmente Cuando detecta un cambio en el archivo de configuraci, realiza las siguientes acciones:

Estado (Topología):

Obtiene el listado de elementos de red para su posterior uso.
Lee el JSON y lo envía vía MQTT al topic "TOPOLOGY".
Detección de Archivo Tipo 2 (Comportamiento):

Trocea el JSON en base a los elementos de red.
Envía cada "sub JSON" al topic específico vía MQTT.

**Sistema Controlador**
...



## Despliegue

1. Clonar el repositorio de github

2. Crear los directorios 
    tfg-digital-twins/topology
    tfg-digital-twins/behaviour