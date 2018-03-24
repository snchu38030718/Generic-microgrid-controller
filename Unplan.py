# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 15:57:30 2018

@author: csun26
"""
class Unplan:
    def __init__(self):

        self.Pdiesel_max = 1.2
        self.Pdiesel_min = 0.2  #-1.5
        
        self.dPdiesel = 0
        self.PSLd = 0
        self.PCwd = 0


    def edispatch(self,Pdiesel,P_ES):
        if P_ES>=0:    # More
            if self.Pdiesel_max-Pdiesel-P_ES>=0:
                self.dPdiesel=P_ES
                self.PSLd=0
                self.PCwd=0
            else:
                self.dPdiesel=self.Pdiesel_max-Pdiesel   # Charge
                self.PSLd=self.Pdiesel_max-Pdiesel-P_ES
                self.PCwd=0
        else:             # Freq_min<Freq<Freq_max
            if Pdiesel+P_ES-self.Pdiesel_min>=0:
                self.dPdiesel=P_ES
                self.PCwd=0
                self.PSLd=0
            else:
                 self.dPdiesel=-(Pdiesel-self.Pdiesel_min)   # Charge
                 self.PCwd=Pdiesel+P_ES-self.Pdiesel_min
                 self.PSLd=0
