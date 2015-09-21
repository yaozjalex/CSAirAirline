'''
Created on Mar 6, 2015

@author: AlexxxYiu
'''
from csair.Node import Node
from csair.Edge import Edge
import sys
import math
from matplotlib.cbook import Null

class Graph(object):
    def __init__(self):
        self.continent = []
        self.nodes = []
        self.edges = []
        self.cityCode = []



    '''
    helper function to calculate the routes' information related with distance
    return value: tuple(longestSingleRoute, shorestSingleRoute, averageDistance)
    '''
    def flightDistance(self):
        totalDistance = 0.0
        longestDistance = 0
        shortestDistance = sys.maxint
        longestFlight = []
        shortestFlight = []
        for flights in self.edges:
            flights = flights.data
            totalDistance += flights[2]
            if longestDistance < flights[2]:
                longestDistance = flights[2]
                longestFlight = [flights]
            elif longestDistance == flights[2]:
                longestFlight.append(flights)
            if shortestDistance > flights[2]:
                shortestDistance = flights[2]
                shortestFlight = [flights]
            elif shortestDistance == flights[2]:
                shortestFlight.append(flights)
        ##modify the longest and shortest flights into string
        longestFlight_rt = ""
        shortestFlight_rt = ""
        for flights in longestFlight:                 
            longestFlight_rt += "\n" + flights[0].data["code"] + " - " + flights[1].data["code"] + ": distance " + str(flights[2])
        
        for flights in shortestFlight:
            shortestFlight_rt += "\n" + flights[0].data["code"] + " - " + flights[1].data["code"] + ": distance " + str(flights[2])
        return [longestFlight_rt, shortestFlight_rt, str(totalDistance / len(self.edges))] 
                
    
    
    '''
    helper function to calculate the graph's statistical information related with city size
    return value: tuple(biggestCityCityCode, smallestCityCityCode, averageSize)
    '''

    def cityPopulation(self):
        totalSize = 0
        biggestCity = {"population" : 0}
        smallestCity = {"population" : sys.maxint}
        for city in self.nodes:
            cityData = city.data
            totalSize += cityData["population"]
            if cityData["population"] > biggestCity["population"]:
                biggestCity = cityData
            if cityData["population"] < smallestCity["population"]:
                smallestCity = cityData
        return [biggestCity["code"], smallestCity["code"], str(totalSize / len(self.nodes))]


    '''
    helper function that return the hub cities (cities that have the most direct connection)
    '''
    def hubCity(self):
        hubCity = Node({})
        for city in self.nodes:
            if (len(city.edgeIn) + len(city.edgeOut)) > (len(hubCity.edgeIn) + len(hubCity.edgeOut)):
                hubCity = city
        return hubCity.data["code"]
    
    

    '''
    Add a node to the graph
    '''
    def addNode(self, node_data):
        if node_data["continent"] in self.continent:
            pass
        else:
            self.continent.append(node_data["continent"])
        city = Node(node_data)
        self.nodes.append(city)
        self.cityCode.append(node_data["code"])
    
    
    '''
    Add single directed route of two cities to the graph
    '''
    def addSingleEdge(self,edge_data): 
        departureCity = edge_data["ports"][0] ##string
        arrivalCity = edge_data["ports"][1]
        route_distance = edge_data["distance"]
        d_n = Node({})
        a_n = Node({})
        for cur_node in self.nodes:
            node_data = cur_node.get_data()
            if node_data["code"] == departureCity:
                d_n = cur_node
            if node_data["code"] == arrivalCity:
                a_n = cur_node  
        for edge in self.edges:
            if edge.data == [d_n, a_n, route_distance]:      ##edge_data: parse from json file
                return False
        new_edge = Edge([d_n, a_n, route_distance])
        d_n.edgeOut.append(new_edge)
        a_n.edgeIn.append(new_edge)
        self.edges.append(new_edge)
        return True
    
    '''
    Add two directed routes of two cities to the graph
    '''
    def addDualEdge(self, edge_data):
        city1 = edge_data["ports"][0] ##string
        city2 = edge_data["ports"][1]
        route_distance = edge_data["distance"]
        nodeList = []
        for cur_node in self.nodes:
            node_data = cur_node.get_data()
            if node_data["code"] == city1:
#                 cur_node.add_edgeIn(edge_data)
#                 cur_node.add_edgeOut(city1)
                nodeList.append(cur_node)
            if node_data["code"] == city2:
