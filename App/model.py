"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from sys import call_tracing
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import graph as grph
from DISClib.ADT import map 
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newcatalog():
    catalog = {'Fullroutes': None, 'Bothwaysroutes': None, 'airports':None, 'cities':None}
    catalog['Fullroutes'] = grph.newGraph(datastructure= 'ADJ_LIST', directed= True)
    catalog['Bothwaysroutes'] = grph.newGraph(directed= False)
    catalog['airports']= map.newMap() #mapa por el IATA de cada airport
    catalog['citiesIDindex'] = map.newMap() #mapa con keys el id de la ciudad
    #se crearan dos indices para ciudades. Uno de ellos es un mapa keys = city['lng']  con values= map(keys = lat y value = city)
    # el segundo indice de ciudades es la misma estructura pero esta vez el mapa latitudes contiene las longitudes 
    #los indices fueron construidos con el fin de encontrar cual sera la distancia entre coordenadas dadas y las de una ciudad mediate el uso  del teorema de pitagoras.
    #ejm: d = sq(lng2 + lat2)
    
    catalog['lnglatcityindex'] = om.newMap(omaptype= 'BST', comparefunction= cmpnumbers) #mapa keys = city['lng']  con values= otro mapa con keys = lat y value = city
    catalog['latlngcityindex'] = om.newMap(omaptype= 'BST', comparefunction= cmpnumbers)
    return catalog

# Funciones para agregar informacion al catalogo
def addcity(catalog, city):
    map.put(catalog['citiesIDindex'], city['id'], city)

def lnglatcityindex(catalog, city):
    lng = city['lng']
    lat = city['lat']
    if not om.contains(catalog['lnglatcityindex'],lng):
        latmap = om.newMap(omaptype= 'BST')
        om.put(latmap, lat, city)
        om.put(catalog['lnglatcityindex'], lng, latmap)
    else: 
        latmapentry = om.get(catalog['lnglatcityindex'], lng)
        latmap = me.getValue(latmapentry)
        om.put(latmap, lat, city)
        om.put(catalog['lnglatcityindex'], lng, latmap )

def latlngcityindex(catalog, city):
    lng = city['lng']
    lat = city['lat']
    if not om.contains(catalog['latlngcityindex'],lat):
        lngmap = om.newMap(omaptype= 'BST')
        om.put(lngmap, lng, city)
        om.put(catalog['latlngcityindex'], lat, lngmap)
    else: 
        lngmapentry = om.get(catalog['latlngcityindex'], lng)
        lngmap = me.getValue(lngmapentry)
        om.put(lngmap, lng, city)
        om.put(catalog['latlngcityindex'], lng, lngmap )

def addairport(catalog, airport):
    grph.insertVertex(catalog['Fullroutes'], airport["IATA"])
    map.put(catalog['airports'], airport['IATA'], airport)
    
def addroute(catalog, route):
    vertexa = route['Departure']
    vertexb = route['Destination']
    weight = route['distance_km']
    grph.addEdge(catalog['Fullroutes'], vertexa, vertexb, weight)
# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
def cmpnumbers(uno, dos):
    if uno>dos:
        return 1
    else:
        return -1       
    