#! /usr/bin/env python
#encoding:UTF-8
'''
Created on Mar 6, 2015

@author: AlexxxYiu
'''

import json
import webbrowser
from csair.Graph import Graph
from csair.Node import Node
from matplotlib.cbook import Null

'''
helper function to 
1. list all the cities in the route network
2. show the specific information about a specific city of the route graph on shell
'''
def cityInfo(flightGraph):
    for cities in flightGraph.nodes:
        cityinfo = cities.get_data()
        print(cityinfo["code"] + "  City: " + cityinfo["name"]) 
    print("Enter the city code of the city that you want to get Info (0. return to main manu)")
    right_input = 0
    while right_input == 0:
        temp_response = raw_input().upper()
        if temp_response == "0":
            return
        for cities in flightGraph.nodes:
            cityinfo = cities.get_data()
            if temp_response == cityinfo["code"]:
                right_input = 1
                city_coordinates = cityinfo["coordinates"]
                coordinate_keys = city_coordinates.keys()
                coordinate_values = city_coordinates.values()
                print("code: " + cityinfo["code"] + "\nname: " + cityinfo["name"] + "\ncountry: " + 
                cityinfo["country"] + "\ncontinent: " + cityinfo["continent"] + "\ntimezone: " +
                str(cityinfo["timezone"]) + "\nLatitude: " + coordinate_keys[0] + str(coordinate_values[0]) + 
                "\nLongtitude: " + coordinate_keys[1] + str(coordinate_values[1]) + "\npopulation: " +
                str(cityinfo["population"]) + "\nregion: " + str(cityinfo["region"]))
        if right_input == 0:
            print("CityCode does not exist, please enter again")
    print("\n1. return to main menu 2. select different city 3. exit")
    while(1):
        temp_response = raw_input()
        if temp_response == "1":
            return
        elif temp_response == "2":
            cityInfo(flightGraph)
            return
        elif temp_response == "3":
            exit()
        else: 
            print("wrong number, please enter again")
            print("1. return to main menu 2. select different city 3. exit")
            
  
  
  
  
  
'''
helper function to list all the cities that are accessible via a single non-stop flight from the source city
'''     
def cityConnection(flightGraph):
    print("Enter the city code of the city that you want to get Info about cityConnection (0: return to main menu)")
    right_input = 0
    while right_input == 0:
        temp_response = raw_input().upper()
        if temp_response == "0":
            return
        for cities in flightGraph.nodes:
            cityinfo = cities.data
            if temp_response == cityinfo["code"]:
                right_input = 1
                connectedCity = []
                for connection in cities.edgeIn:
                    connectedCity.append(connection.data[0])
                for connection in cities.edgeOut:
                    if connection.data[1] not in connectedCity:
                        connectedCity.append(connection.data[1])      
                for city in connectedCity:
                    print(city.data["code"])
        if right_input == 0:
            print("CityCode does not exist, please enter again")
    
    print("\n1. return to main menu 2. select different city 3. exit")
    while(1):
        temp_response = raw_input()
        if temp_response == "1":
            return
        elif temp_response == "2":
            cityConnection(flightGraph)
            return
        elif temp_response == "3":
            exit()
        else: 
            print("wrong number, please enter again")
            print("1. return to main menu 2. select different city 3. exit")

 
 
 
 
'''
helper function to print out the statistical information of csAir's route network, 
''' 
def csAirInfo(flightGraph):
    print("longestFlight: " + flightGraph.flightDistance()[0] + "\n")
    print("shortestFlight: " + flightGraph.flightDistance()[1] + "\n")
    print("averageDistance: " + flightGraph.flightDistance()[2] + "\n")
    print("biggestCity: " + flightGraph.cityPopulation()[0] + "\n")
    print("smallestCity: " + flightGraph.cityPopulation()[1] + "\n")
    print("averageSize: " + flightGraph.cityPopulation()[2] + "\n")
    print("Our flight covers " + str(len(flightGraph.continent)) + " continents.")
    for continent in flightGraph.continent:
        print(continent)
    print("\nhubCity: " + flightGraph.hubCity() + "\n")
    print("\n1. return to main menu 2. exit")
    while(1):
        temp_response = raw_input()
        if temp_response == "1":
            return
        elif temp_response == "2":
            exit()
        else: 
            print("wrong number, please enter again")
            print("1. return to main menu 2. exit")
    
    
    
    
'''
helper function to visualize CSAir's route map
'''   
def visualizeMap(flightGraph):
    link = "http://www.gcmap.com/mapui?P="
    for flights in flightGraph.edges:
        flights = flights.data
        word = flights[0].data["code"] +"-"+flights[1].data["code"]+";+"
        link += word
    link = link[:-2]
    webbrowser.open_new(link)
    
   
