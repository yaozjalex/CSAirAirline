import sys
'''
Created on Mar 6, 2015

@author: AlexxxYiu
'''
from matplotlib.cbook import Null
class Node(object):
    '''
    default initialization funcition of edge
    data: same as the json input
    '''
    def __init__(self, node_data):
        self.data = node_data
        self.edgeIn = []  ##Edge
        self.edgeOut = []
        ##for Dijkstra's Algorithm
        self.distanceFromStartVertex = (float)(sys.maxint)
        self.shortestPathFrom = Null
    def get_data(self):
        return self.data
    
    def get_edgeIn(self):
        return self.edgeIn
    
    def get_edgeOut(self):
        return self.edgeOut
    
    def add_edgeIn(self, connectedCity):
        self.edgeIn.append(connectedCity)
        
    def add_edgeOut(self, connectedCity):
        self.edgeOut.append(connectedCity)
        