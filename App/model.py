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
from prettytable import PrettyTable
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newcatalog():
    catalog = {'Fullroutes': None, 'Bothwaysroutes': None, 'airports':None, 'citiesIDindex':None, 'CityNameIndex': None, 'lnglatcityindex': None, 'latlngcityindex':None}
    catalog['Fullroutes'] = grph.newGraph(datastructure= 'ADJ_LIST', directed= True)
    catalog['Bothwaysroutes'] = grph.newGraph(directed= False)
    catalog['airports']= map.newMap(maptype= 'PROBING', loadfactor= 0.5) #mapa por el IATA de cada airport
    catalog['CityNameIndex'] = map.newMap(maptype= 'PROBING', loadfactor= 0.5)
    return catalog

# Funciones para agregar informacion al catalogo
def AddCityByName(catalog, city):
    if not map.contains(catalog['CityNameIndex'], str(city['city_ascii'])):
        newcitylist = lt.newList(datastructure='ARRAY_LIST', cmpfunction=None)
        lt.addLast(newcitylist, city)
        map.put(catalog['CityNameIndex'], str(city['city_ascii']), newcitylist)
    else:
        entry = map.get(catalog['CityNameIndex'], str(city['city_ascii']))
        citylist = me.getValue(entry)
        lt.addLast(citylist, city)

def addairport(catalog, airport):
    grph.insertVertex(catalog['Fullroutes'], airport["IATA"])
    map.put(catalog['airports'], airport['IATA'], airport)
    
def addroute(catalog, route):
    vertexa = route['Departure']
    vertexb = route['Destination']
    weight = route['distance_km']
    grph.addEdge(catalog['Fullroutes'], vertexa, vertexb, weight)

#req 1
#req 2
#req 3

def BuildTable(catalog, issue):
    counter = 0
    table=PrettyTable()
    table.field_names = ['Number', 'city', 'country' , 'state', 'longitude' , 'latitude']
    table.align='l'
    table._max_width= {'Number':4,'city':15 , 'country': 15, 'state':15, 'longitude':10, 'latitude':10}
    for item in lt.iterator(issue):
        table.add_row([counter, str(item['city']), str(item['country']),str(item['admin_name']), str(item['lng']), str(item['lat'])])
        counter += 1
    return table
    
#req 4
#req 5
#req 6
#req 7
# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
def cmpnumbers(uno, dos):
    if uno>dos:
        return 1
    else:
        return -1       
    