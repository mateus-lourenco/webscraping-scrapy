# -*- coding: utf-8 -*-

from pymongo import MongoClient
import csv

client = MongoClient('mongodb://localhost:27017/')
db = client['letras_db']
musicas = db.musicas.find({})

with open('letras_dataset2.csv', mode='w', encoding='utf-8') as csv_file:
    campos = ['genero','artista','album','ano', 'titulo', 'compositor', 'letra']
    writer = csv.DictWriter(csv_file, fieldnames=campos, delimiter=';')
    writer.writeheader()


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
        }
        
        writer.writerow(linha)