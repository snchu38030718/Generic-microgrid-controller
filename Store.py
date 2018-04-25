# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 22:09:25 2018

@author: csun26
"""

class Store( object ):
    def __init__( self ):
        self.x, self.y, self.z = 1.0, 1.0, 3.0
    def store(self, x,y,z):
#        if x is None and y is None and z is None:
#            return self.x, self.y, self.z
#        else:
         self.x, self.y, self.z = x, y, z
    def getx(self):
        return self.x
    def gety(self):
        return self.y
    def getz(self):
        return self.z