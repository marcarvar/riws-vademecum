import os
from scrapy.cmdline import execute

os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Ejecutar este archivo cuando se quiera depurar el codigo

try:
    execute(
        [  
            'scrapy',
            'crawl',
            'medicamentos',
            #'enfermedades',
        ]
    )
except SystemExit:
    pass