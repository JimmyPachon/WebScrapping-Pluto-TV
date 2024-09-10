#Importa las librerías necesarias

import requests
from bs4 import BeautifulSoup


#Elimina duplicados de una lista
def delete_duplicates(element):

    return list(set(element))

#Crea el objeto soup para analizar el HTML dada una url

def obtain_soup_object(url):

      
        response = requests.get(url)
        
     
        soup = BeautifulSoup(response.text, 'html.parser')

        return soup


# Clase creada para almacenar datos de películas
class Movie:

    def __init__(self,title,description,rating,genre,duration,url):

        self.title = title
        self.description = description
        self.rating = rating
        self.genre = genre
        self.duration = duration
        self.url = url 

# Clase creada para almacenar datos de series
class Serie:

    def __init__(self,title,description,rating,genre,url):

        self.title = title
        self.description = description
        self.rating = rating
        self.genre = genre
        self.url = url 

#Clase creada para almacenar datos de canales


class Channel:

    def __init__(self,title,description,url):

        self.title = title
        self.description = description
        self.url = url

    
#Defino el objeto 'link'

class Link:

    # Defino las propiedades de link, su url y su desglose con Beautifulsoup
    def __init__(self, url):

        self.url = url  # Atributo de la instancia
        self.soup = obtain_soup_object(self.url)


    #Obtiene la lista de urls dentro de soup que contienen determinada cadena y se puede añadir una al final

    def obtain_list(self, string_contained, string_added=''):


        # Es la lista que va a contener todas las url requeridas
        links_requireds = []

        # Encuentra todos los href dentro de los elementos <a> y filtra los que contienen la cadena string_contained
        for a in self.soup.find_all('a', href=True):

            href = a['href']  # Obtiene el href del elemento <a>

            if string_contained in href:  

                # Agrego la cadena 'https://pluto.tv' al inicio del href para tener la url completa y adiciono string_added al final
                link = 'https://pluto.tv' + href + string_added

                links_requireds.append(link)

        return delete_duplicates(links_requireds)
    

# Defino la clase MovieLink para tratar la url de películas
class MovieLink:
    
    def __init__(self, url):
        
        self.url = url  
        self.soup = obtain_soup_object(self.url)
        

    #Dada la url me devuelve un objeto de clase Movie
    def obtain_movie(self):


        # Busca el div con la clase 'inner'
        inner_div = self.soup.find('div', class_='inner')
        
        if inner_div:

            # Obtiene el nombre de la película
            h1_name = inner_div.find('h1')
            title = h1_name['title'] if h1_name and 'title' in h1_name.attrs else "Atributo 'title' no encontrado"
            
            # Obtiene la descripción de la película
            first_div = inner_div.find('div')
            description = first_div.get_text(strip=True) if first_div else "Contenido no encontrado"
            
            # Obtiene la clasificación, el género y la duración de la película
            li_elements = inner_div.find_all('li')
            rating= li_elements[0].get_text(strip=True)
            genre= li_elements[2].get_text(strip=True)
            duration = li_elements[4].get_text(strip=True) 
            
            return Movie(title,description,rating, genre,duration,self.url)
        else:
            return {"error": "No se encontró el <div> con la clase 'inner'"}
        

#Defino una clase ChannelLink para tratar las url de canales
class ChannelLink:

    def __init__(self, url):
        
        self.url = url 
        self.soup = obtain_soup_object(self.url)

    #Dada una url me devuelve un objeto de clase Channel
    def obtain_channel(self):


        # Busca el div con la clase 'inner'
        inner_div = self.soup.find('div', class_='inner')
        
        if inner_div:
            # Obtiene el nombre del canal
            h2_name = inner_div.find('h2')
            title = h2_name['title'] if h2_name and 'title' in h2_name.attrs else "Atributo 'title' no encontrado"
            
            #Halla la descripcion del canal
            div_elements = inner_div.find_all('div')
            description = div_elements[1].get_text(strip=True)
            
            
            return Channel(title, description, self.url)
        else:
            return {"error": "No se encontró el <div> con la clase 'inner'"}

#Defino la clase Episode para almacenar la información
class Episode:

    def __init__(self,serie,episode,episode_description, season):

        self.serie = serie
        self.episode = episode
        self.episode_description = episode_description
        self.season = season
        
# Defino la clase SerieLink
class SerieLink:
    
    def __init__(self, url):
        
        self.url = url  

    def obtain_serie(self):

        soup = obtain_soup_object(self.url)
        
        # Busca el div con la clase 'inner'
        inner_div = soup.find('div', class_='inner')
       
        
        if inner_div:
            
            # Obtiene el nombre de la serie
            first_h1= inner_div.find('h1')
            title = first_h1.get_text(strip=True) if first_h1 else "Contenido no encontrado"
            
            # Obtiene el la clasificación y el género
            li_elements = inner_div.find_all('li')
            rating= li_elements[0].get_text(strip=True)
            genre= li_elements[2].get_text(strip=True)
            

            #Obtiene la descripción de la serie
            first_div = inner_div.find('p')
            description = first_div.get_text(strip=True) if first_div else "Contenido no encontrado"
            
            return Serie(title,description,rating,genre,self.url)
        else:
            return {"error": "No se encontró el <div> con la clase 'inner'"}

        
        
    # Obtiene la lista de episodios a partir de una url de una serie
    def obtain_episodes(self):

        #Se inicializa la temporada
        season = 1

        episodes = [] #Almacena los objetos Episode


        season_break=set() #Se usa para romper el bucle cuando se acaben las temporadas

        while True:

            try:

                #Si se llega a la última temporada se rompe el bucle
                if(season in season_break):


                    return episodes
                
                else:

                    season_break.add(season)
                
                # Es la url que tiene en cuenta los cambios de temporada
                link = self.url + '/season/' + str(season)
                
                
                soup = obtain_soup_object(link)

                

                # Busca el div con la clase 'inner'
                inner_div = soup.find('div', class_='inner')

            

                if inner_div:

                    # Obtiene el nombre de la serie
                    title = inner_div.find('h1')
                    
                    serie = title.get_text(strip=True)

                    # Busca todas las secciones <section class="episode-details"> dentro de inner_div
                    episode_sections = inner_div.find_all('section', class_='episode-details')

                    

                    for episodio in episode_sections:

                        
                        # Extrae el nombre del episodio 
                        episode = episodio.find('h4').text if episodio.find('h4') else None

                        # Extrae la sinopsis del episodio
                        description = episodio.find('p').text if episodio.find('p') else None

                        # Crea el objeto Episode y lo añade a una lista
                        episodes.append(Episode(serie, episode, description, season))

                        
                        

                    #Una vez recorridos todos los episodios, se avanza a la siguiente temporada
                    season+=1

                    

            
            except :
                
                break

