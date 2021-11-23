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


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import graph as grph
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newcatalog():
    catalog = {'Fullroutes': None, 'Bothwaysroutes': None, 'Fullroutesaux':None}
    catalog['Fullroutes'] = grph.newGraph(datastructure= 'ADJ_LIST', directed= True)
    catalog['Bothwaysroutes'] = grph.newGraph(directed= False)
    return catalog

# Funciones para agregar informacion al catalogo
def addairport(catalog, airport):
    grph.insertVertex(catalog['Fullroutes'], airport["IATA"])

def addroute(catalog, route):
    vertexa = route['Departure']
    vertexb = route['Destination']
    weight = route['distance_km']
    grph.addEdge(catalog['Fullroutes'], vertexa, vertexb, weight)
# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
