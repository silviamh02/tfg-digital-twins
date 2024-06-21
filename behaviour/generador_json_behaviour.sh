#!/bin/bash

CURRENT_TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%S+00:00")

# Directorio donde se encuentra el archivo JSON de topología
topology_dir="/home/silvia/tfg-digital-twins/topology"

# Buscar el archivo más reciente que coincida con el patrón TOPO_*.json
archivo_json=$(ls -t "${topology_dir}"/TOPO_*.json 2>/dev/null | head -n 1)

if [ -z "$archivo_json" ]; then
    echo "No se encontraron archivos JSON de topología en ${topology_dir}"
    exit 1
fi

echo "El archivo JSON de topología más reciente es: ${archivo_json}"

# Directorio de salida para los JSONs de comportamiento
output_dir="/home/silvia/tfg-digital-twins/behaviour"

generate_filename() {
    number="$1"
    epoch=$(date +%s%N)  # Obtener el tiempo actual en nanosegundos
    echo "$output_dir/net_elem_${number}.json_${epoch}.json"
}

# Leer y parsear el archivo JSON de topología para obtener los elementos de red
network_elements=$(jq -c '.network_elements[]' "$archivo_json")

# Contar el número de elementos de red
num_elements=$(echo "$network_elements" | wc -l)

i=1
for element in $network_elements; do
    formatted_i=$(printf "%03d" $i)
    for ((j=1; j<=4; j++)); do
        # Incrementar el timestamp en 1 minuto en cada iteración
        NEW_TIMESTAMP=$(date -u -d "${CURRENT_TIMESTAMP} + ${i} minutes" +"%Y-%m-%dT%H:%M:%S+00:00")

        net_increment=$(awk -v min=10 -v max=100 -v seed="$RANDOM" 'BEGIN{srand(seed); printf "%.2f\n", min+rand()*(max-min)}')
        net_in=$(awk -v net_in="$net_in" -v net_incr="$net_increment" 'BEGIN{printf "%.2f\n", net_in + net_incr}')

        net_out_increment=$(awk -v min=10 -v max=100 -v seed="$RANDOM" 'BEGIN{srand(seed); printf "%.2f\n", min+rand()*(max-min)}')
        net_out=$(awk -v net_out="$net_out" -v net_out_incr="$net_out_increment" 'BEGIN{printf "%.2f\n", net_out + net_out_incr}')

        # Crear un documento JSON con el nuevo timestamp
        JSON_DATA='{
          "net_element": {
            "comm_channel": "PT2MANO",
            "timestamp": "'${NEW_TIMESTAMP}'",
            "flag_status": "1",
            "is_generic_hw": "true",
            "is_gateway": "false",
            "id": "network_element_'$formatted_i'",
            "id_scenario": "caso_II",
            "agent_behavior_data": {
              "uuid": "caso_ii_'$formatted_i'",
              "name": "user_equipment",
              "desc": "virtualmachine_'$formatted_i'",
              "so": "ubuntu20.04",
              "disk": "25GB",
              "cpu": "2",
              "ram": "2GB",
              "virtualbox": {
                "vms": {
                  "name": "vmachine_ue",
                  "status": "running",
                  "resources": {
                    "cpu": "2",
                    "ram": {
                      "used": "1",
                      "total": "2"
                    },
                    "disk": {
                      "used": "10",
                      "total": "25"
                    }
                  },
                  "config": {
                    "so": "ubuntu",
                    "version": "20.04",
                    "net": {
                      "ens3": {
                        "name": "ens3",
                        "status": "connected",
                        "ip_dir": "10.100.100.22",
                        "adapter_type": "red_interna",
                        "mapping_ports": ""
                      },
                      "ens9": {
                        "name": "ens9",
                        "status": "connected",
                        "ip_dir": "10.200.1.1",
                        "adapter_type": "red_interna",
                        "mapping_ports": ""
                      }
                    }
                  },
                  "details": {
                    "so": "ubuntu20.04LTS",
                    "connected_users": "1"
                  }
                }
              },
              "docker": {
                "docker_version": "20.10.24",
                "containers": {
                    "001":{
                          "id": "c7b701d6be9a",
                          "name": "cliente_VLC",
                          "status": "up",
                          "resources": {
                            "cpu": "'$(awk -v min=1.25 -v max=20 -v seed="$RANDOM" 'BEGIN{srand(seed); printf "%.2f\n", min+rand()*(max-min)}')'",
                            "ram": "'$(awk -v min=1.25 -v max=50 -v seed="$RANDOM" 'BEGIN{srand(seed); printf "%.2f\n", min+rand()*(max-min)}')'",
                            "net": {
                              "in": "'${net_in}MB'",
                              "out": "'${net_out}MB'",
                              "adap_type": "tesis_network",
                              "map_ports": ""
                            },
                            "disk": "34.16MB"
                          },
                          "details": {
                            "name": "ubuntu",
                            "version": "20.04"
                          }
                      }
                   }
              },
              "kubernetes": {
                "cluster": {
                  "nodes": {
                    "name": "",
                    "state": "",
                    "resources": {
                      "cpu": "",
                      "ram": "",
                      "disk": "",
                      "net": {
                        "in": "",
                        "out": "",
                        "adap_type": "",
                        "map_ports": ""
                      }
                    },
                    "details": {
                      "tags": "",
                      "uptime": ""
                    }
                  },
                  "pods": {
                    "total": "",
                    "running": "",
                    "pending": ""
                  },
                  "details": {
                    "version": ""
                  }
                }
              }
            }
          }
        }'

        # Generar el nombre del archivo
        filename=$(generate_filename "${formatted_i}_$j")

        # Crear el archivo JSON con los datos actuales
        echo "$JSON_DATA" > "$filename"

        echo -e "Archivo creado: $filename\n"
    done
    i=$((i+1))
done

echo "Se han generado $((num_elements * 4)) JSONs de comportamiento, 4 de cada uno de los $num_elements network elements en $output_dir."