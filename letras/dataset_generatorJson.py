# -*- coding: utf-8 -*-

from pymongo import MongoClient
import json

client = MongoClient('mongodb://localhost:27017/')
db = client['letras_db']
musicas = db.musicas.find({})

with open('letras_bossanova.json', mode='w', encoding='utf-8') as json_file:
    count = 0
    for musica in musicas:

        try :
            compositor = musica['compositor'].split(':').pop()
        except:
            compositor = ''

        linha = {
            'genero' : musica['genero'],
            'artista' : musica['artista'],
            'album' : musica['album']['titulo_album'],
            'ano' : musica['album']['ano'],
            'titulo' : musica['titulo'],
            'compositor' : compositor.strip(),
            'letra' : musica['letra']
        },

        json.dump(linha, json_file, separators=(',', ':'), indent=2)
        count+=1
    print('{} letras foram capturadas'.format(count))