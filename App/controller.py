﻿"""
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
import prettytable
import config as cf
import model
from DISClib.ADT import list as lt
from DISClib.DataStructures import edge as e
from DISClib.ADT import map
from DISClib.Algorithms.Graphs.dfs import DepthFirstSearch
from DISClib.Algorithms.Graphs import scc 
import csv
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import graph as grph
from DISClib.ADT import orderedmap as om
import DISClib.DataStructures.rbt as rbt



"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def initcatalog():
    return model.newcatalog()

# Funciones para la carga de datos
def updatecitiesindices(catalog, cities_file):
    for city in cities_file:
        model.AddCityByName(catalog, city)

def loadcatalog(catalog, airports_file, routes_file, cities_file):
    addairports(catalog, airports_file)
    addroutes(catalog, routes_file)
    addauxindex(catalog)
    updatecitiesindices(catalog, cities_file)
    

def getfirstcity(cities_file):
    
    return next(cities_file)
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
    for airport in lt.iterator(vertices):
        adyacentes = grph.adjacents(catalog['Fullroutes'], airport)
        for vertexb in lt.iterator(adyacentes):
            peso = e.weight(grph.getEdge(catalog['Fullroutes'], airport, vertexb))
            if grph.getEdge(catalog['Fullroutes'], airport, vertexb):
                if grph.getEdge(catalog['Bothwaysroutes'], airport, vertexb) is None: #adyacenteb not in res:
                    grph.insertVertex(catalog['Bothwaysroutes'], airport)
                    grph.insertVertex(catalog['Bothwaysroutes'], vertexb)
                    grph.addEdge(catalog['Bothwaysroutes'], airport, vertexb, peso)
                    

#req 1

def MostConnected(graph):
    return model.MostConnected(graph)
def BuildMostConnectedTable(catalog, connectionsmap, top5):
    return model.BuildMostConnectedTable(catalog, connectionsmap, top5)
    
#req 2
#req 3
def BuildTable(catalog, city):
    if city != None:
        condition = model.BuildTable(catalog, city)
    else:
        condition = 'City not Found'
    return condition
#req 4
#req 5
def req5table(lista):
    table = prettytable.PrettyTable()
    table.field_names = ['IATA', 'Name', 'City', 'Country']
    for item in lt.iterator(lista):
        table.add_row([item['IATA'], item['Name'], item['City'], item['Country']])
    return table

def getbothwaysadj(catalog, cerrado):
    return model.getbothwaysadj(catalog, cerrado)

def getparaagregar(catalog, lista):
    return model.getparaagregar(catalog, lista)
#req 6
#req 7
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def getcomponents(graph):
    sc = scc.KosarajuSCC(graph)
    return scc.connectedComponents(sc)

def RSC(graph, verta, vertb):
    graphone = scc.KosarajuSCC(graph)
    return scc.stronglyConnected(graphone, verta, vertb)