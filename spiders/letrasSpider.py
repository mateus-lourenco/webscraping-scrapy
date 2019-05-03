# -*- coding: utf-8 -*-
from scrapy import Request, Spider
import re

class LetrasspiderSpider(Spider):
    name = 'letrasSpider'
    allowed_domains = ['www.letras.mus.br']
    start_urls = [
        'https://www.letras.mus.br',
        'https://www.letras.mus.br/estilos/'
    ]
    estilo = ''

    def parse(self, response):
        genero = self.start_urls[1] + self.estilo
        artistas_genero = genero + '/todosartistas.html'
        req = Request(url=artistas_genero, callback=self.todos_artistas)
        yield req

    def todos_artistas(self, response):
        todos_artistas = response.xpath('.//li/a') 
        link = ''
        nome = ''
        for item in todos_artistas:
            nome = item.xpath('text()').get()
            link = self.start_urls[0] + item.xpath('@href').get() + 'discografia'

            album = Request(url=link, callback=self.albuns)
            
            yield {
                'artista' : {
                    'nome' : nome,
                    'album' : album
                }
            }

    def albuns(self, response):
        res = response.xpath('//*[@id="cnt_top"]/div[2]/div[3]/div[1]/div/div/div')
        albuns = res.xpath('./h4/a/text()').extract()
        lancamentos = res.xpath('./span/text()').extract()
        links_musica = res.xpath('../ol/li[not(contains(@class, "contrib"))]/a/@href')

        for titulo, ano, link in zip(albuns, lancamentos, links_musica):
            url = self.start_urls[0] + link
            musica = Request(url=url, callback=self.musicas)

            yield {
                'album' : {
                    'titulo' : titulo,
                    'ano' : ano,
                    'musicas' : musica
                }
            }

    def musicas(self, response):
        info_trad = response.css('div.letra-menu > a')
        trad = info_trad.xpath('./@data-tt')

        if(trad != 'Tradução'):
            info_titulo = response.css('div.cnt-head_title > h1')
            titulo = info_titulo.xpath('./text()').get()
            info_compositor = response.css('div.letra-info_comp')
            compositor = info_compositor.xpath('./text()').get()
            info_letra = response.css('div.cnt-letra > p')
            letra = ''.join(frase + '\r\n' for frase in info_letra.xpath('./text()').getall())

            yield {
                'titulo' : titulo,
                'compositor': compositor,
                'letra' : letra
            }
                     
        else:
            yield '' 
