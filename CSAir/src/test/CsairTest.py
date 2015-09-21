'''
Created on Mar 6, 2015

@author: AlexxxYiu
'''
import unittest
from csair.Node import Node
from csair.Edge import Edge
from csair.Graph import Graph
from csair.CSAir import *

city1Data =      {
            "code" : "IST" ,
            "name" : "Istanbul" ,
            "country" : "TR" ,
            "continent" : "Europe" ,
            "timezone" : 2 ,
            "coordinates" : {"N" : 41, "E" : 29} ,
            "population" : 12800000 ,
            "region" : 2
        }
city2Data =   {
            "code" : "CAI" ,
            "name" : "Cairo" ,
            "country" : "EG" ,
            "continent" : "Africa" ,
            "timezone" : 2 ,
            "coordinates" : {"N" : 30, "E" : 31} ,
            "population" : 15200000 ,
            "region" : 2
        }
city3Data =   {
            "code" : "BGW" ,
            "name" : "Bagdad" ,
            "country" : "IQ" ,
            "continent" : "Asia" ,
            "timezone" : 3.5 ,
            "coordinates" : {"N" : 33, "E" : 44} ,
            "population" : 6600000 ,
            "region" : 2
        }
city4Data =  {
            "code" : "LOS" ,
            "name" : "Lagos" ,
            "country" : "NG" ,
            "continent" : "Africa" ,
            "timezone" : 1 ,
            "coordinates" : {"N" : 7, "E" : 19} ,
            "population" : 11800000 ,
            "region" : 1
        }
city5Data =  {
            "code" : "KRT" ,
            "name" : "Khartoum" ,
            "country" : "SD" ,
            "continent" : "Africa" ,
            "timezone" : 3 ,
            "coordinates" : {"N" : 16, "E" : 33} ,
            "population" : 4975000 ,
            "region" : 1
        }
city6Data = {
            "code" : "SAO" ,
            "name" : "Sao Paulo" ,
            "country" : "BR" ,
            "continent" : "South America" ,
            "timezone" : -3 ,
            "coordinates" : {"S" : 24, "W" : 47} ,
            "population" : 20900000 ,
            "region" : 1
        }
city7Data = {
            "code" : "ALG" ,
            "name" : "Algiers" ,
            "country" : "DZ" ,
            "continent" : "Africa" ,
            "timezone" : 1 ,
            "coordinates" : {"N" : 37, "E" : 3} ,
            "population" : 3175000 ,
            "region" : 2
        }
city8Data = {
            "code" : "MAD" ,
            "name" : "Madrid" ,
            "country" : "ES" ,
            "continent" : "Europe" ,
            "timezone" : 1 ,
            "coordinates" : {"N" : 40, "W" : 4} ,
            "population" : 6200000 ,
            "region" : 3
        }
city9Data = {
            "code" : "LON" ,
            "name" : "London" ,
            "country" : "UK" ,
            "continent" : "Europe" ,
            "timezone" : 0 ,
            "coordinates" : {"N" : 52, "W" : 0} ,
            "population" : 12400000 ,
            "region" : 3
        }
city10Data = {
            "code" : "PAR" ,
            "name" : "Paris" ,
            "country" : "FR" ,
            "continent" : "Europe" ,
            "timezone" : 1 ,
            "coordinates" : {"N" : 49, "E" : 2} ,
            "population" : 10400000 ,
            "region" : 3
        }
flight1Data =  {
            "ports" : ["CAI" , "IST"] ,
            "distance" : 1227
        }
flight2Data =  {
            "ports" : ["CAI" , "BGW"] ,
            "distance" : 1264
        }
flight3Data = {
            "ports" : ["IST" , "BGW"] ,
            "distance" : 1612
        }
flight4Data = {
            "ports" : ["KRT" , "CAI"] ,
            "distance" : 1614
        }
flight5Data = {
            "ports" : ["CAI" , "ALG"] ,
            "distance" : 2710
        }
flight6Data = {
            "ports" : ["ALG" , "MAD"] ,
            "distance" : 726
        }
flight7Data = {
            "ports" : ["ALG" , "IST"] ,
            "distance" : 1354
        }
flight8Data = {
            "ports" : ["LOS" , "KRT"] ,
            "distance" : 3341
        }
flight9Data = {
            "ports" : ["SAO" , "MAD"] ,
            "distance" : 8373
        }
