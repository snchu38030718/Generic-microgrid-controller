# -*- coding: utf-8 -*-
"""
# Dispatch in grid-connected mode
Created on Tue Jan  8 14:26:41 2019

@author: csun26
"""

class Griddisp1:
    def _init_(self):
        self.SoC_max=0.9   #95
        self.SoC_min=0.3
        self.disp_mode=0 
        self.Pch_max = 1
        self.Pdis_max = -1  #-1.5
        self.Pds_min=0.3
        self.Pds_max=1
        self.Pwdref=0
        self.Tdiesel=4
        self.Pldref=0
        self.Pessref=0
        self.Pdsref=0
        self.Start_ds=0
		
    def griddisp1(self,Pwind,Pload,SoC,PES,start_ds,Type,Disp_mode,SoC_ref):  ## P_ES is power at POI
        self.SoC_max=0.9   #95
        self.SoC_min=0.3
        self.disp_mode=0 
        self.Pch_max = 1
        self.Pdis_max = -1  #-1.5
        self.Pds_min=0.3
        self.Pds_max=1
        self.Pwdref=0
        self.Tdiesel=4
        self.Pldref=0
        self.Pessref=0
        self.Pdsref=0
        self.Start_ds=1
        Pnet=Pwind+PES-Pload
        if Type==1:  ## load following&cycle charging  # Load following & cycle charging
            if Pnet>=0 and Disp_mode==0:    # More, wind is controllable, diesel is off, ESS dep#ends
                self.dispmode=0
                if SoC>=self.SoC_max:     # Charge is
                    self.Pwdref=Pnet        # self.Pwdref is positive
                    self.Pessref=0
                    self.Pdsref=0
                    self.Pldref=0
                    self.Start_ds=0
                else:     # SoC<self.SoC_max
                    if start_ds>=1 and (start_ds<=(self.Tdiesel-1)):
                        self.Pdsref=self.Pds_min*1
                        if (Pnet+self.Pdsref)<self.Pch_max:
                            self.Pessref=Pnet+self.Pds_min
                            self.Pwdref=0
                            self.Pldref=0
                            self.Pdsref=self.Pds_min
                            self.Start_ds=start_ds+1
                            if self.Start_ds>=self.Tdiesel:
                                self.Start_ds=0
                            #end
                        else:
                            self.Pessref=self.Pch_max
                            self.Pwdref=Pnet+self.Pdsref-self.Pch_max
                            self.Pldref=0
#                                 self.Pdsref=self.Pds_min
                            self.Start_ds=start_ds+1
                            if self.Start_ds>=self.Tdiesel:
                                self.Start_ds=0  # turn off diesel
                            #end
                        #end
                    else:
                        self.Start_ds=0
                        if Pnet<self.Pch_max:  # ds is off or Ton>=3
                            self.Pessref=Pnet
                            self.Pwdref=0
                            self.Pdsref=0
                            self.Pldref=0
                        else:
                            self.Pessref=self.Pch_max
                            self.Pwdref=Pnet-self.Pch_max
                            self.Pdsref=0
                            self.Pldref=0 
                        #end
                        #end
                    #end           
            elif SoC>=self.SoC_min and Disp_mode==0:   ## Pnet<0, load is controllable, diesel on/off, self.SoC_min
                self.disp_mode=0
                if start_ds>=1 and (start_ds<=(self.Tdiesel-1)):
#                            self.Pdsref=self.Pds_min
                    Pnet=Pwind+self.Pds_min+PES-Pload
                    if -Pnet<-self.Pdis_max:   # Pnet is smaller than largest discharge power
                        self.Pessref=Pnet   # # self.Pessref is negative
                        self.Pldref=0
                        self.Pdsref=self.Pds_min
                        self.Start_ds=start_ds+1
                        self.Pwdref=0
                        if self.Start_ds>=self.Tdiesel:
                            self.Start_ds=0
                        #end
                    else:
                        self.Pldref=-Pnet+self.Pdis_max  #self.Pldref is positive
                        self.Pessref=self.Pdis_max
                        self.Pdsref=self.Pds_min
                        self.Start_ds=start_ds+1
                        self.Pwdref=0
                        if self.Start_ds>=self.Tdiesel:
                            self.Start_ds=0
                            #end
                       #end
                else:
                    self.Start_ds=0
                    if -Pnet<-self.Pdis_max:   # Pnet is smaller than largest discharge power
                        self.Pessref=Pnet   # # self.Pessref is negative
                        self.Pldref=0
                        self.Pdsref=0
                        self.Pwdref=0
                    else:                 ## Pnet is larger than the largest discharge power
                        self.Pldref=-Pnet+self.Pdis_max  #self.Pldref is positive
                        self.Pessref=self.Pdis_max
                        self.Pdsref=0
                        self.Pwdref=0
                        #end
                #end
            elif SoC<self.SoC_min or Disp_mode==1:           ## SoC<self.SoC_min, diesel should be on
                self.disp_mode=1
                if SoC>=self.SoC_min+0.2:   #Hysteresis control
                    self.disp_mode=0
                   #end
                if -Pnet<self.Pds_min:  # Pnet is smaller than the smallest diesel power self.Pds_min
                    if start_ds>=1 and (start_ds<=(self.Tdiesel-1)):
                        self.Pdsref=self.Pds_min
                        self.Start_ds=start_ds+1
                        self.Pldref=0
                        self.Pessref=self.Pds_min+Pnet##+ or -,charge
                        self.Pwdref=0
