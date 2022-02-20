# This file contains all the required routines to make an A* search algorithm.
#
__authors__ = '1569115'
__group__ = ' DL.12'
# _________________________________________________________________________________________
# Intel.ligencia Artificial
# Grau en Enginyeria Informatica
# Curs 2016- 2017
# Universitat Autonoma de Barcelona
# _______________________________________________________________________________________

from SubwayMap import *
from utils import *
import os
import math
import copy


def expand(path, map):
    """
     It expands a SINGLE station and returns the list of class Path.
     Format of the parameter is:
        Args:
            path (object of Path class): Specific path to be expanded
            map (object of Map class):: All the information needed to expand the node
        Returns:
            path_list (list): List of paths that are connected to the given path.
    """


    llistaAux =[]
    for estacio in map.connections.keys():
        if estacio == path.last:
            for a in map.connections[estacio].keys():
                llista = copy.deepcopy(path)
                llista.add_route(a)
                llistaAux.append(llista)
    return llistaAux   
    pass


def remove_cycles(path_list):
    """
     It removes from path_list the set of paths that include some cycles in their path.
     Format of the parameter is:
        Args:
            path_list (LIST of Path Class): Expanded paths
        Returns:
            path_list (list): Expanded paths without cycles.
    """
 
    llistaAux2 =[]
    for path in path_list:
        aux = False
        for estacio in path.route[:-1]:
            if (estacio == path.route[-1]):
                aux = True
        if (aux == False):
            llistaAux2.append(path)

    return llistaAux2
    pass


def insert_depth_first_search(expand_paths, list_of_path):
    """
     expand_paths is inserted to the list_of_path according to DEPTH FIRST SEARCH algorithm
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            list_of_path (LIST of Path Class): The paths to be visited
        Returns:
            list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """
    llistaAux = expand_paths + list_of_path
    return llistaAux
    
    pass


def depth_first_search(origin_id, destination_id, map):
    """
     Depth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): the route that goes from origin_id to destination_id
    """

    llistaAux=[Path(origin_id)]
    
    while (llistaAux[0].last != destination_id) and (llistaAux != None):
        C = llistaAux[0]
        E = expand(C, map)
        El = remove_cycles(E)
        llistaAux = insert_depth_first_search(El,llistaAux[1:])
        
    if llistaAux != None:
        return llistaAux[0]
    else:
        return "No existeix Solucio"   
    pass

