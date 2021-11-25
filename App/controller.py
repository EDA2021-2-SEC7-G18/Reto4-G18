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
 """

from DISClib.DataStructures.chaininghashtable import rehash
import config as cf
import model
from DISClib.ADT import list as lt
from DISClib.DataStructures import edge as e
from DISClib.ADT import map
import csv
from DISClib.ADT import graph as grph


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def initcatalog():
    return model.newcatalog()

# Funciones para la carga de datos
def loadcatalog(catalog, airports_file, routes_file, cities_file):
    addairports(catalog, airports_file)
    addroutes(catalog, routes_file)
    addauxindex(catalog)
    updatecitiesindices(catalog, cities_file)
    

def getfirstcity(cities_file):
    
    return next(cities_file)
def updatecitiesindices(catalog, cities_file):
    for city in cities_file:
        model.addcity(catalog, city)
        model.lnglatcityindex(catalog, city)
        model.latlngcityindex(catalog, city)
def addauxindex(catalog):
    catalog['Fullroutesaux'] = catalog['Fullroutes']

def addairports(catalog, airports_file):
    for airport in airports_file:
        model.addairport(catalog, airport)

def addroutes(catalog, routes_file):
    for route in routes_file:
        model.addroute(catalog, route)

def Bothwaysroutes(catalog):
    vertices = grph.vertices(catalog['Fullroutes'])
    res=map.newMap()
    for airport in lt.iterator(vertices):
        adyacentes = grph.adjacents(catalog['Fullroutes'], airport)
        for vertexb in lt.iterator(adyacentes):
            peso = e.weight(grph.getEdge(catalog['Fullroutes'], airport, vertexb))
            adyacentesb = grph.adjacents(catalog['Fullroutes'], vertexb)
            for adyacenteb in lt.iterator(adyacentesb):
                if adyacenteb == airport:
                    #if not map.contains(res, adyacenteb): #adyacenteb not in res:
                        #print(verta, vertb, peso, 'siii')
                    grph.insertVertex(catalog['Bothwaysroutes'], airport)
                    grph.insertVertex(catalog['Bothwaysroutes'], vertexb)
                    grph.addEdge(catalog['Bothwaysroutes'], airport, vertexb, peso)
                    map.put(res, adyacenteb, '')
       
    
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
