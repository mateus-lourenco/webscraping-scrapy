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
        artista_sel = response.css('.h3 a')
        disc = artista_sel.css('::text').get()
        artista = {}
        if disc != None and disc.lower() == 'discografia':
            url = self.start_urls[0] + artista_sel.css('::attr(href)').get()
            artista['nome'] = response.css('.cnt-head_title h1 ::text').get()
            request = Request(
                        url=url, 
                        callback=self.albuns
                    )

            request.meta['artista'] = artista

            yield request

    def albuns(self, response):
        albuns = response.css('.cnt-discografia_cd')
        album_dic = {}
        for album in albuns:
            album_dic['titulo_album'] = album.css('.cnt-discografia_info a ::text').get()
            album_dic['ano'] = self.ano(album.css('.cnt-discografia_info span ::text').get())
            album_dic['titulo_musica'] = album.css('li:not([class^="contrib"]) span ::text').get()

            yield album_dic
            '''request = Request(
                url= self.start_urls[0] + album.css('li:not([class^="contrib"]) ::attr(href)').get(),
                callback= self.musicas
            )

            request.meta['artista']['album'] = album_dic

            yield request'''

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
    def ano(self, text):
        return re.match(r'.*([1-2][0-9]{3})', text).group(1)
