# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MedicamentoItem(scrapy.Item):
    # define the fields for your item here like:
    nombre = scrapy.Field()
    alertas_composicion = scrapy.Field()
    principio_activo = scrapy.Field()
    envases = scrapy.Field()
    definicion_uso = scrapy.Field()
    antes_tomar = scrapy.Field()
    como_tomar = scrapy.Field()
    efectos_adversos = scrapy.Field()
    conservacion = scrapy.Field()
    info_adicional = scrapy.Field() 

class EnfermedadItem(scrapy.Item):
    # define the fields for your item here like:
    nombre = scrapy.Field()
    medicamentos = scrapy.Field() 