#                                 if self.Start_ds>=self.Tdiesel
#                                     self.Start_ds=0
#                                 #end
                    else:  ## diesel is OFF
                        self.Start_ds=start_ds+1    # change 4
                        self.Pdsref=self.Pds_min
                        self.Pldref=0
#                                 self.Start_ds=0 
#                                 self.Pdsref=0 #(conventional load following
#                                 control)
                        # self.Pldref=-Pnet   # (conventional load following control)#self.Pldref is positive, shedding
                        self.Pessref=self.Pds_min+Pnet # ESS is still master
                        self.Pwdref=0
                        #end
                else:                   
                    if (-Pnet-self.Pds_max)<=0:  # self.Pds_min<-Pnet<self.Pds_max
                        self.Pessref=self.Pds_max+Pnet
                        self.Pdsref=self.Pds_max  # to charge BESS back
#                                 self.Pdsref=-Pnet
                        self.Start_ds=start_ds+1
                        self.Pwdref=0
                        self.Pldref=0
#                                 if self.Start_ds>=self.Tdiesel
#                                     self.Start_ds=0
#                                 #end
                    else:              # -Pnet>self.Pds_max
                        self.Pessref=0
                        self.Pwdref=0
                        self.Pdsref=self.Pds_max
                        self.Start_ds=start_ds+1
                        self.Pldref=-Pnet-self.Pds_max
#                                 if self.Start_ds>=self.Tdiesel
#                                     self.Start_ds=0
#                                 #end
#                            end
#                     end
#            end
            
            # Power smoothing & Cycle charging control
        elif Type==2:
            if (SoC>=0.48 and SoC<=SoC_ref) or Disp_mode==2:  ##should disable or in type D
                self.disp_mode=2
                Pnet = -Pwind-PES+Pload  ## load larger than genertion
                self.Start_ds=start_ds+1
                if (Pnet-self.Pds_max)>=0: ## More, wind is controllable, diesel is off, ESS dep#ends
                    if (Pnet-self.Pds_max)<-self.Pdis_max:      ## Discharge
                        self.Pdsref=self.Pds_max
                        self.Pldref=0
                        self.Pwdref=0
                        self.Pessref=-Pnet+self.Pds_max # discharge
                    else:
                        self.Pdsref=self.Pds_max
                        self.Pldref=Pnet-self.Pds_max+self.Pdis_max
                        self.Pwdref=0
                        self.Pessref=self.Pdis_max  #discharge
                    #end
                elif Pnet > self.Pds_min:
                    self.Pdsref=Pnet
                    self.Pldref=0
                    self.Pwdref=0
                    self.Pessref=0
                else:   # Pnet<self.Pds_min
                    self.Pdsref=self.Pds_min
                    if self.Start_ds>=self.Tdiesel:
                        self.Start_ds=0
                        self.Pdsref=0                   
                    #end
        #                self.Pdsref=0.5
                        self.Pldref=0
                    if (self.Pdsref-Pnet)<self.Pch_max:
                        self.Pwdref=0
                        self.Pessref=self.Pdsref-Pnet # charge
                        if self.Pessref>=0:  #charge
                            self.Pldref=0
                        else:  #discharge
                            self.Pldref=0 ## right or wrong?              
