import requests
import json

URL = 'http://es01:9200'
size_pag = 10
size_aggs = 10

class SearcherConnection():
    __instance = None

    def __init__(self):
        if SearcherConnection.__instance != None:
            raise Exception("This class has been instantiated")
        else:
            SearcherConnection.__instance = self
            self.clean()

    @staticmethod 
    def getInstance():
        if SearcherConnection.__instance == None:
            SearcherConnection()
        return SearcherConnection.__instance
    
    def get_all_data(self):
        data = {}
        data['name'] = self.__name
        data['content'] = self.__content
        data['envases'] = self.__envases
        data['efect_adv'] = self.__efect_adv
        data['alertas_comp'] = self.__alertas_comp
        data['prin_act'] = self.__prin_act
        return data

    def get_actual_interval(self):
        if self.__index_pag + size_pag < self.__total_docs:
            interval = [self.__index_pag + 1, self.__index_pag + size_pag]
        elif self.__index_pag == self.__total_docs:
            interval = [self.__total_docs, self.__total_docs]
        else:
            interval = [self.__index_pag + 1, self.__total_docs]
        return interval
    
    def get_total_result(self):
        return self.__total_docs

    def get_aggs(self):
        return self.__aggs

    def clean(self):
        self.__index_pag = 0
        self.__total_docs = 0
        self.__name = ''
        self.__content = ''
        self.__envases = ''
        self.__efect_adv = ''
        self.__alertas_comp = []
        self.__prin_act = []
        self.__aggs = []

    def previous_page(self):
        if self.__index_pag - size_pag >= 0:
            self.__index_pag -= size_pag
        return self.__launch_query(self.__name, self.__content, self.__envases, self.__efect_adv, self.__alertas_comp, self.__prin_act, self.__index_pag) 

    def next_page(self):
        if self.__index_pag + size_pag < self.__total_docs:
            self.__index_pag += size_pag
        return self.__launch_query(self.__name, self.__content, self.__envases, self.__efect_adv, self.__alertas_comp, self.__prin_act, self.__index_pag)    
    
    def search(self, name, content, envases, efect_adv, alertas_comp):
        self.clean()
        self.__name = name
        self.__content = content        
        self.__envases = envases
        self.__efect_adv = efect_adv 
        self.__alertas_comp = alertas_comp
        return self.__launch_query(name, content, envases, efect_adv, alertas_comp)

    def aplicate_princ_act(self, prin_act):
        self.__index_pag = 0
        self.__total_docs = 0
        self.__prin_act = prin_act
        return self.__launch_query(self.__name, self.__content, self.__envases, self.__efect_adv, self.__alertas_comp, prin_act)
    
    def obtein(self, id):
        uri = URL + '/medicamentos/_doc/' + id
        response = requests.get(uri)
        results = json.loads(response.text)['_source']
        results['enfermedades'] = self.__get_enfermedades(results['nombre'])
        return  results
    
    def __get_enfermedades(self, name_med):
        query = {
            "_source": ["nombre"],
            "size": size_pag,
            "query": {
                "match": {
                    "medicamentos": name_med
                }      
            }
        }

        result_list = []
        index = 0
        stop = True        
        uri = URL + '/enfermedades/_search'
        # Se ejecuta la busqueda las veces necesarias para obtener todas las enfermedades
        while stop:
            query['from'] = index
            response = requests.get(uri, data=json.dumps(query), headers={"Content-Type":"application/json"})
            results = json.loads(response.text) 
            total_result = results['hits']['total']['value']              
            for item in results['hits']['hits']:
                result_list.append(item['_source']['nombre'].capitalize())

            if index + size_pag < total_result:
                index += size_pag
            else:
                stop = False

        return result_list


    def __launch_query(self, name, content, envases, efect_adv, alertas_comp, prin_act=[], from_query=0):
        # Query inicial incompleta
        query = {
            "_source": ["nombre"],
            "from": from_query,
            "size": size_pag,
            "query": { 
                "bool": { 
                    "should": [],
                    "filter": [],
                    "minimum_should_match" : 1
                }
            },
            "aggs":{
                "pa": {
                    "terms": {
                        "field": "principio_activo",
                        "size": size_aggs
                    }
                }
            } 
        }

        should = []
        # Se añade a la busqueda el valor en el campo nombre, si no es vacio
        if name != '':
            should.append({ "match": { "nombre": name}})
        # Se añade a la busqueda el valor en los campos considerados contenido, si no es vacio
        if content != '':
            should.append({ "multi_match": 
                {
                "query": content,
                "fields": ["definicion_uso", "antes_tomar", "como_tomar", "efectos_adversos", "conservacion", "info_adicional"]
                }
            })
        # Se añade a la busqueda el valor en el campo envases, si no es vacio
        if envases != '':
            should.append({ "match": { "envases": envases}})
        # Se añade a la busqueda el valor en el campo efectos_adversos, si no es vacio
        if efect_adv != '':
            should.append({ "match": { "efectos_adversos": efect_adv}})
        # Se añaden los filtro por alerta y principios activo seleccionados
        filters = []
        for alerta in alertas_comp:
            filters.append({ "term":  { "alertas_composicion": alerta }})    
        
        for pa in prin_act:
            filters.append({ "term":  { "principio_activo": pa }})    
        
        query['query']['bool']['should'] = should
        query['query']['bool']['filter'] = filters

        # Se ejecuta la busqueda
        uri = URL + '/medicamentos/_search'
        response = requests.get(uri, data=json.dumps(query), headers={"Content-Type":"application/json"})
        results = json.loads(response.text)
        self.__total_docs = results['hits']['total']['value']
        self.__aggs = results['aggregations']['pa']['buckets']
        
        result_list = []
        for item in results['hits']['hits']:
            result_list.append(item)
        return result_list
