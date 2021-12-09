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
from typing import OrderedDict

from haversine import haversine
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import graph as grph
from DISClib.ADT import map 
from DISClib.Algorithms.Graphs.dfs import DepthFirstSearch
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
import DISClib.DataStructures.rbt as rbt
import DISClib.Algorithms.Graphs.dijsktra as djk
from prettytable import PrettyTable
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newcatalog():
    catalog = {'Fullroutes': None, 'Bothwaysroutes': None, 'airports':None, 'citiesIDindex':None, 'CityNameIndex': None,'CoordinatesTree':None, 'RoutesMap':None}
    catalog['Fullroutes'] = grph.newGraph(datastructure= 'ADJ_LIST', directed= True)
    catalog['Bothwaysroutes'] = grph.newGraph(datastructure = 'ADJ_LIST', directed= False)
    catalog['airports']= map.newMap(maptype= 'PROBING', loadfactor= 0.5) #mapa por el IATA de cada airport
    catalog['listairports'] = lt.newList(datastructure='ARRAY_LIST')
    catalog['CityNameIndex'] = map.newMap(maptype= 'PROBING', loadfactor= 0.5)
    catalog['CoordinatesTree'] = om.newMap(omaptype='RBT', comparefunction=CompareLatitudes)
    catalog['RoutesMap'] = map.newMap(maptype= 'PROBING', loadfactor= 0.5)
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
    lt.addLast(catalog['listairports'], airport)
    
def addroute(catalog, route):
    vertexa = route['Departure']
    vertexb = route['Destination']
    weight = float(route['distance_km'])
    grph.addEdge(catalog['Fullroutes'], vertexa, vertexb, weight)
    key = str(vertexa)+ ',' + str(vertexb) + ',' + str(weight)
    map.put(catalog['RoutesMap'], key, route['Airline'])

def updateLatitude(catalog, airport):
    '''Arbol cuyas llaves son latitudes y sus hojas son arboles cuyas llaves son longitudes'''
    latitude= str(airport['Latitude'])
    entry = om.get(catalog['CoordinatesTree'], latitude)
    longitudeIndex= {'longitude':None , 'IATA':None}
    longitudeIndex['longitude'] = airport['Longitude']
    longitudeIndex['IATA'] = airport['IATA']
    if entry is None:
        newlist = lt.newList(datastructure='ARRAY_LIST', cmpfunction=None)
        lt.addLast(newlist, longitudeIndex)
        om.put(catalog['CoordinatesTree'], latitude, newlist)
    else:
        oldlist = me.getValue(entry)
        lt.addLast(oldlist, longitudeIndex)

#req 1

def MostConnected(graph):
    connectionsmap = om.newMap(omaptype='RBT', comparefunction=CompareTotalDegrees)
    vertices = grph.vertices(graph)
    amountconnected = 0
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
        if dict['TotalDegree'] != '0':
            amountconnected += 1
    keys = om.keySet(connectionsmap)
    return amountconnected, keys, connectionsmap

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
            if counter == 5:
                break
        if counter == 5:
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

def Closest_To_Destiny(catalog, ciudad):
    lat = float(ciudad['lat'])
    lng = float(ciudad['lng'])
    upperlat = float(lat)
    lowerlat = float(lat)
    upperlng = float(lng)
    lowerlng = float(lng)
    airportstree = om.newMap(omaptype='RBT', comparefunction = CompareDistance)
    while om.size(airportstree) < 1:
        upperlat += 0.1
        lowerlat -= 0.1
        upperlng += 0.1
        lowerlng -= 0.1
        lat_in_range = om.keys(catalog['CoordinatesTree'],str(lowerlat), str(upperlat))
        for latitude in lt.iterator(lat_in_range):
            if lat_in_range is not None:
                entry = om.get(catalog['CoordinatesTree'], str(latitude))
                longitudeindex = me.getValue(entry)
                for airport in lt.iterator(longitudeindex):
                    IATAcode = airport['IATA']
                    if lowerlng < float(airport['longitude']) < upperlng:
                        city_coordinates = (lat,lng)
                        airport_coordinates = (float(latitude), float(airport['longitude']))
                        distance = haversine(city_coordinates, airport_coordinates)
                        if not om.contains(airportstree, str(distance)):
                            om.put(airportstree, str(distance), str(IATAcode))
    return airportstree

