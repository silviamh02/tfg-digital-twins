CURRENT_TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%S+00:00")
#CURRENT_TIMESTAMP=$(date -u -d "${CURRENT_TIMESTAMP} - 1 week" +"%Y-%m-%dT%H:%M:%S+00:00")

output_dir="/home/silvia/tfg-digital-twins/behaviour"


generate_filename() {
    # Extraer el número de la variable
    number="${1#*DATA_}"
    epoch=$(date +%s%N)  # Obtener el tiempo actual en nanosegundos
    echo "$output_dir/net_elem_$number"_"$epoch.json"
}

for ((i=0; i<2; i++)); do
        # Incrementar el timestamp en 1 minuto en cada iteración

        net_increment=$(awk -v min=10 -v max=100 -v seed="$RANDOM" 'BEGIN{srand(seed); printf "%.2f\n", min+rand()*(max-min)}')
        net_in=$(awk -v net_in="$net_in" -v net_incr="$net_increment" 'BEGIN{printf "%.2f\n", net_in + net_incr}')

        net_out_increment=$(awk -v min=10 -v max=100 -v seed="$RANDOM" 'BEGIN{srand(seed); printf "%.2f\n", min+rand()*(max-min)}')
        net_out=$(awk -v net_out="$net_out" -v net_out_incr="$net_out_increment" 'BEGIN{printf "%.2f\n", net_out + net_out_incr}')

        NEW_TIMESTAMP=$(date -u -d "${CURRENT_TIMESTAMP} + ${i} minutes" +"%Y-%m-%dT%H:%M:%S+00:00")

        # Crear un documento JSON con el nuevo timestamp
        JSON_DATA_001='{
          "net_element": {
            "comm_channel": "PT2MANO",
            "timestamp": "'${NEW_TIMESTAMP}'",
            "flag_status": "1",
            "is_generic_hw": "true",
            "is_gateway": "false",
            "id": "network_element_001",
            "id_scenario": "caso_II",
            "agent_behavior_data": {
              "uuid": "caso_ii_001",
              "name": "user_equipment",
              "desc": "virtualmachine_001",
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
        JSON_DATA_002='{
          "net_element": {
            "comm_channel": "PT2MANO",
            "timestamp": "'${NEW_TIMESTAMP}'",
            "flag_status": "1",
            "is_generic_hw": "true",
            "is_gateway": "false",
            "id": "network_element_002",
            "id_scenario": "caso_II",
            "agent_behavior_data": {
              "uuid": "caso_ii_002",
              "name": "stg_utg",
              "desc": "virtualmachine_002",
              "so": "ubuntu20.04",
              "disk": "25GB",
              "cpu": "2",
              "ram": "2GB",
              "virtualbox": {
                "vms": {
                  "name": "vmachine_stgutg",
                  "status": "running",
                  "resources": {
                    "cpu": "2",
                    "ram": {
                      "used": "1.1",
                      "total": "2"
                    },
                    "disk": {
                      "used": "9",
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
                        "ip_dir": "10.100.100.23",
                        "adapter_type": "red_interna",
                        "mapping_ports": ""
                      },
                      "ens8": {
                        "name": "ens8",
                        "status": "connected",
                        "ip_dir": "192.168.60.10",
                        "adapter_type": "red_interna",
                        "mapping_ports": ""
                      },
                      "ens9": {
                        "name": "ens9",
                        "status": "connected",
                        "ip_dir": "10.200.1.2",
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
                "docker_version": "",
                "containers": {
                  "id": "",
                  "name": "",
                  "status": "",
                  "resources": {
                    "cpu": "",
                    "ram": "",
                    "net": {
                      "in": "",
                      "out": "",
                      "adap_type": "",
                      "map_ports": ""
                    },
                    "disk": ""
                  },
                  "details": {
                    "name": "",
                    "version": ""
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
        JSON_DATA_003='{
          "net_element": {
            "comm_channel": "PT2MANO",
            "timestamp": "'${NEW_TIMESTAMP}'",
            "flag_status": "1",
            "is_generic_hw": "true",
            "is_gateway": "false",
            "id": "network_element_003",
            "id_scenario": "caso_II",
            "agent_behavior_data": {
              "uuid": "caso_ii_003",
              "name": "5G_core",
              "desc": "virtualmachine_003",
              "so": "ubuntu20.04",
              "disk": "25GB",
              "cpu": "2",
              "ram": "2GB",
              "virtualbox": {
                "vms": {
                  "name": "vmachine_free5gc",
                  "status": "running",
                  "resources": {
                    "cpu": "2",
                    "ram": {
                      "used": "1.1",
                      "total": "2"
                    },
                    "disk": {
                      "used": "9",
                      "total": "25"
                    }
                  },
                  "config": {
                    "so": "ubuntu",
                    "version": "20.04",
                    "net": {
                      "ens3":{
                          "name": "ens3",
                          "status": "connected",
                          "ip_dir": "10.100.100.24",
                          "adapter_type": "internal",
                          "mapping_ports": ""
                       },
                      "ens8":{
                          "name": "ens8",
                          "status": "connected",
                          "ip_dir": "192.168.60.11",
                          "adapter_type": "internal",
                          "mapping_ports": ""
                       },
                      "ens10":{
                          "name": "ens10",
                          "status": "connected",
                          "ip_dir": "192.168.99.1",
                          "adapter_type": "internal",
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
                    "001": {
                          "id": "1052bf48245d",
                          "name": "n3iwf",
                          "status": "up",
                          "resources": {
                            "cpu": "'$(awk -v min=1.25 -v max=20 -v seed="$RANDOM" 'BEGIN{srand(seed); printf "%.2f\n", min+rand()*(max-min)}')'",
                            "ram": "'$(awk -v min=1.25 -v max=50 -v seed="$RANDOM" 'BEGIN{srand(seed); printf "%.2f\n", min+rand()*(max-min)}')'",
                            "net": {
                              "in": "'${net_in}kB'",
                              "out": "'${net_out}kB'",
                              "adap_type": "free5gc-compose-321_privnet",
                              "map_ports": ""
                            },
                            "disk": "5.87kB"
                          },
                          "details": {
                            "name": "free5gc/n3iwf",
                            "version": "v3.2.1"
                          }
                    },
                    "002": {
                          "id": "be0fb35c50a2",
                          "name": "ueransim",
                          "status": "up",
                          "resources": {
                            "cpu": "'$(awk -v min=1.25 -v max=20 -v seed="$RANDOM" 'BEGIN{srand(seed); printf "%.2f\n", min+rand()*(max-min)}')'",
                            "ram": "'$(awk -v min=1.25 -v max=50 -v seed="$RANDOM" 'BEGIN{srand(seed); printf "%.2f\n", min+rand()*(max-min)}')'",
                            "net": {
                              "in": "'${net_in}kB'",
                              "out": "'${net_out}kB'",
                              "adap_type": "free5gc-compose-321_privnet",
                              "map_ports": ""
                            },
                            "disk": "34.16MB"
                          },
                          "details": {
                            "name": "free5gc/ueransim",
                            "version": "v3.3.0"
                          }
                    },
                    "003": {
                          "id": "8835628fdd04",
                          "name": "nssf",
                          "status": "up",
                          "resources": {
                            "cpu": "'$(awk -v min=1.25 -v max=20 -v seed="$RANDOM" 'BEGIN{srand(seed); printf "%.2f\n", min+rand()*(max-min)}')'",
                            "ram": "'$(awk -v min=1.25 -v max=50 -v seed="$RANDOM" 'BEGIN{srand(seed); printf "%.2f\n", min+rand()*(max-min)}')'",
                            "net": {
                              "in": "'${net_in}kB'",
                              "out": "'${net_out}kB'",
                              "adap_type": "free5gc-compose-321_privnet",
                              "map_ports": "8000/tcp"
                            },
                            "disk": "76kB"
                          },
                          "details": {
                            "name": "free5gc/nssf",
                            "version": "v3.2.1"
                          }
                    },
                    "004": {
                          "id": "eed6657bbd37",
                          "name": "amf",
                          "status": "up",
                          "resources": {
                            "cpu": "'$(awk -v min=1.25 -v max=20 -v seed="$RANDOM" 'BEGIN{srand(seed); printf "%.2f\n", min+rand()*(max-min)}')'",
                            "ram": "'$(awk -v min=1.25 -v max=50 -v seed="$RANDOM" 'BEGIN{srand(seed); printf "%.2f\n", min+rand()*(max-min)}')'",
                            "net": {
                              "in": "'${net_in}kB'",
                              "out": "'${net_out}kB'",
                              "adap_type": "free5gc-compose-321_privnet",
                              "map_ports": "8000/tcp, 48412->38412/sctp, 48412->38412/sctp"
                            },
                            "disk": "2.78kB"
                          },
                          "details": {
                            "name": "free5gc/amf",
                            "version": "v3.2.1"
                          }
                    },
                    "005": {
                          "id": "efbcba7e1f29",
                          "name": "udr",
                          "status": "up",
                          "resources": {
                            "cpu": "'$(awk -v min=1.25 -v max=20 -v seed="$RANDOM" 'BEGIN{srand(seed); printf "%.2f\n", min+rand()*(max-min)}')'",
                            "ram": "'$(awk -v min=1.25 -v max=50 -v seed="$RANDOM" 'BEGIN{srand(seed); printf "%.2f\n", min+rand()*(max-min)}')'",
                            "net": {
                              "in": "'${net_in}kB'",
                              "out": "'${net_out}kB'",
                              "adap_type": "free5gc-compose-321_privnet",
                              "map_ports": "8000/tcp"
                            },
                            "disk": "12.1kB"
                          },
                          "details": {
                            "name": "free5gc/udr",
                            "version": "v3.2.1"
                          }
                    },
                    "006": {
                          "id": "302f67ec0d31",
                          "name": "ausf",
                          "status": "up",
                          "resources": {
                            "cpu": "'$(awk -v min=1.25 -v max=20 -v seed="$RANDOM" 'BEGIN{srand(seed); printf "%.2f\n", min+rand()*(max-min)}')'",
                            "ram": "'$(awk -v min=1.25 -v max=50 -v seed="$RANDOM" 'BEGIN{srand(seed); printf "%.2f\n", min+rand()*(max-min)}')'",
                            "net": {
                              "in": "'${net_in}kB'",
                              "out": "'${net_out}kB'",
                              "adap_type": "free5gc-compose-321_privnet",
                              "map_ports": "8000/tcp"
                            },
                            "disk": "6.98kB"
                          },
                          "details": {
                            "name": "free5gc/ausf",
                            "version": "v3.2.1"
                          }
                    },
                    "007": {
                          "id": "2f55510e48ea",
                          "name": "smf",
                          "status": "up",
                          "resources": {
                            "cpu": "'$(awk -v min=1.25 -v max=20 -v seed="$RANDOM" 'BEGIN{srand(seed); printf "%.2f\n", min+rand()*(max-min)}')'",
                            "ram": "'$(awk -v min=1.25 -v max=50 -v seed="$RANDOM" 'BEGIN{srand(seed); printf "%.2f\n", min+rand()*(max-min)}')'",
                            "net": {
                              "in": "'${net_in}kB'",
                              "out": "'${net_out}kB'",
                              "adap_type": "free5gc-compose-321_privnet",
                              "map_ports": "8000/tcp"
                            },
                            "disk": "4.18kB"
                          },
                          "details": {
                            "name": "free5gc/smf",
                            "version": "v3.2.1"
                          }
                    },
                    "008": {
                          "id": "357f0d349069",
                          "name": "udm",
                          "status": "up",
                          "resources": {
                            "cpu": "'$(awk -v min=1.25 -v max=20 -v seed="$RANDOM" 'BEGIN{srand(seed); printf "%.2f\n", min+rand()*(max-min)}')'",
                            "ram": "'$(awk -v min=1.25 -v max=50 -v seed="$RANDOM" 'BEGIN{srand(seed); printf "%.2f\n", min+rand()*(max-min)}')'",
                            "net": {
                              "in": "'${net_in}kB'",
                              "out": "'${net_out}kB'",
                              "adap_type": "free5gc-compose-321_privnet",
                              "map_ports": "8000/tcp"
                            },
                            "disk": "11.3kB"
                          },
                          "details": {
                            "name": "free5gc/udm",
                            "version": "v3.2.1"
                          }
                    },
                    "009": {
                          "id": "bd1c035722fc",
                          "name": "pcf",
                          "status": "up",
                          "resources": {
                            "cpu": "'$(awk -v min=1.25 -v max=20 -v seed="$RANDOM" 'BEGIN{srand(seed); printf "%.2f\n", min+rand()*(max-min)}')'",
                            "ram": "'$(awk -v min=1.25 -v max=50 -v seed="$RANDOM" 'BEGIN{srand(seed); printf "%.2f\n", min+rand()*(max-min)}')'",
                            "net": {
                              "in": "'${net_in}kB'",
                              "out": "'${net_out}kB'",
                              "adap_type": "free5gc-compose-321_privnet",
                              "map_ports": "8000/tcp"
                            },
                            "disk": "6.51kB"
                          },
                          "details": {
                            "name": "free5gc/pcf",
                            "version": "v3.2.1"
                          }
                    },
                    "010": {
                          "id": "0d685933b5a9",
                          "name": "nrf",
                          "status": "up",
                          "resources": {
                            "cpu": "'$(awk -v min=1.25 -v max=20 -v seed="$RANDOM" 'BEGIN{srand(seed); printf "%.2f\n", min+rand()*(max-min)}')'",
                            "ram": "'$(awk -v min=1.25 -v max=50 -v seed="$RANDOM" 'BEGIN{srand(seed); printf "%.2f\n", min+rand()*(max-min)}')'",
                            "net": {
                              "in": "'${net_in}kB'",
                              "out": "'${net_out}kB'",
                              "adap_type": "free5gc-compose-321_privnet",
                              "map_ports": "8000/tcp"
                            },
                            "disk": "3.24kB"
                          },
                          "details": {
                            "name": "free5gc/nrf",
                            "version": "v3.2.1"
                          }
                    },
                    "011": {
                          "id": "51a0170365ce",
                          "name": "webui",
                          "status": "up",
                          "resources": {
                            "cpu": "'$(awk -v min=1.25 -v max=20 -v seed="$RANDOM" 'BEGIN{srand(seed); printf "%.2f\n", min+rand()*(max-min)}')'",
                            "ram": "'$(awk -v min=1.25 -v max=50 -v seed="$RANDOM" 'BEGIN{srand(seed); printf "%.2f\n", min+rand()*(max-min)}')'",
                            "net": {
                              "in": "'${net_in}kB'",
                              "out": "'${net_out}kB'",
                              "adap_type": "free5gc-compose-321_privnet",
                              "map_ports": "5000->5000/tcp"
                            },
                            "disk": "23.2kB"
                          },
                          "details": {
                            "name": "free5gc/webui",
                            "version": "v3.2.1"
                          }
                    },
                    "012": {
                          "id": "e8f1ac6987e7",
                          "name": "upf",
                          "status": "up",
                          "resources": {
                            "cpu": "'$(awk -v min=1.25 -v max=20 -v seed="$RANDOM" 'BEGIN{srand(seed); printf "%.2f\n", min+rand()*(max-min)}')'",
                            "ram": "'$(awk -v min=1.25 -v max=50 -v seed="$RANDOM" 'BEGIN{srand(seed); printf "%.2f\n", min+rand()*(max-min)}')'",
                            "net": {
                              "in": "'${net_in}kB'",
                              "out": "'${net_out}kB'",
                              "adap_type": "free5gc-compose-321_privnet",
                              "map_ports": "2152->2152/tcp, 2152->2152/udp "
                            },
                            "disk": "5.07kB"
                          },
                          "details": {
                            "name": "free5gc/upf",
                            "version": "20.04"
                          }
                    },
                    "013": {
                          "id": "8882a3af996e",
                          "name": "mongo",
                          "status": "up",
                          "resources": {
                            "cpu": "'$(awk -v min=1.25 -v max=20 -v seed="$RANDOM" 'BEGIN{srand(seed); printf "%.2f\n", min+rand()*(max-min)}')'",
                            "ram": "'$(awk -v min=1.25 -v max=50 -v seed="$RANDOM" 'BEGIN{srand(seed); printf "%.2f\n", min+rand()*(max-min)}')'",
                            "net": {
                              "in": "'${net_in}kB'",
                              "out": "'${net_out}kB'",
                              "adap_type": "free5gc-compose-321_privnet",
                              "map_ports": "27017/tcp"
                            },
                            "disk": "9.88kB"
                          },
                          "details": {
                            "name": "mongo",
                            "version": "latest"
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
        JSON_DATA_004='{
          "net_element": {
            "comm_channel": "PT2MANO",
            "timestamp": "'${NEW_TIMESTAMP}'",
            "flag_status": "1",
            "is_generic_hw": "true",
            "is_gateway": "false",
            "id": "network_element_004",
            "id_scenario": "caso_II",
            "agent_behavior_data": {
              "uuid": "caso_ii_004",
              "name": "data_network",
              "desc": "virtualmachine_004",
              "so": "ubuntu20.04",
              "disk": "25GB",
              "cpu": "2",
              "ram": "2GB",
              "virtualbox": {
                "vms": {
                  "name": "vmachine_data_network",
                  "status": "running",
                  "resources": {
                    "cpu": "2",
                    "ram": {
                      "used": "1.1",
                      "total": "2"
                    },
                    "disk": {
                      "used": "9",
                      "total": "25"
                    }
                  },
                  "config": {
                    "so": "ubuntu",
                    "version": "20.04",
                    "net": {
                      "ens3":{
                          "name": "ens3",
                          "status": "connected",
                          "ip_dir": "10.100.100.25",
                          "adapter_type": "internal",
                          "mapping_ports": ""
                       },
                      "ens10":{
                          "name": "ens10",
                          "status": "connected",
                          "ip_dir": "192.168.99.2",
                          "adapter_type": "internal",
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
                      "id": "09b701j6be1f",
                      "name": "server_VLC",
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
                        "disk": "543MB"
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


    for ((j=1; j<=4; j++)); do

        var_name="JSON_DATA_00$j"
        data="${!var_name}"

        # Generar el nombre del archivo
        filename=$(generate_filename "$var_name")

        # Crear el archivo JSON con los datos actuales
        echo "$data" > "$filename"

        echo -e "Archivo creado: $filename\n"
    done

#  curl -X POST "${BASE_URL}" -H 'Content-Type: application/json' -d "${JSON_DATA_001}"
#  curl -X POST "${BASE_URL}" -H 'Content-Type: application/json' -d "${JSON_DATA_002}"
#  curl -X POST "${BASE_URL}" -H 'Content-Type: application/json' -d "${JSON_DATA_003}"
#  curl -X POST "${BASE_URL}" -H 'Content-Type: application/json' -d "${JSON_DATA_004}"

done