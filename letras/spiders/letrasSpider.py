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
        request = Request(
            url=artistas_genero, 
            callback=self.todos_artistas
        )

        yield request

    def todos_artistas(self, response):
        todos_artistas = response.css('.cnt-list--col3 a')
        for artista in todos_artistas:
            url = self.start_urls[0] + artista.css('::attr(href)').get()
            request = Request(
                url=url, 
                callback=self.artistas_validos
            )

            yield request

    def artistas_validos(self, response):
        disc = response.css('.artista-albuns .cnt-more').get()
        if disc is not None:
            url = self.start_urls[0] + response.css('.h3 a ::attr(href)').get()
            nome = response.css('.cnt-head_title h1 ::text').get()
            
            request = Request(
                        url=url, 
                        callback=self.albuns
                    )

            request.meta['nome'] = nome
            yield request

    def albuns(self, response):
        albuns = response.css('.cnt-discografia_cd')                  
        album_dic = {}
        for album in albuns:
            url_musica = album.css('li:not([class^="contrib"]) ::attr(href)').get()
            album_dic = {
                    'nome': response.meta['nome'],
                    'album' : {   
                        'titulo_album' : album.css('.cnt-discografia_info a ::text').get(),
                        'ano' : self.ano(album.css('.cnt-discografia_info span ::text').get())                    }
                }
            request = Request(
                url=self.start_urls[0] + url_musica,
                callback=self.musicas
            )           
            request.meta['artista'] = album_dic

            yield request

    def musicas(self, response):
        trad = response.css('.letra-menu a ::attr(data-tt)').get()

        musica = {}
        if(trad is None):
            musica = {
                'artista': response.meta['artista']['nome'],
                'album': response.meta['artista']['album'],
                'titulo' : response.css('.cnt-head_title h1 ::text').get(),
                'compositor(es)' : response.css('.letra-info_comp ::text').get(),
                'letra' : ''.join(verso + '\r\n' for verso in response.css('div.cnt-letra p ::text').getall())
            }

            yield musica


    def ano(self, text):
        return re.match(r'.*([1-2][0-9]{3})', text).group(1)