#                 cur_node.add_edgeIn(city2)
#                 cur_node.add_edgeOut(city2)
                nodeList.append(cur_node)
        if len(nodeList) < 2:
            return False
        flight_info = (nodeList[0], nodeList[1], route_distance)
        flight = Edge(flight_info)
        if flight not in self.edges:
            self.edges.append(flight)
        nodeList[0].add_edgeOut(flight)
        nodeList[1].add_edgeIn(flight)
        flight_info = (nodeList[1], nodeList[0], route_distance)
        flight = Edge(flight_info)
        if flight not in self.edges:
            self.edges.append(flight)
        nodeList[1].add_edgeOut(flight)
        nodeList[0].add_edgeIn(flight)

        return True
    
    '''
    Remove a city from the graph
    '''
    def removeCity(self, cityCode):
        if cityCode not in self.cityCode:
            return False
        ##remove from cityCode
        self.cityCode.remove(cityCode)
        targetCity = Node(None)
        for cities in self.nodes:
            if cityCode == cities.data["code"]:
                targetCity = cities
        ##remove from continent
        continentCount = 0
        for cities in self.nodes:
            if cities.data["continent"] == targetCity.data["continent"] and cities != targetCity:
                continentCount = 1
        if continentCount == 0:
            self.continent.remove(targetCity.data["continent"])
        ##remove from edges
        ##remove the edgeIn and edgeOut of connected cities
        removeRoute = []
        for routes in self.edges:
            if routes.data[0].data["code"] == targetCity.data["code"]: ##city is the departure city
                removeRoute.append(routes)
#                 self.edges.remove(routes)
                for cities in self.nodes:
                    if cities.data["code"] == routes.data[1].data["code"]:
                        cities.edgeIn.remove(routes)
                        break
            elif routes.data[1].data["code"] == targetCity.data["code"]: ##city is the arrival city
                removeRoute.append(routes)
#                 self.edges.remove(routes)
                for cities in self.nodes:
                    if cities.data["code"] == routes.data[0].data["code"]:
                        cities.edgeOut.remove(routes)
                        break
        for route in removeRoute:
            self.edges.remove(route)
        ##remove from nodes
        self.nodes.remove(targetCity)
        return True



    def removeRoute(self, departureCityCode, arrivalCityCode):
        success = False
        ##remove the edges
        routes = self.findRoute(departureCityCode, arrivalCityCode)
        if routes != None:
            self.edges.remove(routes)
            success = True
        ##remove edgeIn and edgeOut from arrival and departure cities
            for cities in self.nodes:
                if cities.data["code"] == departureCityCode:
                    cities.edgeOut.remove(routes)
                if cities.data["code"] == arrivalCityCode:
                    cities.edgeIn.remove(routes)    
        return success
    
    '''
    find the shortest path between two cities
    '''
    def shortestPath(self, CityACode, CityBCode):
        visited = []
        unvisited = []
        for city in self.nodes:
            unvisited.append(city)
        cityA = None
        cityB = None
        for city in self.nodes:
            city.distanceFromStartVertex = sys.maxint
            city.shortestPathFrom = Null
            if city.data["code"] == CityACode:
                cityA = city
            if city.data["code"] == CityBCode:
                cityB = city
        cityA.distanceFromStartVertex = 0
        visited.append(cityA)
        unvisited.remove(cityA)
        return self.shortestPathRecursiveHelper(cityA, cityB, visited, unvisited) 
        
        
        
    def shortestPathRecursiveHelper(self, curCity, cityB, visited, unvisited):
        if(curCity == cityB): ##Base case: we find the shortest path
            return curCity ##finish tail recursion, return Nodes of the ending city
        
        for flights in curCity.edgeOut:
            for city in self.nodes:
                if city ==  flights.data[1] and city not in visited and city.distanceFromStartVertex > curCity.distanceFromStartVertex + flights.data[2]:
                    city.distanceFromStartVertex = curCity.distanceFromStartVertex + flights.data[2]
                    city.shortestPathFrom = curCity
        mini = sys.maxint
        minCity = Node({})
        for city in unvisited:
            if city.distanceFromStartVertex < mini:
                mini = city.distanceFromStartVertex
                minCity = city
        if mini == sys.maxint:
            return Null
        visited.append(minCity)
        unvisited.remove(minCity)
        return self.shortestPathRecursiveHelper(minCity, cityB, visited, unvisited)           
       
       
    def routeInfo(self, route, i):
        Acceleration = 750 * 15 / 8
        Cost = 0.0
        Time = 0.0
        flightDistance = route.data[2]
        Distance = flightDistance
        if i <= 7:
            Cost = (float)(0.35 - 0.05 * i) * flightDistance
        if flightDistance <= 400:
            Time = (float)(math.sqrt(flightDistance / Acceleration))
        else:
            Time = (float)(flightDistance - 400) / 750 + (float)(math.sqrt(400 / Acceleration))
        if i != 0 and len(route.data[1].edgeOut) <= 12:
            Time += 2 - (float)(len(route.data[1].edgeOut) - 1) * 1/6  
        return [Distance, Cost, Time]
       
       
        
    '''
    find the route in the route network
    return: the route(Edge)
    '''
    def findRoute(self, departureCityCode, arrivalCityCode):
        for routes in self.edges:
            if routes.data[0].data["code"] == departureCityCode and routes.data[1].data["code"] == arrivalCityCode:
                return routes
        return None