def Closest_Path(catalog, ciudadorigen, ciudaddestino):
    lat = float(ciudadorigen['lat'])
    lng = float(ciudadorigen['lng'])
    upperlat = float(lat)
    lowerlat = float(lat)
    upperlng = float(lng)
    lowerlng = float(lng)
    airportstree = om.newMap(omaptype='RBT', comparefunction=CompareDistance)
    destinytree = Closest_To_Destiny(catalog, ciudaddestino)
    closestdestiny = om.minKey(destinytree)
    entry = om.get(destinytree, str(closestdestiny))
    destinyIATA = me.getValue(entry)
    condition = True
    while condition:
        upperlat += 0.1
        lowerlat -= 0.1
        upperlng += 0.1
        lowerlng -= 0.1
        lat_in_range = om.keys(catalog['CoordinatesTree'],str(lowerlat), str(upperlat))
        if lat_in_range != None:
            for latitude in lt.iterator(lat_in_range):
                entry = om.get(catalog['CoordinatesTree'], str(latitude))
                longitudeindex = me.getValue(entry)
                for airport in lt.iterator(longitudeindex):
                    IATAcode = airport['IATA']
                    if lowerlng < float(airport['longitude']) < upperlng:
                            city_coordinates = (lat,lng)
                            airport_coordinates = (float(latitude), float(airport['longitude']))
                            distance = haversine(city_coordinates, airport_coordinates)
                            if not om.contains(airportstree, str(distance)):
                                om.put(airportstree, str(distance), str(IATAcode))
        keys = om.keySet(airportstree)
        for item in lt.iterator(keys):
            entry = om.get(airportstree, item)
            codigoIATA = me.getValue(entry)
            search = djk.Dijkstra(catalog['Fullroutes'], codigoIATA)
            if djk.hasPathTo(search, destinyIATA):
                origindict = OrderedDict()
                destinydict = OrderedDict()
                origindict['distance'] = item
                origindict['IATA'] = codigoIATA
                destinydict['distance'] = closestdestiny
                destinydict['IATA'] = destinyIATA
                minpath = djk.pathTo(search, destinyIATA)
                condition = False
    return origindict, destinydict, minpath

def Build_Tables_Req_5(catalog, dictionary):
    table=PrettyTable()
    table.field_names = ['IATA', 'Name', 'City' , 'Country']
    table.align='l'
    table._max_width= {'IATA':5, 'Name':30, 'City':15 , 'Country':15}
    IATAcode = dictionary['IATA']
    entry = map.get(catalog['airports'], IATAcode)
    airport = me.getValue(entry)
    table.add_row([IATAcode, airport['Name'], airport['City'], airport['Country']])
    return table

def Build_Path_Table(catalog, path):
    table=PrettyTable()
    table.field_names = ['Airline', 'Departure', 'Destination', 'distance_km']
    table.align='l'
    table._max_width= {'Airline':5, 'Departure':10, 'Destination':10, 'distance_km':10}
    weightsum = 0.0
    for item in lt.iterator(path):
        weight = item['weight']
        weightsum += float(weight)
        vertexA = item['vertexA']
        vertexB = item['vertexB']
        key = str(vertexA) + ',' + str(vertexB) + ',' + str(weight)
        airlineentry = map.get(catalog['RoutesMap'],key)
        airline = me.getValue(airlineentry)
        table.add_row([airline, vertexA, vertexB, weight])
    return weightsum, table

def StopsTable(catalog, stops):          
    table=PrettyTable()
    table.field_names = ['IATA', 'Name', 'City' , 'Country']
    table.align='l'
    table._max_width= {'IATA':5, 'Name':30, 'City':15 , 'Country':15}
    for item in lt.iterator(stops):
        vertexA = item['vertexA']
        entry = map.get(catalog['airports'], vertexA)
        airport = me.getValue(entry)
        table.add_row([airport['IATA'], airport['Name'], airport['City'], airport['Country']])
    lastvertex = lt.lastElement(stops)
    entry = map.get(catalog['airports'], lastvertex['vertexB'])
    last = me.getValue(entry)
    table.add_row([last['IATA'], last['Name'], last['City'], last['Country']])
    return table


    
#req 4

#req 5
def listaafectados(catalog,cerrado):
    arcos = grph.edges(catalog['Fullroutes'])
    newlist = lt.newList(datastructure='ARRAY_LIST')
    for item in lt.iterator(arcos):
        vertexA = str(item['vertexA'])
        vertexB = str(item['vertexB'])
        if vertexA == cerrado:
            if not lt.isPresent(newlist, vertexB):
                lt.addLast(newlist, vertexB)
        elif vertexB == cerrado:
            if not lt.isPresent(newlist, vertexA):
                lt.addLast(newlist, vertexA)
    return newlist

def req5table(catalog, lista):
    table = PrettyTable()
    table.field_names = ['IATA', 'Name', 'City', 'Country']
    for item in lt.iterator(lista):
        entry = map.get(catalog['airports'], str(item))
        airport = me.getValue(entry)
        table.add_row([airport['IATA'], airport['Name'], airport['City'], airport['Country']])
    return table
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
def CompareLatitudes(lat1, lat2):
    lat11=float(lat1)
    lat22=float(lat2)
    if (lat11 == lat22):
        return 0
    elif lat11 > lat22:
        return 1
    else:
        return -1
def CompareDistance(dist1, dist2):
    dist11=float(dist1)
    dist22=float(dist2)
    if (dist11 == dist22):
        return 0
    elif dist11 > dist22:
        return 1
    else:
        return -1