#                             self.Pldref=-self.Pessref
#                             self.Pessref=0
                        #end
                    else:
                        self.Pwdref=-Pnet+self.Pdsref-self.Pch_max
                        self.Pessref=self.Pch_max   #charge
                    #end
                #end
            else:
                Pnet=Pwind+PES-Pload
                if Pnet>=0 and Disp_mode==0:    # More, wind is controllable, diesel is off, ESS dep#ends
                    self.disp_mode=0
                    if SoC>=self.SoC_max:     # Charge is
                        self.Pwdref=Pnet        # self.Pwdref is positive
                        self.Pessref=0
                        self.Pdsref=0
                        self.Pldref=0
                        self.Start_ds=0
                    else:     # SoC<self.SoC_max
                        if start_ds>=1 and (start_ds<=(self.Tdiesel-1)):
                            self.Pdsref=self.Pds_min*1
                            if (Pnet+self.Pdsref)<self.Pch_max:
                                self.Pessref=Pnet+self.Pds_min
                                self.Pwdref=0
                                self.Pldref=0
                                self.Pdsref=self.Pds_min
                                self.Start_ds=start_ds+1
                                if self.Start_ds>=self.Tdiesel:
                                    self.Start_ds=0
                                #end
                            else:
                                self.Pessref=self.Pch_max
                                self.Pwdref=Pnet+self.Pdsref-self.Pch_max
                                self.Pldref=0
#                                 self.Pdsref=self.Pds_min
                                self.Start_ds=start_ds+1
                                if self.Start_ds>=self.Tdiesel:
                                    self.Start_ds=0  # turn off diesel
                                #end
                            #end
                        else:
                            self.Start_ds=0
                            if Pnet<self.Pch_max:  # ds is off or Ton>=3
                                self.Pessref=Pnet
                                self.Pwdref=0
                                self.Pdsref=0
                                self.Pldref=0
                            else:
                                self.Pessref=self.Pch_max
                                self.Pwdref=Pnet-self.Pch_max
                                self.Pdsref=0
                                self.Pldref=0 
                            #end
                        #end
                    #end
    #                  self.Pdsref=0.5
    #                  self.Pwdref=0.2
    #                  self.Pldref=0
    #                  self.Start_ds=0              
                elif SoC>=self.SoC_min and Disp_mode==0:   ## Pnet<0, load is controllable, diesel on/off, self.SoC_min
                    self.disp_mode=0
                    if start_ds>=1 and (start_ds<=(self.Tdiesel-1)):
#                            self.Pdsref=self.Pds_min
                        Pnet=Pwind+self.Pds_min+PES-Pload
                        if -Pnet<-self.Pdis_max:   # Pnet is smaller than largest discharge power
                            self.Pessref=Pnet   # # self.Pessref is negative
                            self.Pldref=0
                            self.Pdsref=self.Pds_min
                            self.Start_ds=start_ds+1
                            self.Pwdref=0
                            if self.Start_ds>=self.Tdiesel:
                                self.Start_ds=0
                            #end
                        else:
                            self.Pldref=-Pnet+self.Pdis_max  #self.Pldref is positive
                            self.Pessref=self.Pdis_max
                            self.Pdsref=self.Pds_min
                            self.Start_ds=start_ds+1
                            self.Pwdref=0
                            if self.Start_ds>=self.Tdiesel:
                                self.Start_ds=0
                            #end
                       #end
                    else:
                        self.Start_ds=0
                        if -Pnet<-self.Pdis_max:   # Pnet is smaller than largest discharge power
                            self.Pessref=Pnet   # # self.Pessref is negative
                            self.Pldref=0
                            self.Pdsref=0
                            self.Pwdref=0
                        else:                 ## Pnet is larger than the largest discharge power
                            self.Pldref=-Pnet+self.Pdis_max  #self.Pldref is positive
                            self.Pessref=self.Pdis_max
                            self.Pdsref=0
                            self.Pwdref=0
                        #end
                    #end
    #                  self.Pdsref=0
    #                  self.Pwdref=0.5
    #                  self.Pldref=0
    #                  self.Start_ds=0
                elif SoC<self.SoC_min or Disp_mode==1:           ## SoC<self.SoC_min, diesel should be on
    #                  self.Pdsref=0.2
    #                  self.Pwdref=0
    #                  self.Pldref=0
    #                  self.Start_ds=0
                    self.disp_mode=1
                    if SoC>=self.SoC_min+0.2:   #Hysteresis control
                        self.disp_mode=0
                       #end
                    if -Pnet<self.Pds_min:  # Pnet is smaller than the smallest diesel power self.Pds_min
                        if  start_ds>=1 and (start_ds<=(self.Tdiesel-1)):
                            self.Pdsref=self.Pds_min
                            self.Start_ds=start_ds+1
                            self.Pldref=0
                            self.Pessref=self.Pds_min+Pnet## + or -
                            self.Pwdref=0