'''
helper function to let user modify the map data
1.city removal  2.route removal 3.city addition 4.route addition 5.city edition 6. return to main menu 7. exit
'''   
def mapEdition(flightGraph):
    while 1:
        print("Please Select the following modification methods")
        print("1.city removal  2.route removal 3.city addition 4.route addition 5.city edition 6. return to main menu 7. exit")
        response = raw_input()
        if response == "1":
            while(1):
                print("Please enter the code of the city you want to remove from the graph (0 to select other options)")
                response = raw_input().upper()
                if response == "0":
                    mapEdition(flightGraph)
                    return
                if response not in flightGraph.cityCode:
                    print("code does not exist")
                    continue
                break
            flightGraph.removeCity(response)
        elif response == "2":
            direction_removal = ""
            departureCityCode =  ""
            arrivalCityCode = ""
            while 1:
                print("0. return 1. remove routes in one direction 2. remove routes in both directions")
                direction_removal = raw_input()
                if direction_removal == "0":
                    mapEdition(flightGraph)
                    return
                if direction_removal != "1" and direction_removal != "2":
                    print("incorrect input, please re-enter")
                    continue
                print("Please enter the code of the cities of the route you want to remove from the graph (0 to select other options)")
                print("if you only want to remove one direction, enter by sequence of DepartureCity ArrivalCity.")
                print("eg. 'JFK LHR' will remove the route from New York to London")
                print("if you want to remove both directions, you need to ensure that there are routes in both directions")
                response = raw_input().upper()
                if response == "0":
                    mapEdition(flightGraph)
                    return
                edgeFound = False
                departureCityCode = response[0:3]
                arrivalCityCode = response[4:]
                for routes in flightGraph.edges:
                    if (routes.data[0].data["code"] == departureCityCode and routes.data[1].data["code"] == arrivalCityCode):
                        edgeFound =True
                if not (len(response) == 7 and edgeFound):
                    print("your input format is incorrect/ code does not exist")
                    continue
                break
            if direction_removal == "1":
                flightGraph.removeRoute(departureCityCode, arrivalCityCode)
            else:
                flightGraph.removeRoute(departureCityCode, arrivalCityCode)
                flightGraph.removeRoute(arrivalCityCode, departureCityCode)
        elif response =="3":
            data = {}
            while 1:
                print("Please enter the information of the city you want to add to the flightGraph by the follow sequence, separated by empty space(0 to select other options)")
                print("[code, name, country, continent, timezone, coordinates, population, religion]")
                print("For coordinates, please enter by this format: LatitudeX-LongtitudeY")
                print("eg. N52-W0")
                print("Please enter 'timezone', 'population', 'religion' in int, otherwise, an error will throw out")
                response = raw_input()
                if response == "0":
                    mapEdition(flightGraph)
                    return
                cityDataList = response.split()
                if len(cityDataList) != 8:
                    print("lack of components")
                    continue
                data["code"] = cityDataList[0].upper()
                cityDataList[1][0].upper()
                data["name"] = cityDataList[1]
                data["country"] = cityDataList[2].upper()
                cityDataList[3][0].upper()
                data["continent"] = cityDataList[3]
                try:
                    data["timezone"] = int(cityDataList[4])
                except ValueError:
                    print("timezone input is not an int!")
                    continue
                data["coordinates"] = {}
                coordinateList = cityDataList[5].split("-")
                if len(coordinateList) != 2:
                    print("incorrect coordinates input format")
                    continue
                data["coordinates"][coordinateList[0][0]]= int(coordinateList[0][1:])
                data["coordinates"][coordinateList[1][0]]= int(coordinateList[1][1:])
                try:
                    data["population"] = int(cityDataList[6])
                except ValueError:
                    print("population input is not an integer!")
                    continue
                try:
                    data["religion"] = int(cityDataList[7])
                except ValueError:
                    print("religion input is not an int!")
                    continue
                break
            flightGraph.addNode(data)
        elif response =="4":
            while 1:
                print("0. return 1. add routes in one direction 2. add routes in both directions")
                direction_addition = raw_input()
                if direction_addition == "0":
                    mapEdition(flightGraph)
                    return
                if direction_addition != "1" and direction_addition != "2":
                    print("incorrect input, please re-enter")
                    continue
                print("Please enter the code of the cities and the distance of the route you want to add to the graph (0 to select other options)")
                print("if you only want to add route in one direction, enter by sequence of DepartureCity ArrivalCity..")
                print("eg. 'CHI ATL 958' will add the route from Chicago to Atlanta")
                response = raw_input().upper()
                print(len(response))
                if response == "0":
                    mapEdition(flightGraph)
                    return
                if not (response[0:3] in flightGraph.cityCode and response[4:7] in flightGraph.cityCode and len(response) > 8):
                    print("your input format is incorrect/ code does not exist")
                    continue
                break
            response_dataFormat = {}
            response_dataFormat["ports"] = [response[0:3], response[4:7]]
            response_dataFormat["distance"] = int(response[8:])
            if direction_addition == "1":           
                flightGraph.addSingleEdge(response_dataFormat)
            else:
                flightGraph.addDualEdge(response_dataFormat)
        elif response =="5":
            targetCity = Node({})
            while 1:
                found = 0
                print("Please enter the code of the city you want to edit (0 to select other options)")
                response = raw_input().upper()
                if response == "0":
                    mapEdition(flightGraph)
                    return
                for cities in flightGraph.nodes:
                    if cities.data["code"] == response:
                        targetCity = cities
                        found = 1
                if found == 0:
                    print("Invalid city code")   
                    continue 
                print("please enter the attribute that you want to modify, followed by new value and separated by empty space (0: return)")
                print("City Info Part: [code, name, country, continent, timezone, coordinates, population, religion]")
                print("For coordinates, please enter new value by this format: LatitudeX-LongtitudeY")
                print("eg. N52-W0")
                print("Please enter value of 'timezone', 'population', 'religion' in int, otherwise, an error will throw out")
                print("Edited city current information")
                cityinfo = targetCity.data
                city_coordinates = cityinfo["coordinates"]
                coordinate_keys = city_coordinates.keys()
                coordinate_values = city_coordinates.values()
                print("code: " + cityinfo["code"] + "\nname: " + cityinfo["name"] + "\ncountry: " + 
                cityinfo["country"] + "\ncontinent: " + cityinfo["continent"] + "\ntimezone: " +
                str(cityinfo["timezone"]) + "\nLatitude: " + coordinate_keys[0] + str(coordinate_values[0]) + 
                "\nLongtitude: " + coordinate_keys[1] + str(coordinate_values[1]) + "\npopulation: " +
                str(cityinfo["population"]) + "\nregion: " + str(cityinfo["region"]))
                
                response = raw_input() 
                if response == "0":
                    break
                response_split = response.split()
                if len(response_split) != 2:
                    print("incorrect input format")
                    continue
                cityAttribute = response_split[0]
                newValue = response_split[1]
                if cityAttribute == "timezone" or "population" or "region":
                    try:
                        targetCity.data[cityAttribute] = int(newValue)
                    except ValueError:
                        print("new value should be an integer!")
                        continue
                elif cityAttribute == "coordinates":
                    coordinateList = newValue.split("-")
                    if len(coordinateList) != 2:
                        print("incorrect coordinates input format")
                        continue
                    targetCity.data["coordinates"] = {}
                    targetCity.data["coordinates"][coordinateList[0][0]]= int(coordinateList[0][1:])
                    targetCity.data["coordinates"][coordinateList[1][0]]= int(coordinateList[1][1:])
                elif cityAttribute == ("code" or "country"):
                    targetCity.data[cityAttribute] = newValue.upper()
                elif cityAttribute == ("name" or "continent"):
                    newValue[0].upper()
                    targetCity.data[cityAttribute] = newValue
                else:
                    print("Invalid attribute")
                    continue              
        elif response =="6":
            return
        elif response =="7":
            exit()
        else:
            print("Incorrect Input, Please try again")
    
