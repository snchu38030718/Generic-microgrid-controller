# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 01:01:57 2018

@author: csun26
"""

class Gridisp:
    def _init_(self):
        self.SoC_max = 0.9   #95
        self.SoC_min = 0.2
        self.Pch_max = 1
        self.Pdis_max = -1  #-1.5
        self.Pds_min=0.2
        self.Pds_max=1
        self.Pwdref=0
        self.Pdsref=0
        self.Pldref=0

    def gridispatch(self,Pwind,Pload,SoC,PES,start_ds):  ## P_ES is power at POI
        self.SoC_max = 0.9   #95
        self.SoC_min = 0.2
        self.Pch_max = 1
        self.Pdis_max = -1  #-1.5
        self.Pds_min=0.2
        self.Pds_max=1
        self.Pwdref=0
        self.Pdsref=0
        self.Pldref=0
        Pnet = Pwind+PES-Pload
        if Pnet>=0:    # More, wind is controllable, diesel is off, ESS depends
                if SoC>=self.SoC_max:     # Charge is
                    self.Pwdref=Pnet        # self.Pwdref is positive
                    # self.Pessref=0
                    self.Pdsref=0
                    self.Pldref=0
                    self.Start_ds=0
                else:     # SoC<self.SoC_max
                    if start_ds>=1 and start_ds<=(24000000-1):
                        self.Pdsref=self.Pds_min
                        if (Pnet+self.Pdsref)<self.Pch_max:
                            # self.Pessref=Pnet+self.Pds_min
                            self.Pwdref=0
                            self.Pldref=0
                            self.Pdsref=self.Pds_min
                            self.Start_ds=start_ds+1
                            if self.Start_ds>=24000000:
                                self.Start_ds=0
                        else:
                            # self.Pessref=self.Pch_max
                            self.Pwdref=Pnet+self.Pdsref-self.Pch_max
                            self.Pldref=0
                            self.Pdsref=self.Pds_min
                            self.Start_ds=start_ds+1
                            if self.Start_ds>=24000000:
                                self.Start_ds=0  # turn off diesel
                    else:
                        self.Start_ds=0
                        if Pnet<self.Pch_max:  # ds is off or Ton>=3
                            # self.Pessref=Pnet
                            self.Pwdref=0
                            self.Pdsref=0
                            self.Pldref=0
                        else:
                            # self.Pessref=self.Pch_max
                            self.Pwdref=Pnet-self.Pch_max
                            self.Pdsref=0
                            self.Pldref=0   
        elif SoC>=self.SoC_min:    ## Pnet<0, load is controllable, diesel on/off, SoC_min
                if  start_ds>=1 and start_ds<=(24000000-1):
                       self.Pdsref=self.Pds_min
                       Pnet=Pwind+self.Pds_min+PES-Pload
                       if -Pnet<-self.Pdis_max:   # Pnet is smaller than largest discharge power
                    # # self.Pessref=Pnet   # # self.Pessref is negative
                            self.Pldref=0
                            self.Pdsref=self.Pds_min
                            self.Start_ds=start_ds+1
                            self.Pwdref=0
                            if self.Start_ds>=24000000:
                                self.Start_ds=0
                       else:
                            self.Pldref=-Pnet+self.Pdis_max  #self.Pldref is positive
                            # self.Pessref=self.Pdis_max
                            self.Pdsref=self.Pds_min
                            self.Start_ds=start_ds+1
                            self.Pwdref=0
                            if self.Start_ds>=24000000:
                                self.Start_ds=0
                else:
                        self.Start_ds=0
                        if -Pnet<-self.Pdis_max:   # Pnet is smaller than largest discharge power
                        # self.Pessref=Pnet   # # self.Pessref is negative
                            self.Pldref=0
                            self.Pdsref=0
                            self.Pwdref=0
                        else:                 ## Pnet is larger than the largest discharge power
                            self.Pldref=-Pnet+self.Pdis_max  #self.Pldref is positive
                            # self.Pessref=self.Pdis_max
                            self.Pdsref=0
                            self.Pwdref=0
#                  self.Pdsref=0.2
#                  self.Pwdref=0
#                  self.Pldref=0
#                  self.Start_ds=1
            
               
        elif SoC<self.SoC_min:            ## SoC<self.SoC_min, diesel should be on
#                  self.Pdsref=1.2
#                  self.Pwdref=0
#                  self.Pldref=0
#                  self.Start_ds=1
                 if -Pnet<self.Pds_min:  # Pnet is smaller than the smallest diesel power Pds_min
                        if  start_ds>=1 and start_ds<=(24000000-1):
                            self.Pdsref=self.Pds_min
                            self.Start_ds=start_ds+1
                            self.Pldref=0
                            # self.Pessref=self.Pds_min-Pnet
                            self.Pwdref=0
                            if self.Start_ds>=24000000:
                                self.Start_ds=0
                        else:
                            self.Start_ds=0
                            self.Pldref=-Pnet   #self.Pldref is positive, shedding
                            # self.Pessref=0 # ESS is still master
                            self.Pdsref=0
                            self.Pwdref=0
                        
                 else:                   
                        if (-Pnet-self.Pds_max)<=0:  # self.Pds_min<-Pnet<self.Pds_max
                            # self.Pessref=0
                            self.Pdsref=-Pnet
                            self.Start_ds=start_ds+1
                            self.Pwdref=0
                            self.Pldref=0
                            if self.Start_ds>=24000000:
                                self.Start_ds=0
                        else:              # -Pnet>self.Pds_max
                            # self.Pessref=0
                            self.Pwdref=0
                            self.Pdsref=self.Pds_max
                            self.Start_ds=start_ds+1
                            self.Pldref=-Pnet-self.Pds_max
                            if self.Start_ds>=24000000:
                                self.Start_ds=0