def insert_breadth_first_search(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to BREADTH FIRST SEARCH algorithm
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """  
    llistaAux = list_of_path + expand_paths
    return llistaAux
    pass


def breadth_first_search(origin_id, destination_id, map):
    """
     Breadth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    llistaAux=[Path(origin_id)]
    
    while ((llistaAux[0].last != destination_id) and (llistaAux != None)):
        C = llistaAux[0]
        E = expand(C, map)
        El = remove_cycles(E)
        llistaAux = insert_breadth_first_search(El, llistaAux[1:])
        
    if llistaAux != None:
        return llistaAux[0]
    else:
        return "No existeix Solucio"
    pass

def calculate_cost(expand_paths, map, type_preference=0):
    """
         Calculate the cost according to type preference
         Format of the parameter is:
            Args:
                expand_paths (LIST of Paths Class): Expanded paths
                map (object of Map class): All the map information
                type_preference: INTEGER Value to indicate the preference selected:
                                0 - Adjacency
                                1 - minimum Time
                                2 - minimum Distance
                                3 - minimum Transfers
            Returns:
                expand_paths (LIST of Paths): Expanded path with updated cost
    """
    
    for i in expand_paths:
        posActual = i.last
        posPenultim = i.penultimate
        if type_preference == 0: #Adjecencia
            i.update_g(1)

        elif type_preference == 1: #Temps minim
            i.update_g(map.connections[i.penultimate][i.last])
            
        elif type_preference == 2: #Distància minima
            if map.stations[posActual]['line'] == map.stations[posPenultim]['line']:
                tiempo = map.connections[i.penultimate][i.last]
                velocidad = map.stations[posPenultim]['velocity']
                d = velocidad * tiempo
                i.update_g(d)
         
        elif type_preference == 3: #Transferència minima
            if map.stations[posActual]['line'] != map.stations[posPenultim]['line']:
                i.update_g(1)
            pass
    
    return expand_paths
    pass


def insert_cost(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to COST VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to cost
    """
    
    listaAux = list_of_path + expand_paths
    listaAux = sorted(listaAux, key=lambda x: x.g)
    return listaAux
    pass


def uniform_cost_search(origin_id, destination_id, map, type_preference=0):
    """
     Uniform Cost Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    
    llistaAux=[Path(origin_id)]
    
    while ((llistaAux[0].last != destination_id) and (llistaAux != None)):
        C = llistaAux[0]
        E = expand(C, map)
        El = remove_cycles(E)
        aux = calculate_cost(El,map,type_preference) 
        llistaAux = insert_cost(aux, llistaAux[1:])
        
    if llistaAux != None:
        return llistaAux[0]
    else:
        return "No existeix Solucio"
    pass


def calculate_heuristics(expand_paths, map, destination_id, type_preference=0):
    """
     Calculate and UPDATE the heuristics of a path according to type preference
     WARNING: In calculate_cost, we didn't update the cost of the path inside the function
              for the reasons which will be clear when you code Astar (HINT: check remove_redundant_paths() function).
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            expand_paths (LIST of Path Class): Expanded paths with updated heuristics
    """
    if type_preference == 0:
        for i in expand_paths:
            if i.last==destination_id or i.last in map.connections[destination_id].keys():
                i.update_h(0)
            else:
                i.update_h(1)
                
    elif type_preference == 1:
        for i in expand_paths:
            x1 = map.stations[i.last]['x']
            y1 = map.stations[i.last]['y']
            x2 = map.stations[destination_id]['x']
            y2 = map.stations[destination_id]['y']
            x = x2 - x1
            x = x**2
            y = y2 - y1
            y = y**2
            h = x + y
            d = math.sqrt(h)
            i.update_h(d/max(map.velocity.values()))

    elif type_preference == 2:
        for i in expand_paths:
            x1 = map.stations[i.last]['x']
            y1 = map.stations[i.last]['y']
            x2 = map.stations[destination_id]['x']
            y2 = map.stations[destination_id]['y']
            x = x2 - x1
            x = x**2
            y = y2 - y1
            y = y**2
            h = x + y
            d = math.sqrt(h)
            i.update_h(d)
            
    elif type_preference == 3:
        for i in expand_paths:
            if map.stations[i.last]['line'] != map.stations[destination_id]['line']:
                i.update_h(1)
            else:
                i.update_h(0)
                
    return expand_paths
    pass



def update_f(expand_paths):
    """
      Update the f of a path
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
         Returns:
             expand_paths (LIST of Path Class): Expanded paths with updated costs
    """
    for i in expand_paths:
        i.update_f()
    
    return expand_paths
    pass


def remove_redundant_paths(expand_paths, list_of_path, visited_stations_cost):
    """
      It removes the Redundant Paths. They are not optimal solution!
      If a station is visited and have a lower g in this moment, we should remove this path.
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
             list_of_path (LIST of Path Class): All the paths to be expanded
             visited_stations_cost (dict): All visited stations cost
         Returns:
             new_paths (LIST of Path Class): Expanded paths without redundant paths
             list_of_path (LIST of Path Class): list_of_path without redundant paths
    """
    for i in expand_paths:
        ultim = i.last
        if ultim not in visited_stations_cost:
            visited_stations_cost[ultim] = i.g
        elif ultim in visited_stations_cost:
            if i.g < visited_stations_cost[ultim]:  
                for x in list_of_path:
                    if ultim == x.last:
                        list_of_path.remove(x)
                visited_stations_cost[ultim] = i.g
            else:
                expand_paths.remove(i)
    return (expand_paths, list_of_path, visited_stations_cost)
    pass


def insert_cost_f(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to f VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to f
    """
    listaAux = list_of_path + expand_paths
    listaAux = sorted(listaAux, key=lambda x: x.f)
    return listaAux
    pass


def coord2station(coord, map):
    """
        From coordinates, it searches the closest station.
        Format of the parameter is:
        Args:
            coord (list):  Two REAL values, which refer to the coordinates of a point in the city.
            map (object of Map class): All the map information
        Returns:
            possible_origins (list): List of the Indexes of stations, which corresponds to the closest station
    """
    diccionariDistancies = {}
    resultat = []
    for i in map.stations:
        x = map.stations[i]['x'] - coord[0]
        y = map.stations[i]['y'] - coord[1]
        distancia = x*x + y*y
        distanciaEstacio = math.sqrt(distancia)
        diccionariDistancies[i] = distanciaEstacio
    
    claves = list(diccionariDistancies.keys())
    valores = list(diccionariDistancies.values())
    posMin = valores[0]

    aux = 0
    for a in valores:
        node = claves[aux]
        if a < posMin:
            posMin = a
            if len(resultat) == 0:
                resultat.append(node)
            else:
                resultat = []
                resultat.append(node)
        elif a == posMin:
            resultat.append(node)
        aux = aux + 1
    return resultat
    pass


def Astar(origin_coor, dest_coor, map, type_preference=0):
    """
     A* Search algorithm
     Format of the parameter is:
        Args:
            origin_id (list): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    origen = coord2station(origin_coor, map)[0]
    desti = coord2station(dest_coor, map)[0]
    llistaAux=[Path(origen)]
    TCP = {}
    
    while ((llistaAux[0].last != desti) and (llistaAux != None)):
        C = llistaAux[0]
        E = expand(C, map)
        El = remove_cycles(E)
        El = calculate_cost(El, map, type_preference)
        El = calculate_heuristics(El, map, desti, type_preference)
        El = update_f(El)
        El, llistaAux, TCP= remove_redundant_paths(El, llistaAux, TCP)
        llistaAux = insert_cost_f(El, llistaAux[1:])
        
    if llistaAux != None:
        return llistaAux[0]
    else:
        return "No existeix Solucio"
    pass
