#Importa las librerías necesarias

import pandas as pd
import PlutoTVScrapping as plu
import time


# Toma el tiempo inicial
start_time = time.time()

#url de la sección on_demand con 'Películas' seleccionado, se define como objeto Link
link_on_demand= plu.Link(url='https://pluto.tv/latam/on-demand/618da9791add6600071d68b0?lang=en')

#Se usa el método obtain_List para obtener una lista de urls de categorías de películas
links_categories_movies= link_on_demand.obtain_list(string_contained='/latam/on-demand/618da9791add6600071d68b0/')

"""Creo un objeto Link para cada url de cada categoría,
uso de nuevo el método obtain_list para hallar una lista de urls de todas las películas"""

links_movies=[]

for link_category in links_categories_movies:

    link_category = plu.Link(url = link_category)

    links_movies += link_category.obtain_list(string_contained='/latam/on-demand/movies/', string_added='/details')
    
metadata_movies=[]

#Convierto cada url de película en un objeto MovieLink y uso el método obtain_movie para sacar su información

for link in links_movies:

    link= plu.MovieLink(url = link)

    movie = link.obtain_movie()

    metadata_movies += [{'title':movie.title,'description':movie.description,'rating':movie.rating,'genre':movie.genre,'duration':movie.duration,'url':movie.url}]


#Creo el DataFrame final de Películas
metadata_movies = pd.DataFrame(metadata_movies)

#Creo un objeto Link a partir de la url de la sección live
link_on_live=plu.Link(url='https://pluto.tv/latam/live-tv')

#Obtengo la lista de canales
links_channels= link_on_live.obtain_list(string_contained='/live-tv/', string_added='/details')

metadata_channels=[]

#Obtengo la información de cada canal utilizando el método obtain_channel

for link in links_channels:

    link= plu.ChannelLink(url = link)

    channel = link.obtain_channel()

    metadata_channels += [{'name':channel.title,'description':channel.description,'url':channel.url}]


#Creo el DataFrame final de los canales
metadata_channels = pd.DataFrame(metadata_channels)

#Objeto Link de on_demand con la opción 'series' seleccionada
link_on_demand=plu.Link('https://pluto.tv/latam/on-demand/619043246d03190008131b89?lang=en')

links__categories_series=[]

#Obtengo la lista de urls de categorías de series

links_categories_series = link_on_demand.obtain_list(string_contained='/latam/on-demand/619043246d03190008131b89')

links_series=[]

#Obtengo la lista de todas las urls que pertenecen a series

for link_category in links_categories_series:

    link_category = plu.Link(url = link_category)

    links_series += link_category.obtain_list(string_contained='/latam/on-demand/series/')

#Convierto cada url de serie en un objeto SerieLink y uso el método obtain_serie para sacar su información

metadata_series=[]

for link in links_series:

    link= plu.SerieLink(url = link)

    serie = link.obtain_serie()

    metadata_series += [{'title':serie.title,'description':serie.description,'rating':serie.rating,'genre':serie.genre,'url':serie.url}]

metadata_series= pd.DataFrame(metadata_series)

# Exporta los archivos .csv
metadata_movies.to_csv("metadata_movies.csv", index=False, sep=';')  


metadata_channels.to_csv("metadata_channels.csv", index=False, sep=';')  


metadata_series.to_csv("metadata_series.csv", index=False, sep=';')  


# Toma el tiempo final
end_time = time.time()

# Calcula el tiempo de ejecución
execution_time = end_time - start_time

print(f"El tiempo de ejecución fue: {execution_time} segundos") #Aprox 58 minutos //3481 segundos

# Pausa la ejecución hasta que el usuario presione Enter
input("Presiona Enter para salir...")