#Importa las librerías necesarias

import pandas as pd
import PlutoTVScrapping as plu
import time



# Toma el tiempo inicial
start_time = time.time()

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


metadata_episodes=[]



#Se recorre cada episodio de cada serie y se crea un diccionario con todos los datos
for serie in links_series:

    link_serie = plu.SerieLink(serie)


    for episode in link_serie.obtain_episodes():
    

        metadata_episodes += [{'serie':episode.serie,'episode':episode.episode,'episode_description':episode.episode_description,'season':episode.season}]

#Se crea el DataFrame final de episodios de series
metadata_episodes=pd.DataFrame(metadata_episodes)

metadata_episodes.to_csv("metadata_episodes.csv", index=False, sep=';') 


# Toma el tiempo final
end_time = time.time()

# Calcula el tiempo de ejecución
execution_time = end_time - start_time


print(f"El tiempo de ejecución fue: {execution_time} segundos") #Aprox 15 minutos //870 segundos

# Pausa la ejecución hasta que el usuario presione Enter
input("Presiona Enter para salir...")