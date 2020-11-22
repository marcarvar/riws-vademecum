# -*- coding: utf-8 -*-
import scrapy
from vademecum.items import MedicamentoItem

class MedicamentosSpider(scrapy.Spider):
    name = 'medicamentos'
    allowed_domains = ['www.vademecum.es']
    start_urls = ['https://www.vademecum.es/medicamentos-a_1']
    letter_count = 98

    def parse(self, response):
        # Extrae la URL de cada medicamento
        for href in response.xpath('//ul[@class="no-bullet"]/li/a'):
            yield response.follow(href, self.medicamento)       #Aqui el href es un selector
            
        # Cambiar la letra de inicio del listado de medicamentos
        if self.letter_count < 123:
            href = self.start_urls[0][:38] + chr(self.letter_count) + "_1"
            self.letter_count+=1
            yield response.follow(href, self.parse)


    def medicamento(self,response):
        href_prospecto = response.xpath('//a[@id="mM_2"]/@href').extract() 
        # Si no tiene prospecto solo se quitan estos datos
        if not href_prospecto:
            medicamento = MedicamentoItem()
            #Informacion del medicamento.
            medicamento['nombre'] = response.xpath('//h1/span/text()').extract()[0]       
            medicamento['alertas_composicion'] = self.clean_array(response.xpath('//div[@class="large-12 medium-12 small-12 columns"]/dl/dd/a/text()').extract())
            medicamento['principio_activo'] = self.clean_array(response.xpath('(//td[@class="laboratorioTxt"])[2]/a/strong/text()').extract())
            medicamento['envases'] = self.clean_array(response.xpath('//li[@class="title"]/text()').extract())
            medicamento['definicion_uso'] = ""
            medicamento['antes_tomar'] = ""
            medicamento['como_tomar'] = ""
            medicamento['efectos_adversos'] = ""
            medicamento['conservacion'] = ""
            medicamento['info_adicional'] = ""
            yield medicamento
        else:
            href = self.start_urls[0][:24] + href_prospecto[0]        #link del prospecto    
            yield response.follow(href, self.parse_prospecto)
            
        
    def parse_prospecto(self, response):
        medicamento = MedicamentoItem()
        #Informacion del medicamento.
        medicamento['nombre'] = response.xpath('//h1/span/text()').extract()[0]        
        medicamento['alertas_composicion'] = self.clean_array(response.xpath('//div[@class="large-12 medium-12 small-12 columns"]/dl/dd/a/text()').extract())
        medicamento['principio_activo'] = self.clean_array(response.xpath('(//td[@class="laboratorioTxt"])[2]/a/strong/text()').extract())
        medicamento['envases'] = self.clean_array(response.xpath('//li[@class="title"]/text()').extract())         
        medicamento['definicion_uso'] = " ".join(self.clean_array(response.xpath('//div[@class="bodytext3"]/div[2]/descendant::text()').extract())) 
        medicamento['antes_tomar'] = " ".join(self.clean_array(response.xpath('//div[@class="bodytext3"]/div[3]/descendant::text()').extract()))
        medicamento['como_tomar'] = " ".join(self.clean_array(response.xpath('//div[@class="bodytext3"]/div[4]/descendant::text()').extract()))
        medicamento['efectos_adversos'] = " ".join(self.clean_array(response.xpath('//div[@class="bodytext3"]/div[5]/descendant::text()').extract()))
        medicamento['conservacion'] = " ".join(self.clean_array(response.xpath('//div[@class="bodytext3"]/div[6]/descendant::text()').extract()))
        medicamento['info_adicional'] = " ".join(self.clean_array(response.xpath('//div[@class="bodytext3"]/div[7]/descendant::text()').extract()))
        yield medicamento

    def clean_array(self, array):
        # Quitar los \n \t 
        return list(filter(None, map(lambda s: s.strip(), array)))
    