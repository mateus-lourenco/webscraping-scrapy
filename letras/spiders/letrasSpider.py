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
        todos_artistas = response.css('.cnt-list--col3 a')
        artista = {}
        for item in todos_artistas:
            nome = item.xpath('text()').get()
            link = self.start_urls[0] + item.css('::attr(href)').get()

            req = Request(url=link, callback=self.disc_parse)
            artista['nome'] = nome
            req.meta['artista'] = artista
            yield req

    def disc_parse(self, response):
        disc = self.start_urls[0] + response.css('.h3 a ::attr(href)').get()
        yield {
            Request(url=disc, callback=self.albuns)
        }

    def albuns(self, response):
        albuns = response.css('.cnt-discografia_cd')
        lancamentos = albuns.xpath('./span/text()').extract_first()
        links_musica = albuns.xpath('../ol/li[not(contains(@class, "contrib"))]/a/@href')

        yield { 
            'albuns' : albuns,
            'lancamentos' : lancamentos
        }

        album = {}

        for titulo, ano, link in zip(albuns, lancamentos, links_musica):
            url = self.start_urls[0] + link
            req = Request(url=url, callback=self.musicas)

            album['titulo'] = titulo
            album['ano'] = ano

            req.meta['album'] = album

            yield req

    '''def musicas(self, response):
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

            '''