#                                 if self.Start_ds>=self.Tdiesel
#                                     self.Start_ds=0
#                                 #end
                        else:  ## diesel is OFF
                            self.Start_ds=start_ds+1    # change 4
                            self.Pdsref=self.Pds_min
                            self.Pldref=0
#                                 self.Start_ds=0 
#                                 self.Pdsref=0 #(conventional load following
#                                 control)
                                # self.Pldref=-Pnet   # (conventional load following control)#self.Pldref is positive, shedding
                            self.Pessref=self.Pds_min+Pnet # ESS is still master
                            self.Pwdref=0
                            #end
                    else:                   
                        if (-Pnet-self.Pds_max)<=0:  # self.Pds_min<-Pnet<self.Pds_max
                            self.Pessref=self.Pds_max+Pnet
                            self.Pdsref=self.Pds_max  # to charge BESS back
#                                 self.Pdsref=-Pnet
                            self.Start_ds=start_ds+1
                            self.Pwdref=0
                            self.Pldref=0
#                                 if self.Start_ds>=self.Tdiesel
#                                     self.Start_ds=0
#                                 #end
                        else:              # -Pnet>self.Pds_max
                            self.Pessref=0
                            self.Pwdref=0
                            self.Pdsref=self.Pds_max
                            self.Start_ds=start_ds+1
                            self.Pldref=-Pnet-self.Pds_max
#                                 if self.Start_ds>=self.Tdiesel
#                                     self.Start_ds=0
#                                 #end
                            #end
                     #end
            #end   
            #end
            ## load following
        elif Type==3:  
            if Pnet>=0:    # More, wind is controllable, diesel is off, ESS dep#ends
                if SoC>=self.SoC_max:     # Charge is
                    self.Pwdref=Pnet        # self.Pwdref is positive
                    self.Pessref=0
                    self.Pdsref=0
                    self.Pldref=0
                    self.Start_ds=0
                else:     # SoC<self.SoC_max
                    if start_ds>=1 and (start_ds<=(self.Tdiesel-1)):
                        self.Pdsref=self.Pds_min*1
                        if (Pnet+self.Pdsref)<self.Pch_max:
                            self.Pessref=Pnet+self.Pds_min
                            self.Pwdref=0
                            self.Pldref=0
                            self.Pdsref=self.Pds_min
                            self.Start_ds=start_ds+1
                            if self.Start_ds>=self.Tdiesel:
                                self.Start_ds=0
                            #end
                        else:
                            self.Pessref=self.Pch_max
                            self.Pwdref=Pnet+self.Pdsref-self.Pch_max
                            self.Pldref=0
#                                 self.Pdsref=self.Pds_min
                            self.Start_ds=start_ds+1
                            if self.Start_ds>=self.Tdiesel:
                                self.Start_ds=0  # turn off diesel
                            #end
                        #end
                    else:
                        self.Start_ds=0
                        if Pnet<self.Pch_max:  # ds is off or Ton>=3
                            self.Pessref=Pnet
                            self.Pwdref=0
                            self.Pdsref=0
                            self.Pldref=0
                        else:
                            self.Pessref=self.Pch_max
                            self.Pwdref=Pnet-self.Pch_max
                            self.Pdsref=0
                            self.Pldref=0 
                        #end
                    #end
                    #end
    #                  self.Pdsref=0.5
    #                  self.Pwdref=0.2
    #                  self.Pldref=0
    #                  self.Start_ds=0              
            elif SoC>=self.SoC_min:   ## Pnet<0, load is controllable, diesel on/off, self.SoC_min
                if start_ds>=1 and (start_ds<=(self.Tdiesel-1)):