flight10Data =  {
            "ports" : ["SAO" , "LOS"] ,
            "distance" : 6367
        }
flight11Data = {
            "ports" : ["LON" , "PAR"] ,
            "distance" : 343
        }

class CsairTest(unittest.TestCase):
    def testAll(self):
        graph = Graph()
        self.assertEqual(graph.continent, [], "Incorrect Continent Initialization")
        self.assertEqual(graph.nodes, [], "Incorrect Node Initialization")
        self.assertEqual(graph.edges, [], "Incorrect Edge Initialization")
        self.assertFalse(graph.addDualEdge(flight1Data), "Build route between inexistent city")
        graph.addNode(city1Data)
        graph.addNode(city2Data)
        graph.addNode(city3Data)
        graph.addNode(city4Data)
        graph.addNode(city5Data)
        graph.addNode(city6Data)
        graph.addNode(city7Data)
        graph.addNode(city8Data)
        self.assertEqual(len(graph.continent), 4, "Unmatched number of continents")
        self.assertEqual(len(graph.nodes), 8, "Unsuccessful node addition")
        self.assertTrue(graph.addDualEdge(flight1Data))
        self.assertTrue(graph.addDualEdge(flight2Data))
        self.assertTrue(graph.addDualEdge(flight3Data))
        self.assertEqual(graph.routeInfo(graph.edges[0], 1), [1227, 368.09999999999997, 2.936])
        self.assertEqual(graph.shortestPath("IST", "BGW").distanceFromStartVertex, 1612, "Incorrect Shortest Path method, simplest test")

        self.assertTrue(graph.removeRoute(flight2Data["ports"][0], flight2Data["ports"][1]))
        self.assertTrue(graph.addSingleEdge(flight2Data))
        self.assertFalse(graph.addSingleEdge(flight2Data))
        self.assertEqual(len(graph.edges), 6, "Unsuccessful edge addition")
        self.assertEqual(len(graph.nodes[0].get_edgeIn()), 2, "Unequal edgeIn count")           
        self.assertEqual(len(graph.nodes[0].get_edgeOut()), 2, "Unequal edgeOut count")
        self.assertEqual(graph.findRoute("ABC", "CDE"), None)
        self.assertEqual(graph.nodes[1].get_edgeIn(), [graph.findRoute(city1Data["code"], city2Data["code"]), graph.findRoute(city3Data["code"], city2Data["code"])], "Different outgoing cities")
        
        graph.addDualEdge(flight4Data)
        graph.addDualEdge(flight5Data)
        graph.addDualEdge(flight6Data)
        graph.addDualEdge(flight7Data)
        graph.addDualEdge(flight8Data)
        graph.addDualEdge(flight9Data)
        graph.addDualEdge(flight10Data)
        self.assertEqual(graph.flightDistance(), ["\nSAO - MAD: distance 8373\nMAD - SAO: distance 8373", "\nALG - MAD: distance 726\nMAD - ALG: distance 726", "2858.8"], "Incorrect output from flightDistance method")
        self.assertEqual(graph.cityPopulation(), ["SAO", "ALG", "10206250"], "Incorrect output from cityPopulation method")
        self.assertEqual(graph.hubCity(), "CAI", "Incorrect output from hugCity method")
        self.assertFalse(graph.removeCity("ABC"), "cityCode does not exist")
        self.assertEqual(graph.shortestPath("BGW", "SAO").distanceFromStartVertex, 12065, "Incorrect Shortest Path method, second test")
        
        self.assertTrue(graph.removeCity("SAO"), "Fail on city removal")
        self.assertEqual(len(graph.edges), 16, "removeCity without removing edges")   
        self.assertEqual(len(graph.continent), 3, "continent should not be removed")

        graph.addNode(city9Data)
        graph.addNode(city10Data)
        graph.addDualEdge(flight11Data)
        print(graph.routeInfo(graph.edges[17], 1))
        self.assertEqual(graph.routeInfo(graph.edges[17], 1), [343, 102.89999999999999, 2.0])
        self.assertTrue(graph.removeCity("LOS"), "Fail on city removal")
        self.assertEqual(len(graph.continent), 3, "removeCity without removing continent") 

        self.assertTrue(graph.removeCity("ALG"), "Fail on city removal")
        self.assertEqual(graph.shortestPath("BGW", "SAO"), Null, "disconnected city")
 
        
        
        
        