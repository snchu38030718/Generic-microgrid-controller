# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 16:14:39 2019

@author: csun26
"""
class Unplan1:
    def __init__(self):
        self.SoC_max = 0.9   #95
        self.SoC_min = 0.3
        self.Pch_max = 5
        self.Pdis_max = -5  #-1.5
        self.Pdiesel_max = 5
        self.Pdiesel_min = 1  #-1.5
        self.dPdiesel = 0
        self.PSLd = 0
        self.PCwd = 0
#         Pld_disref=1
        self.Pessref=0
        self.Start_ds=0

        
## do not consider the SoC limit, diesel on/off limit.
    def emgdisp(self,Pdiesel,P_ES,start_ds,Pess,Type):  ## P_ES is power at POI
        self.SoC_max = 0.9   #95
        self.SoC_min = 0.3
        self.Pch_max = 5
        self.Pdis_max = -5  #-1.5
        self.Pdiesel_max = 5
        self.Pdiesel_min = 1  #-1.5
        self.dPdiesel=Pdiesel
        self.PSLd = 0
        self.PCwd = 0
#         Pld_disref=1
        self.Pessref=0
        self.Start_ds=0
        if Type==2:  # Keep ESS unchanged and change diesel
            if P_ES>=0:    # More, POI in, increase diesel
                if (self.Pdiesel_max-Pdiesel-P_ES)>=0:
                    self.dPdiesel=P_ES+Pdiesel
                    self.PSLd=0
                    self.PCwd=0
                    if start_ds==0: # off or run long time (>20 min)
                        self.dPdiesel=0+Pdiesel
                        self.PSLd=P_ES
                    #end
                else:
                    self.dPdiesel=self.Pdiesel_max  # Charge
                    self.PSLd=-self.Pdiesel_max+Pdiesel+P_ES
                    self.PCwd=0
                    if start_ds==0: # off or run long time (>20 min)
                        self.dPdiesel=0+Pdiesel
                        self.PSLd=P_ES
                    #end
                #end
            else:             # Less, POI out, decrease diesel
                if (Pdiesel+P_ES-self.Pdiesel_min)>=0:
                    self.dPdiesel=Pdiesel+P_ES
                    self.PCwd=0
                    self.PSLd=0
                    if start_ds==0: # off or run long time (>20 min) This is added on My 5.
                        self.dPdiesel=0+Pdiesel
                        self.PCwd=-P_ES
                    #end
                else:
                     self.dPdiesel=self.Pdiesel_min   # Charge
                     self.PCwd=Pdiesel+P_ES-self.Pdiesel_min
                     self.PSLd=0
                     if start_ds==0: # off or run long time (>20 min)
                        self.dPdiesel=0+Pdiesel
                        self.PCwd=-P_ES
                     #end
                #end
            #end
    #            self.dPdiesel=0.2
    #            self.PCwd=0
    #            self.PSLd=0.1
        elif Type==1:  ## Keep diesel unchanged and change ESS(fast transit to vf)
            self.dPdiesel=Pdiesel
            if P_ES>=0:    # More, POI in, increase ESS
                if (-self.Pdis_max-Pess)>=P_ES:
                    self.PSLd=0
                    self.PCwd=0
                else:
                    self.PSLd=P_ES+self.Pdis_max+Pess
                    self.PCwd=0
                #end
            else:             # Less, POI out, decrease ESS
                if -P_ES<=self.Pch_max+Pess:
                    self.PCwd=0
                    self.PSLd=0
                else:
                     self.PCwd=-Pess-P_ES-self.Pch_max
                     self.PSLd=0
                #end
            #end
        #end
#end
                                