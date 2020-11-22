# RIWS Mario y Alejo
* Importante descomprimir vademecumJSON.zip este archivo contiene los JSON comprimidos por motivos de espacio en Git
* Si no va docker leer Instalacion.txt

RIWS/
    vademecum/
    flask/
    Elastic/
    docker-compose.yml
    Dockerfile
    entrypoint.sh
    requirements.txt

Como podemos ver en la estructura, se diferencian varias carpetas. En la carpeta Vademecun nos encontramos con todo lo necesario para la ejecución del Crawler. En la carpeta Elastic, lo necesario para crear los índices y añadir los documentos en Elastic y por último Flask, donde tenemos nuestra aplicación web. El resto de ficheros van a ser necesarios para la ejecución del contenedor de Docker.

Scrapy

vademecum/
    vademecum/
        spiders/
            __init__.py
            enfermedades.py
            medicamentos.py
        __init__.py
        items.py
        middlewares.py
        pipelines.py
        runner.py
        settings.py
    enfermedades.json
    medicamentos.json
    scrapy.conf
	
Para poder ejecutar el Crawler, tenemos que tener instalado previamente Scrapy, utilizando el siguiente comando:

pip install Scrapy


Nosotros utilizamos la versión 2.1.0. También utilizamos la librería JSON para obtener los datos del crawler en formato JSON.

Tenemos dos spiders, medicamentos y enfermedades, que nos van a permitir crawler la página web. Para ello utilizamos los siguientes comandos:

scrapy crawl medicamentos
scrapy crawl enfermedades

Este comando hay que realizarlo dentro de la carpeta Vademecum.


Observaciones

Se puede crawlear en cualquier momento y las veces que sea necesario, pero hay que tener en cuenta que crawlear medicamentos puede llevar hasta 2 horas ya que tiene mucho contenido.


Elastic y Flask con Docker
Para disminuir todo tipo de errores de dependencias y versiones a la hora de instalar Elastic o Flask, se ha utilizado Docker para ocultar toda la instalación y así asegurar la portabilidad de la aplicación. Para ello, se ha utilizado docker-compose, que nos permite levantar varios contenedores a la vez con diferentes configuraciones.

Por lo tanto, una vez ejecutado el crawler y obtenidos los ficheros JSON, el siguiente paso el ejecutar los contenedores tanto de Elastic como de Flask. Desde la raíz del proyecto, ejecutamos el siguinte comando:

docker-compose up --build 


Una vez se hayan levantado correctamente los contenedores, el siguiente paso es crear los índices y volcar los datos en ellos. Para ello necesitamos tener una serie de módulos cargados:

apt get install python3-pip
pip3 install elasticsearch


Elastic/
    createindex.py
    
Después de ejecutar esos comandos, dentro de la carpeta Elastic, se ejecutará el siguiente comando:

python3 createindex.py

Una vez realizados todos esos comandos, ya se podrá utilizar la interfaz web entrando en 0.0.0.0:5000 o 127.0.0.1:5000 en el navegador.

Dependiendo de las versiones de Docker y de la máquina local, puede haber algunos errores a la hora de levantar los contenedores. Si es así, es necesario ejecutar el siguiente comando:

sysctl -w vm.max_map_count=262144