def routesInfo(flightGraph):
    Distance = 0.0
    Cost = 0.0
    Time = 0.0 ##in hour
    while 1:
        fail = 0
        print("Please enter the code of each cities you want to fly to sequentially, seperated by empty space (0: return to main menu)")
        response = raw_input().upper()
        citiesOfRoute = response.split()
        if response == "0":
            return
        if len(citiesOfRoute) <= 1:
            print("information incompleted")
            continue
        for city in citiesOfRoute:
            if city not in flightGraph.cityCode:
                print("Input should be valid city code")
                fail = 1
                break
        if fail == 1:
            continue
        for i in range (0, len(citiesOfRoute)-1):
            route = flightGraph.findRoute(citiesOfRoute[i], citiesOfRoute[i+1])
            if route == None:
                print("There is no flight between " + citiesOfRoute[i] + " and " + citiesOfRoute[i+1])
                fail = 1
                break
            else:
                Distance += flightGraph.routeInfo(route, i)[0]
                Cost += flightGraph.routeInfo(route, i)[1]
                Time += flightGraph.routeInfo(route, i)[2]
        if fail == 1:
            continue
        else:
            break
    print("Total distance of the route:" + str(Distance))
    print("Cost to fly the route: " + str(Cost))
    print("Time take to travel the route: " + str(Time*60) + " minutes\n")
        

