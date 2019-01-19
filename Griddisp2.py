# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 15:32:29 2019

@author: buaa_
"""

class Griddisp2:
    def _init_(self):
        self.Smax=0.9   #95
        self.Smin=0.32
        self.dispmode=0 

    def griddisp2(self,Pwind,Pload,PES,Type,Disp_mode):  ## P_ES is power at POI
        self.Smax=0.9   #95
        self.Smin=0.32
        self.dispmode=0 
        Pnet=Pwind+PES-Pload