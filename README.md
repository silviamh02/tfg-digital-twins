# Escenario para la comunicación entre el Physical Twin (PT) y el Digital Twin (DT)
## Introducción
El despliegue de este escenario está formado por tres sistemas: sistema DANA, sistema controlador y sistema de gestión. 

>Cuenta con tres directorios:>
1. Directorio de gestión: tfg-digital-twins/mgmt
2. Directorio de topología: tfg-digital-twins/topology
3. Directorio de comportamiento: tfg-digital-twins/behaviour>

En el directorio de gestión se encuentra almacenado el fichero json de configuración del sistema de monitorización, y en los directorios de topología y comportamiento, se almacenan respectivamente, los ficheros json que contienen los datos de topología y comportamiento, para el despliegue de los sistemas.

Cuenta con dos scripts de Python (sistemaDANA.py y sistemaControlador.py), un fichero de configuración (config.json) y un fichero de requerimientos (requirements.txt).

![Diagrama del escenario](assets/images/escenario.png)

### Sistema DANA
...

### Sistema Controlador
...

### Sistema de gestión
...

## Despliegue

1. Clonar el repositorio de github

2. Crear los directorios 
    tfg-digital-twins/topology
    tfg-digital-twins/behaviour