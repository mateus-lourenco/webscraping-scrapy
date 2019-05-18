# -*- coding: utf-8 -*-
from scrapy import Request, Spider
from letras.items import Genero
import re

class LetrasSpider(Spider):
    name = 'letrasSpider'
    allowed_domains = ['www.letras.mus.br']
    start_urls = [
        'https://www.letras.mus.br',
        'https://www.letras.mus.br/estilos/'
    ]

    def parse(self, response):
        url_genero = self.start_urls[1] + self.estilo
        artistas_genero = url_genero + '/todosartistas.html'
        request = Request(
            url=artistas_genero, 
            callback=self.parse_artista
        )

        yield request

    def parse_artista(self, response):
        todos_artistas = response.css('.cnt-list--col3 a')
        for artista in todos_artistas:
            url = self.start_urls[0] + artista.css('::attr(href)').get()
            request = Request(
                url=url, 
                callback=self.parse_artista_valido
            )

            yield request

    def parse_artista_valido(self, response):
        disc = response.css('.artista-albuns .cnt-more').get()
        if disc is not None:
            url = self.start_urls[0] + response.css('.h3 a ::attr(href)').get()
            nome = response.css('.cnt-head_title h1 ::text').get()
            
            request = Request(
                        url=url, 
                        callback=self.parse_album
                    )

            request.meta['nome'] = nome
            yield request

    def parse_album(self, response):
        albuns_info = response.css('.cnt-discografia_cd')
        album_dic = {}
        for info in albuns_info:
            urls_musica = info.css('li:not([class^="contrib"]) ::attr(href)').getall()
            album_dic = {
                'nome': response.meta['nome'],
                'album' : {   
                   'titulo_album' : info.css('.cnt-discografia_info a ::text').get(),
                   'ano' : info.css('.cnt-discografia_info span ::text').re(r'.*([1-2][0-9]{3})')[0]
                }
            }
            
            for url in urls_musica:
                request = Request(
                    url=self.start_urls[0] + url,
                    callback=self.parse_musica
                )

                request.meta['artista'] = album_dic

                yield request

    def parse_musica(self, response):
        trad = response.css('.letra-menu a ::attr(data-tt)').get()

        genero = {}
        if(trad is None):
            genero = {
                'genero' : self.estilo,
                'artista': response.meta['artista']['nome'],
                'album': response.meta['artista']['album'],
                'titulo' : response.css('.cnt-head_title h1 ::text').get(),
                'compositor' : response.css('.letra-info_comp ::text').get(),
                'letra' : ''.join(verso + '\n' for verso in response.css('div.cnt-letra p ::text').getall())
            }

            yield Genero(genero)