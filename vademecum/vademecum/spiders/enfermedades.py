# -*- coding: utf-8 -*-
import scrapy
from vademecum.items import EnfermedadItem


class EnfermedadesSpider(scrapy.Spider):
    name = 'enfermedades'
    allowed_domains = ['www.vademecum.es']
    start_urls = ['https://www.vademecum.es/enfermedades-a_1']
    letter_count = 98

    def parse(self, response):
        # Extrae la URL de cada enfermedad
        for href in response.xpath('//ul[@class="no-bullet"]/li/a'):
            yield response.follow(href, self.enfermedad)            
        # Cambiar la letra de inicio del listado de enfermedades
        if self.letter_count < 123:
            href = self.start_urls[0][:38] + chr(self.letter_count) + "_1"            
            self.letter_count+=1
            yield response.follow(href, self.parse)


    def enfermedad(self,response):
        enfermedad = EnfermedadItem()
        #Informacion de la enfermedad.
        enfermedad['nombre'] = response.xpath('//li[@class="current"]/a/text()').extract()[0].strip().replace("\u00A0", " ")       
        enfermedad['medicamentos'] = self.clean_array(response.xpath('//ul[@class="no-bullet"]/li/a/descendant::text()').extract())
        yield enfermedad

    def clean_array(self, array):
        # Quitar los \n \t 
        return list(filter(None, map(lambda s: s.strip().replace("\u00A0", " "), array)))