#                            self.Pdsref=self.Pds_min
                   Pnet=Pwind+self.Pds_min+PES-Pload
                   if -Pnet<-self.Pdis_max:   # Pnet is smaller than largest discharge power
                        self.Pessref=Pnet   # # self.Pessref is negative
                        self.Pldref=0
                        self.Pdsref=self.Pds_min
                        self.Start_ds=start_ds+1
                        self.Pwdref=0
                        if self.Start_ds>=self.Tdiesel:
                            self.Start_ds=0
                        #end
                   else:
                        self.Pldref=-Pnet+self.Pdis_max  #self.Pldref is positive
                        self.Pessref=self.Pdis_max
                        self.Pdsref=self.Pds_min
                        self.Start_ds=start_ds+1
                        self.Pwdref=0
                        if self.Start_ds>=self.Tdiesel:
                            self.Start_ds=0
                        #end
                   #end
                else:
                    self.Start_ds=0
                    if -Pnet<-self.Pdis_max:   # Pnet is smaller than largest discharge power
                        self.Pessref=Pnet   # # self.Pessref is negative
                        self.Pldref=0
                        self.Pdsref=0
                        self.Pwdref=0
                    else:                 ## Pnet is larger than the largest discharge power
                        self.Pldref=-Pnet+self.Pdis_max  #self.Pldref is positive
                        self.Pessref=self.Pdis_max
                        self.Pdsref=0
                        self.Pwdref=0
                    #end
                    #end
    #                  self.Pdsref=0
    #                  self.Pwdref=0.5
    #                  self.Pldref=0
    #                  self.Start_ds=0
            elif SoC<self.SoC_min:           ## SoC<self.SoC_min, diesel should be on
    #                  self.Pdsref=0.2
    #                  self.Pwdref=0
    #                  self.Pldref=0
    #                  self.Start_ds=0
                if -Pnet<self.Pds_min:  # Pnet is smaller than the smallest diesel power self.Pds_min
                    if  start_ds>=1 and (start_ds<=(self.Tdiesel-1)):
                        self.Pdsref=self.Pds_min
                        self.Start_ds=start_ds+1
                        self.Pldref=0
                        self.Pessref=self.Pds_min+Pnet
                        self.Pwdref=0
#                                 if self.Start_ds>=self.Tdiesel
#                                     self.Start_ds=0
#                                 #end
                    else:  ## diesel is OFF
#                                 self.Start_ds=1    # change 4
#                                 self.Pdsref=self.Pds_min
#                                 self.Pldref=0
                        self.Start_ds=0 
                        self.Pdsref=0 #(conventional load following control)
                        self.Pldref=-Pnet   # (conventional load following control)#self.Pldref is positive, shedding
                        self.Pessref=0 # ESS is still master
                        self.Pwdref=0
                            #end
                else:                   
                    if (-Pnet-self.Pds_max)<=0:  # self.Pds_min<-Pnet<self.Pds_max
                        self.Pessref=0
#                                 self.Pdsref=self.Pds_max  # to charge BESS back
                        self.Pdsref=-Pnet
                        self.Start_ds=start_ds+1
                        self.Pwdref=0
                        self.Pldref=0
#                                 if self.Start_ds>=self.Tdiesel
#                                     self.Start_ds=0
#                                 #end
                    else:              # -Pnet>self.Pds_max
                        self.Pessref=0
                        self.Pwdref=0
                        self.Pdsref=self.Pds_max
                        self.Start_ds=start_ds+1
                        self.Pldref=-Pnet-self.Pds_max
#                                 if self.Start_ds>=self.Tdiesel
#                                     self.Start_ds=0
#                                 #end
                    #end
             #end
    #end
            ## Power smoothing 
        elif Type==4:
            Pnet = -Pwind-PES+Pload  ## load larger than genertion
            self.Start_ds=start_ds+1
            if (Pnet-self.Pds_max)>=0: ## More, wind is controllable, diesel is off, ESS dep#ends
                if (Pnet-self.Pds_max)<-self.Pdis_max:      ## Discharge
                    self.Pdsref=self.Pds_max
                    self.Pldref=0
                    self.Pwdref=0
                    self.Pessref=-Pnet+self.Pds_max # discharge
                else:
                    self.Pdsref=self.Pds_max
                    self.Pldref=Pnet-self.Pds_max+self.Pdis_max
                    self.Pwdref=0
                    self.Pessref=self.Pdis_max  #discharge
                #end
            elif Pnet > self.Pds_min:
                self.Pdsref=Pnet
                self.Pldref=0
                self.Pwdref=0
                self.Pessref=0
            else:   # Pnet<self.Pds_min
                self.Pdsref=self.Pds_min
                if self.Start_ds>=self.Tdiesel:
                    self.Start_ds=0
                    self.Pdsref=0                   
                #end
    #                self.Pdsref=0.5
                    self.Pldref=0
                if (self.Pdsref-Pnet)<self.Pch_max:
                    self.Pwdref=0
                    self.Pessref=self.Pdsref-Pnet # charge
                    if self.Pessref>=0:
                        self.Pldref=0
                    else:
                        self.Pldref=-self.Pessref
                        self.Pessref=0
                    #end
                else:
                    self.Pwdref=-Pnet+self.Pdsref-self.Pch_max
                    self.Pessref=self.Pch_max   #charge
                #end
            #end
    #end
#end