'''
helper function to save the route network to disk in JSON format
'''
def logToJson(flightGraph):
    print("Please enter the name of the file you want to create, (0: return to main menu)")
    response = raw_input()
    if response == "0":
        return
    if len(response) == 0 or response == "map_data" or response == "cmi_hub":
        print("invalid file name")
        logToJson(flightGraph)
        return
    setChar = ["\\", "/", ":", "*", "?", "<", ">", "|"]
    for c in setChar:
        if c in response:
            print("fileName can't contain \\/：*？“<>|")
            logToJson(flightGraph)
            return
    routeNetwork = {}
    citiesInfo = []
    routesInfo = []
    routesData = {}
    for cities in flightGraph.nodes:
        citiesInfo.append(cities.data)
    for routes in flightGraph.edges:
        routesData["ports"] = [routes.data[0].data["code"], routes.data[1].data["code"]]
        routesData["distance"] = routes.data[2]
        routesInfo.append(routesData)
    routeNetwork["metro"] = citiesInfo
    routeNetwork["routes"] = routesInfo
    json_file = response + ".json"
    with open(json_file, 'w') as outfile:
        json.dump(routeNetwork, outfile, indent=4, sort_keys=True)
        print("Save successfully!")
  
  

'''
Find the shortest path between two city
'''
def findShortestPath(flightGraph):
    Cost = 0.0
    Time = 0.0    
    path = ""
    response = ""
    while 1:
        validCities = 0
        print("please enter the codes of two cities that you want to find shortest path between by the sequence of departureCity, arrivalCity, seperated by empty space (0 to exist)")
        response = raw_input().upper()
        if response == "0":
            return
        response = response.split()
        if len(response) != 2 :
            print("incorrect format")
            continue
        for city in flightGraph.nodes:
            if city.data["code"] == response[0] or city.data["code"] == response[1]:
                validCities += 1
        if validCities < 2:
            print("Incorrect input")
            continue
        path = flightGraph.shortestPath(response[0], response[1])
        if path == Null:
            print("There is no path between these two cities")
            continue
        break
    ##path: the city that is the end of the routes
    route = []
    Distance = path.distanceFromStartVertex
    while path.shortestPathFrom != Null:
        route = [path] + route
        path = path.shortestPathFrom
    route = [path] + route   
    for i in range (0, len(route)-1): 
        route_list = flightGraph.findRoute(route[i].data["code"], route[i+1].data["code"])
        Cost += flightGraph.routeInfo(route_list, i)[1]
        Time += flightGraph.routeInfo(route_list, i)[2]
    print("The shortest path between " + response[0] + " and " + response[1] + " exists")
    print("The connected airport is: ") ,
    for city in route:
        print(city.data["code"] + " ") ,
    print("\n")
    print("Total distance of the route:" + str(Distance))
    print("Cost to fly the route: " + str(Cost))
    print("Time take to travel the route: " + str(Time*60) + " minutes\n")
    
    
        
'''
Expanding CSAir's route by openning up hub city Champaign
'''      
def expansionCsAirRoute(flightGraph):
    with open('cmi_hub.json') as map_data_file:    
        map_data = json.load(map_data_file)
    for city_data in map_data["metros"]:
        flightGraph.addNode(city_data)
    for route_data in map_data["routes"]:
        flightGraph.addDualEdge(route_data)
    print("expansion completed\n")     
               
'''
main function
initialize graph
import data
create text-based User Interface
'''    
def main():
    flightGraph = Graph()
    with open('map_data.json') as map_data_file:    
        map_data = json.load(map_data_file)
    for city_data in map_data["metros"]:
        flightGraph.addNode(city_data)
    for route_data in map_data["routes"]:
        success = flightGraph.addDualEdge(route_data)
        if success == False:
            print("There is no such cities in our route network: " + route_data["ports"][0] + " , " + route_data["ports"][1])
    keep_running = True
    while keep_running:
        print("Welcome to CSAir! What can I do for you?")
        print("1. City Info")
        print("2. City Connection")
        print("3. Info about CSAir")
        print("4. View Routes on Map")
        print("5. Edition")
        print("6. Save info into json")
        print("7. Design your own routes")
        print("8. Find shortest Route between two cities")
        print("9. Expanding route network")
        print("10. Exit")
        response = raw_input()
        if response == "1":
            cityInfo(flightGraph)
        elif response == "2":
            cityConnection(flightGraph)
        elif response == "3":
            csAirInfo(flightGraph)
        elif response == "4":
            visualizeMap(flightGraph)
        elif response == "5":
            mapEdition(flightGraph)
        elif response == "6":
            logToJson(flightGraph)
        elif response == "7":
            routesInfo(flightGraph)
        elif response == "8":
            findShortestPath(flightGraph)
        elif response == "9":
            expansionCsAirRoute(flightGraph)
        elif response == "10":
            exit()
        else:
            print("Incorrect Input, Please try again")
            
            
            
            
if __name__ == '__main__':
    main()