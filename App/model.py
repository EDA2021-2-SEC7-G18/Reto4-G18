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
    catalog = {'Fullroutes': None, 'Bothwaysroutes': None, 'airports':None, 'citiesIDindex':None, 'CityNameIndex': None}
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

def MostConnected(graph):
    connectionsmap = om.newMap(omaptype='RBT', comparefunction=CompareTotalDegrees)
    vertices = grph.vertices(graph)
    for vertex in lt.iterator(vertices):
        dict = {'Name':None, 'indegree': None, 'outdegree': None, 'TotalDegree':None}
        dict['Name'] = str(vertex)
        dict['indegree'] = str(grph.indegree(graph,vertex))
        dict['outdegree'] = str(grph.outdegree(graph,vertex))
        dict['TotalDegree'] = str(int(dict['indegree']) + int(dict['outdegree']))
        if not om.contains(connectionsmap, dict['TotalDegree']):
            newlist = lt.newList(datastructure='ARRAY_LIST')
            lt.addLast(newlist, dict)
            om.put(connectionsmap, str(dict['TotalDegree']), newlist)
        else:
            entry = om.get(connectionsmap, dict['TotalDegree'])
            degreeslist = me.getValue(entry)
            lt.addLast(degreeslist, dict)
    keys = om.keySet(connectionsmap)
    return keys, connectionsmap

def BuildMostConnectedTable(catalog, connectionsmap, top5):
    table=PrettyTable()
    table.field_names = ['Name', 'City', 'Country' , 'IATA', 'connections' , 'Inbound', 'Outbound']
    table.align='l'
    table._max_width= {'Name':15, 'City':10 , 'Country': 15, 'IATA':5, 'Connections':5, 'Inbound':5, 'Outbound':5}
    counter = 0
    for item in lt.iterator(top5):
        entry2= om.get(connectionsmap, item)
        value2 = me.getValue(entry2)
        for element in lt.iterator(value2):
            counter += 1
            codigoIATA = str(element['Name'])
            entry = map.get(catalog['airports'], codigoIATA)
            value = me.getValue(entry)
            table.add_row([value['Name'], str(value['City']), str(value['Country']), codigoIATA,str(element['TotalDegree']), str(element['indegree']), str(element['outdegree'])])
            if counter >= 5:
                break
    return table

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
def CompareTotalDegrees(degree1, degree2)  :
    degree11=int(degree1)
    degree22=int(degree2)
    if (degree11 == degree22):
        return 0
    elif degree11 < degree22:
        return 1
    else:
        return -1  