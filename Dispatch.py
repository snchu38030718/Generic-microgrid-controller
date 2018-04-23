# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 17:49:18 2018
Rule_based dispatch
@author: csun26
"""
class Dispatch:
#function [self.Pessref,self.Pwdref,self.Pdsref,self.Pldref] = Ruledispatch(Pwind,Pload,SoC)

        def __init__(self):
            self.self.Pessref=0
            self.self.Pwdref=0
            self.self.Pdsref=0
            self.self.Pldref=0
            self.SoC_max = 0.9   
            self.SoC_min = 0.2
            self.Pch_max = 1
            self.Pdis_max = -1  
            self.Pds_min=0.4
            self.Pds_max=1     
        def rdispatch(self,Pwind,Pload,SoC):
            self.Pnet=Pwind-Pload
            if self.Pnet>=0:     # More, wind is controllable, diesel is off, ESS depends
                if SoC>=self.SoC_max:   # Charge
                    self.self.Pwdref=self.Pnet        # self.Pwdref is positive
                    self.self.Pessref=0
                    self.Pdsref=0
                    self.Pldref=0
                else:
                    if self.Pnet<self.Pch_max:
                        self.Pessref=self.Pnet
                        self.self.Pwdref=0
                        self.self.Pdsref=0  
                        self.self.Pldref=0
                    else:
                        self.Pessref=self.Pch_max
                        self.Pwdref=self.Pnet-self.Pch_max
                        self.Pdsref=0
                        self.Pldref=0
#                end      
#            end
            elif SoC>=self.SoC_min:    # Less, load is controllable, diesel on/off, ESS depends
                if -self.Pnet<-self.Pdis_max:
                    self.Pessref=self.Pnet   # self.Pessref is negative
                    self.Pldref=0
                    self.Pdsref=0
                    self.Pwdref=0
                else:
                    self.Pldref=-self.Pnet+self.Pdis_max  #self.Pldref is positive
                    self.Pessref=self.Pdis_max
                    self.Pdsref=0
                    self.Pwdref=0
                 #end
            else:             # Freq_min<Freq<Freq_max
                if -self.Pnet<self.Pds_min:  # ESS discharge (> is wrong)
                    self.Pldref=-self.Pnet   #self.Pldref is positive
                    self.Pessref=0 # ESS is still master
                    self.Pdsref=0
                    self.Pwdref=0
                else:                   # ESS charge
                    if -self.Pnet<=self.Pds_max:
                        self.Pessref=0
                        self.Pdsref=-self.Pnet
                        self.Pwdref=0
                        self.Pldref=0
                    else:
                        self.Pessref=0
                        self.Pwdref=0
                        self.Pdsref=self.Pds_max
                        self.Pldref=-self.Pnet+self.Pds_max
#             end
#    end
#end
#end