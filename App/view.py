"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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

#rom App.model import addairport
import model
import config as cf
import sys
import controller
import csv
from DISClib.ADT import list as lt
assert cf
import time
from DISClib.ADT import graph as grph
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map 
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs.bfs import BreadhtFisrtSearch
from haversine import haversine
"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
sys.setrecursionlimit(10000)
def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Encontrar puntos de interconexión aérea")
    print("3- Encontrar clústeres de tráfico aéreo")
    print("4- Encontrar la ruta más corta entre ciudades")
    print("5- Utilizar las millas de viajero")
    print("6- Cuantificar el efecto de un aeropuerto cerrado")

def files():
    airports_filepath = cf.data_dir + 'airports-utf8-small.csv'
    routes_filepath = cf.data_dir + 'routes-utf8-small.csv'
    cities_filepath = cf.data_dir + 'worldcities-utf8.csv'
    airports_file = csv.DictReader(open(airports_filepath, encoding="utf-8"),
                                delimiter=",")
    routes_file = csv.DictReader(open(routes_filepath, encoding="utf-8"),
                                delimiter=",")
    cities_file = csv.DictReader(open(cities_filepath, encoding="utf-8"),
                                delimiter=",")
    #citylt = list(cities_file)
    #lastcity = citylt[-1]
    
    return airports_file, routes_file, cities_file

"""
Menu principal
"""

while True:
    airports_file, routes_file, cities_file = files()
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = controller.initcatalog()
        starttime = time.time()
        controller.loadcatalog(catalog, airports_file, routes_file, cities_file)
        controller.Bothwaysroutes(catalog)
        
        totalairports = grph.numVertices(catalog['Fullroutes'])
        bothwaysairports = grph.numVertices(catalog['Bothwaysroutes'])
        totalroutes = grph.numEdges(catalog['Fullroutes'])
        bothwaysroutes = grph.numEdges(catalog['Bothwaysroutes'])
        
        #print('ultima ciudad cargada: ' + str(firstcity['city'] + ' latitud: ' + str(firstcity['lat'])
               # + ' longitud '+ str(firstcity['lng'] + ' poblacion ' + str(firstcity['population']))))
        print('Aeropuertos indice Fullroutes: ' + str(totalairports))
        print('Aeropuertos indice Bothwaysroutes: '+ str(bothwaysairports))
        print('Total de rutas: '+str(totalroutes))
        print('Both ways routes: ' + str(bothwaysroutes))
        print("--- %s seconds ---" % (time.time() - starttime))
        
        
    elif int(inputs[0]) == 2:
        amountconnected, keys, connectionsmap = controller.MostConnected(catalog['Fullroutes'])
        table = controller.BuildMostConnectedTable(catalog,connectionsmap,keys)
        print('Connected airports inside network: ', amountconnected)
        print('\n The TOP 5 most connected aiports... \n', table)
        
    elif int(inputs[0]) == 3:
        verta = input("Ingrese el codigo IATA del aeropuerto 1: ")
        vertb = input("Ingrese el codigo IATA del aeropuerto 2: ")
        componentes = controller.getcomponents(catalog['Fullroutes'])
        together = controller.RSC(catalog['Fullroutes'],verta, vertb )
        print('componentes ' + str(componentes))
        print('strongly connected: ' + str(together))
        


    elif int(inputs[0]) == 4:
        origen = str(input('Ingrese el nombre de la ciudad de origen'))
        entry = map.get(catalog['CityNameIndex'], origen)
        citieslist = me.getValue(entry)
        table = controller.BuildTable(catalog, citieslist)
        print(table)
        eleccion = int(input('ingrese el numero en el que esta la ciudad que desea'))
        origen_elect = lt.getElement(citieslist, eleccion+1)
        print(origen_elect)
        destino = str(input('Ingrese el nombre de la ciudad destino'))
        entry2 = map.get(catalog['CityNameIndex'], destino)
        citieslist2 = me.getValue(entry2)
        table2 = controller.BuildTable(catalog, citieslist2)
        print(table2)
        eleccion = int(input('ingrese el numero en el que esta la ciudad que desea'))
        destino_elect = lt.getElement(citieslist2, eleccion+1)
        print(destino_elect)
        result = controller.Closest_Path(catalog, origen_elect, destino_elect)
        print(result)
        print("Encontrando clústeres de tráfico aéreo ....")
      
    
    elif int(inputs[0]) == 5:
        IATAfuera = str(input('ingrese el codigo IATA del aeropuerto que esta fuera de funcionamiento'))
        print(BreadhtFisrtSearch(catalog['Bothwaysroutes'], IATAfuera))
        print("Buscando ciudades recomendadas para viajar ....")
    

    elif int(inputs[0]) == 6:
        print("Calculando el efecto de aeropuerto cerrado ....")
        
    else:
        sys.exit(0)
sys.exit(0)