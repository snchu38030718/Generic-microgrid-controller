# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 15:57:30 2018

@author: csun26
"""
# do not consider the SoC limit, diesel on/off limit.
class Unplan:
    def __init__(self):

        self.Pdiesel_max = 1.2
        self.Pdiesel_min = 0.2  #-1.5
        self.Pdis_max = -1  #-1.5
        self.Pch_max=1
#        self.dPdiesel = 0
#        self.PSLd = 0
#        self.PCwd = 0


    def edispatch(self,Pdiesel,P_ES,start_ds,Pess,Type):  ## P_ES is power at POI
        if Type==1:
            if P_ES>=0:    # More, POI in, increase diesel
                if (self.Pdiesel_max-Pdiesel-P_ES)>=0:
                    self.dPdiesel=P_ES+Pdiesel
                    self.PSLd=0
                    self.PCwd=0
                    if start_ds==0: # off or run long time (>20 min)
                        self.dPdiesel=0+Pdiesel
                        self.PSLd=P_ES
                else:
                    self.dPdiesel=self.Pdiesel_max  # Charge
                    self.PSLd=-self.Pdiesel_max+Pdiesel+P_ES
                    self.PCwd=0
                    if start_ds==0: # off or run long time (>20 min)
                        self.dPdiesel=0+Pdiesel
                        self.PSLd=P_ES
            else:             # Less, POI out, decrease diesel
                if (Pdiesel+P_ES-self.Pdiesel_min)>=0:
                    self.dPdiesel=Pdiesel+P_ES
                    self.PCwd=0
                    self.PSLd=0
                    if start_ds==0: # off or run long time (>20 min) This is added on My 5.
                        self.dPdiesel=0+Pdiesel
                        self.PCwd=-P_ES
                else:
                     self.dPdiesel=self.Pdiesel_min   # Charge
                     self.PCwd=Pdiesel+P_ES-self.Pdiesel_min
                     self.PSLd=0
                     if start_ds==0: # off or run long time (>20 min)
                        self.dPdiesel=0+Pdiesel
                        self.PCwd=-P_ES
    #            self.dPdiesel=0.2
    #            self.PCwd=0
    #            self.PSLd=0.1
        elif Type==2:
            self.dPdiesel=Pdiesel
            if P_ES>=0:    # More, POI in, increase ESS
                if (-self.Pdis_max-Pess)>=P_ES:
                    self.PSLd=0
                    self.PCwd=0
                else:
                    self.PSLd=P_ES+self.Pdis_max+Pess
                    self.PCwd=0
            else:             # Less, POI out, decrease ESS
                if -P_ES<=self.Pch_max+Pess:
                    self.PCwd=0
                    self.PSLd=0
                else:
                     self.PCwd=-Pess-P_ES-self.Pch_max
                     self.PSLd=0
                    
                    