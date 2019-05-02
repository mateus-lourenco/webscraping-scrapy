# -*- coding: utf-8 -*-
import scrapy
import re

class LetrasspiderSpider(scrapy.Spider):
    name = 'letrasSpider'
    allowed_domains = ['www.letras.mus.br']
    start_urls = [
        'https://www.letras.mus.br',
        'https://www.letras.mus.br/estilos/'
        ] 

    def parse(self, response):
        genero = self.start_urls[1] + self.estilo
        artistas_genero = genero + '/todosartistas.html'
        req = scrapy.Request(url=artistas_genero, callback=self.todos_artistas)
        yield req

    def todos_artistas(self, response):
        todos_artistas = response.xpath('.//li/a') 
        link = ''
        nome = ''
        for item in todos_artistas:
            nome = item.xpath('text()').extract_first()
            link = self.start_urls[0] + item.xpath('@href').extract_first() + 'discografia'

            album = scrapy.Request(url=link, callback=self.albuns)
            
            yield {
                'artista' : {
                    'nome' : nome,
                    'link' : link,
                    'album' : album
                }
            }

    def albuns(self, response):
        res = response.xpath('//*[@id="cnt_top"]/div[2]/div[3]/div[1]/div/div/div')
        albuns = res.xpath('./h4/a/text()').extract()
        lancamentos = res.xpath('./span/text()').extract()
        musicas = res.xpath('../ol/li[not(contains(@class, "contrib"))]/a/@href')

        for titulo, ano, musica in zip(albuns, lancamentos, musicas):
            url = self.start_urls[0] + musica
            req = scrapy.Request(url=url, callback=self.musicas)

            yield {
                'album' : {
                    'titulo' : titulo,
                    'ano' : ano,
                    'musicas' : req
                }
            }

    def musicas(self, response):
        pass