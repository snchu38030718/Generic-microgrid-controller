# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 00:10:22 2018

@author: csun26
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 15:57:30 2018

@author: csun26
"""
# do not consider the SoC limit, diesel on/off limit.
class Unplan:
    def __init__(self):

#        self.Pdiesel_max = 1.2
#        self.Pdiesel_min = 0.2  #-1.5
        self.Pdis_max = -1  #-1.5
        self.Pch_max=1
#        self.dPdiesel = 0
#        self.PSLd = 0
#        self.PCwd = 0


    def emdisp(self,Pdiesel,P_ES,Pess):  ## P_ES is power at POI
        if P_ES>=0:    # More, POI in, increase diesel
            if (self.Pdis_max-Pess-P_ES)>=0:
                self.PSLd=0
                self.PCwd=0
            else:
                self.PSLd=P_ES+self.Pdis_max+Pess
                self.PCwd=0
        else:             # Less, POI out, decrease diesel
            if (Pess+P_ES+self.Pch_max)>=0:
                self.PCwd=0
                self.PSLd=0
            else:
                 self.PCwd=-Pess-P_ES-self.Pch_max
                 self.PSLd=0