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

import config as cf
import model
import csv
from DISClib.ADT import graph as grph


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def initcatalog():
    return model.newcatalog()

# Funciones para la carga de datos
def loadcatalog(catalog, airports_file, routes_file):
    addairports(catalog, airports_file)
    addroutes(catalog, routes_file)

def addairports(catalog, airports_file):
    for airport in airports_file:
        model.addairport(catalog, airport)

def addroutes(catalog, routes_file):
    for route in routes_file:
        model.addroute(catalog, route)

def Bothwaysroutes(catalog):
    vertices = grph.vertices(catalog['Fullroutes'])
    return vertices
    for airport in vertices:
        
        adyacentes = grph.adjacentEdges(catalog['Fullroutes'], airport)
    return adyacentes
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
