#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os, json
from elasticsearch import Elasticsearch, helpers

ELASTIC_URL = 'localhost:9200'

# Configuracion del analizador del indexer
mapping = {
        "settings": {
            "analysis": {
				"filter": {
					"spanish_stop": {
					  "type":       "stop",
					  "stopwords":  "_spanish_" 
					},
				},
                "analyzer": {
                    "customAnalyzer": {
                        "tokenizer": "standard",
                        "filter":[
                            "lowercase",
							"spanish_stop"
                        ]
                    }
                }
            }
        },
        "mappings": {
            "properties": {}
        }
    }

# Campos del indice medicamentos
medicamentos = {        
    "nombre": {
        "type": "text",
        "fields": {
            "analyzed": {
                "type": "text",
                "analyzer": "customAnalyzer",
                "search_analyzer": "customAnalyzer"
                }
            }
    },
    "alertas_composicion": {
        "type": "keyword",
        "fields": {
            "analyzed": {
				"type": "text",
				"analyzer": "customAnalyzer",
				"search_analyzer": "customAnalyzer"
            }
        }
    },
    "principio_activo": {
        "type": "keyword",
        "fields": {
            "analyzed": {
                "type": "text",
                "analyzer": "customAnalyzer",
                "search_analyzer": "customAnalyzer"
                }
            }
    },
    "envases": {
        "type": "text",
        "fields": {
            "analyzed": {
                "type": "text",
                "analyzer": "customAnalyzer",
                "search_analyzer": "customAnalyzer"
                }
            }
    },
    "definicion_uso": {
        "type": "text",
        "fields": {
            "analyzed": {
                "type": "text",
                "analyzer": "customAnalyzer",
                "search_analyzer": "customAnalyzer"
                }
            }
    },
    "antes_tomar": {
        "type": "text",
        "fields": {
            "analyzed": {
                "type": "text",
                "analyzer": "customAnalyzer",
                "search_analyzer": "customAnalyzer"
                }
            }
    },
    "como_tomar": {
        "type": "text",
        "fields": {
            "analyzed": {
                "type": "text",
                "analyzer": "customAnalyzer",
                "search_analyzer": "customAnalyzer"
                }
            }
    },
    "efectos_adversos": {
        "type": "text",
        "fields": {
            "analyzed": {
                "type": "text",
                "analyzer": "customAnalyzer",
                "search_analyzer": "customAnalyzer"
                }
            }
    },
    "conservacion": {
        "type": "text",
        "fields": {
            "analyzed": {
                "type": "text",
                "analyzer": "customAnalyzer",
                "search_analyzer": "customAnalyzer"
                }
            }
    },
    "info_adicional": {
        "type": "text",
        "fields": {
            "analyzed": {
                "type": "text",
                "analyzer": "customAnalyzer",
                "search_analyzer": "customAnalyzer"
                }
            }
    }
}

# Campo del indice enfermedades
enfermedades = {
    "nombre": {
        "type": "text",
        "fields": {
            "analyzed": {
                "type": "text",
                "analyzer": "customAnalyzer",
                "search_analyzer": "customAnalyzer"
                }
            }
    },
    "medicamentos": {
        "type": "keyword",
        "fields": {
            "analyzed": {
            "type": "text",
            "analyzer": "customAnalyzer",
            "search_analyzer": "customAnalyzer"
            }
        }
    }
}


def get_path_so():
    path = os.path.dirname(os.path.realpath(__file__))
    if os.name == 'posix': # posix si es Mac o Linux
        path = path + "/"
    else:
        path = path + chr(92) # si es Windows añadimos una barra invertida
    return path


def dump_json_data(index_name, path_json, path=get_path_so()):
    # Se abre el achivo .json
    with open(path + path_json, encoding="utf8", errors='ignore') as file:
        # Conversion a un diccionario
        json_list = json.load(file)
        
        id = 1
        for item in json_list:      
            yield {
                "_index": index_name,
                "_id": id,
                "_source": item,
            }        
            id += 1


def index(index_name):
    
    # Conexion con elastic
    elastic = Elasticsearch(ELASTIC_URL)

    # Segun el nombre del indice se escoje su estructura
    if index_name == "enfermedades":
        mapping['mappings']['properties'] = enfermedades
    else:
        mapping['mappings']['properties'] = medicamentos

    # Obtencion de la ruta del archivo .json
    datapath = '../vademecum/{}.json'.format(index_name)
    if(not os.path.exists(get_path_so() + datapath)):
        print("No se ha encontrado {}.json, el indice no se creo.".format(index_name))
        return False

    # Creacion del indice y eliminacion si existe
    if elastic.indices.exists(index=index_name): #doc_type='enfermedades'
        elastic.indices.delete(index=index_name, ignore=[400, 404])
    elastic.indices.create(index=index_name, body=mapping)
    print('Se ha creado el indice: ' + index_name)
    
    # Se vuelcan los documentos del .json a elastic 
    response = helpers.bulk(elastic, dump_json_data(index_name, datapath))
    print ("Bulk Response:", response)

    return True

index("enfermedades")
index("medicamentos")