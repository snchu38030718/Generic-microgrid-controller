# -*- coding: utf-8 -*-
"""
# Steady-state dispatch in islanded mode
Created on Tue Jan  8 15:49:31 2019

@author: csun26
"""
class Isldisp1:
    def _init_(self):
        self.SoC_max = 0.9   #95
        self.SoC_min = 0.32
        self.Pch_max = 1
        self.Pdis_max = -1  #-1.5
        self.Pds_min=0.3
        self.Pds_max=1
        self.Pwdref=0
        self.Tdiesel=4
        self.Pldref=0
        self.Pessref=0
        self.disp_mode=0     
        self.Pdsref=0
        self.Start_ds=0
		
    def Isldispatch1(self,Prer,Pload,SoC,start_diesel,Type,Disptch_mode,SoC_ref):
        self.SoC_max = 0.9   #95
        self.SoC_min = 0.32
        self.SoCd=self.SoC_min+0.1 # The lower bound for cycle-charging control
        self.SoCup=self.SoC_min+0.5 # The upper bound for cycle-charging control
        self.SoCref1=0.45     # The lower bound of power smoothing control
        self.Pch_max = 1
        self.Pdis_max = -1  #-1.5
        self.Pds_min=0.3
        self.Pds_max=1
        self.Pwdref=0
        self.Tdiesel=4
        self.Pldref=0
        self.Pessref=0
        self.disp_mode=0     
        self.Pdsref=0
        self.Start_ds=0
        
        ## Load following&cycle charge
        if Type==1:
            Pnet = Prer-Pload
            if Pnet>=0 and Disptch_mode==0:    # Generation more than load, wind is controllable, diesel is off, ESS dep#ends
                    self.disp_mode=0                       # Stayed at Mode 0
                    if SoC>=self.SoC_max:         # SoC is larger or equal to maximum SoC
                        self.Prerref=Pnet        # Wind curtail power is the net power
                        self.Pdsref=0           # Diesel is OFF
                        self.Pldref=0           # Power reference of load is 0
                        self.Start_ds=0         # Diesel kept OFF
                    else:     # SoC<self.SoC_max (SoC is small than Maximum SoC)
                        if start_diesel>=1 and (start_diesel<=(self.Tdiesel-1)): # The number of intervals of diesel ON is between 1 and self.Tdiesel-1
                            self.Pdsref=self.Pds_min # Power reference of diesel is at mimimum
                            if (Pnet+self.Pdsref)<self.Pch_max: # Net power mismatch plus diesel power is less than maximum charge power of ESS
                                # Pessref=Pnet+self.Pds_min # ESS will be charged at Pnet+self.Pds_min
                                self.Prerref=0 # Wind power curtailment is 0
                                self.Pldref=0 # Load power shedding is 0
                                self.Pdsref=self.Pds_min
                                self.Start_ds=start_diesel+1 # The number of intevals that Diesel ON is increased by one
                                if self.Start_ds>=self.Tdiesel: # If self.Start_ds larger than the minimum required time
                                    self.Start_ds=0      # Diesel turned OFF
                                #end
                            else:                     # Diesel turned OFF
                                self.Prerref=Pnet+self.Pdsref-self.Pch_max # ESS been charged at the maximum charge power
                                self.Pldref=0 # Wind power curtailed to maintain power balance
                                self.Pdsref=self.Pds_min # Load shed is zero
                                self.Start_ds=start_diesel+1
                                if self.Start_ds>=self.Tdiesel:
                                    self.Start_ds=0  # Diesel turned OFF
                                #end
                            #end
                        else:                       # Diesel is OFF, or the ON time of diesel larger than minimum
                            self.Start_ds=0            # Diesel OFF
                            if Pnet<self.Pch_max:        # Net power smaller than maximum charge power of ESS
                                # Pessref=Pnet     # Charge ESS with net power
                                self.Prerref=0
                                self.Pdsref=0
                                self.Pldref=0
                            else:                   # Net power larger than maximum charge power of ESS
                                # Pessref=self.Pch_max  # Charge ESS with net power
                                self.Prerref=Pnet-self.Pch_max # Wind power curtailed to maintain power balance
                                self.Pdsref=0
                                self.Pldref=0 
                            #end
                         #end
                    #end
            elif SoC>=self.SoC_min and Disptch_mode==0:    # Pnet<0 (load larger than generation), SoC>=self.SoC_min and Disptch_mode is 0
                    self.disp_mode=0                 # self.disp_mode kept at 0
                    if  start_diesel>=1 and (start_diesel<=(self.Tdiesel-1)): # The number of intervals of diesel ON is between 1 and self.Tdiesel-1
                           self.Pdsref=self.Pds_min
                           Pnet=Prer+self.Pds_min-Pload # self.Pdsref=self.Pds_min, readjust Pnet to include self.Pds_min
                           if -Pnet<-self.Pdis_max:   # Pnet is smaller than largest discharge power
                                # Pessref=Pnet   # Pessref is negative
                                self.Pldref=0        # load shedding is 0
                                self.Pdsref=self.Pds_min  # diesel output minimum
                                self.Start_ds=start_diesel+1
                                self.Prerref=0        # wind power curtail is 0
                                if self.Start_ds>=self.Tdiesel:
                                    self.Start_ds=0
                                #end
                           else:
                                self.Pldref=-Pnet+self.Pdis_max  # Load shed to maintain power balance
                                # Pessref=self.Pdis_max      # ESS discharge power at its maximum
                                self.Pdsref=self.Pds_min
                                self.Start_ds=start_diesel+1
                                self.Prerref=0               # Wind curtail is 0
                                if self.Start_ds>=self.Tdiesel:
                                    self.Start_ds=0
                                #end
                           #end
                    else: # Diesel is OFF, or the ON time of diesel larger than minimum
                            self.Start_ds=0 # Diesel OFF
                            if -Pnet<-self.Pdis_max:   # Pnet is smaller than largest discharge power
                                # Pessref=Pnet   # ESS Power reference is net power
                                self.Pldref=0
                                self.Pdsref=0
                                self.Prerref=0
                            else:                 # Pnet is larger than the largest discharge power
                                self.Pldref=-Pnet+self.Pdis_max  # Load shed to maintain power balance
                                # Pessref=self.Pdis_max # ESS will discharge power at its maximum
                                self.Pdsref=0
                                self.Prerref=0
                            #end
                    #end             
            elif SoC<self.SoC_min or Disptch_mode==1:            # Pnet<0(load larger than generation), SoC<self.SoC_min, diesel kept ON (Disptch_mode==1)
                     self.disp_mode=1         # self.disp_mode kept at 1
                     if SoC>=self.SoCup:        # self.SoCup=self.SoC_min+0.5, the cycle-charging upper bound
                         self.disp_mode=0     # Recede cycle-charging mode
                       #end
                     if -Pnet<self.Pds_min:  # Pnet is smaller than self.Pds_min
                            if  start_diesel>=1 and (start_diesel<=(self.Tdiesel-1)): # The number of intervals of diesel ON is between 1 and self.Tdiesel-1
                                self.Pdsref=self.Pds_min # Diesel power is at minimum
                                self.Start_ds=start_diesel+1
                                self.Pldref=0 # Load shedding is 0
                                # Pessref=self.Pds_min-Pnet # ESS to maintain power balance
                                self.Prerref=0 # Wind curtailment is 0
                            else:
                                self.Start_ds=1    # Keep at 1, for cycle-charging
                                self.Pdsref=self.Pds_min # Diesel power is at minimum
                                self.Pldref=0 # Load shedding is 0
                                self.Prerref=0
                            #end
                     else:    # Pnet is larger than self.Pds_min               
                            if (-Pnet-self.Pds_max)<=0:  # self.Pds_min<-Pnet<self.Pds_max
                                # Pessref=0
                                self.Pdsref=self.Pds_max  # Diesel at maximum to charge BESS back
                                self.Start_ds=start_diesel+1
                                self.Prerref=0        # Wind curtailment is 0
                                self.Pldref=0        # Load shedding is 0
                            else:                 # -Pnet>self.Pds_max
                                # Pessref=0      # ESS power reference is 0
                                self.Prerref=0
                                self.Pdsref=self.Pds_max
                                self.Start_ds=start_diesel+1
                                self.Pldref=-Pnet-self.Pds_max # Load shed to avoid ESS discharge
                            #end
                     #end
            #end
        ## Power smoothing
        elif Type==4:
            Pnet = -Prer+Pload    # Net power is calculated as load minus generation
            self.Start_ds=1             # Diesel is ON all the time
            if (Pnet-self.Pds_max) >=0:   # Net power larger than maximum diesel power
                if (Pnet-self.Pds_max)<-self.Pdis_max: # (Net power with maximum diesel power) smaller than largest discharge power
                    self.Pdsref=self.Pds_max # Diesel output maximum power
                    #self.Pldref=0       # ESS to maintain power balance
                    self.Pldref=Pnet-self.Pds_max # Load to maintain power balance
                    self.Prerref=0
                else:                # Net power smaller than maximum diesel power
                    self.Pdsref=self.Pds_max # Diesel output maxium power
                    self.Pldref=Pnet-self.Pds_max+self.Pdis_max # Load shed to maintain power balance
                    self.Prerref=0
                #end
            elif Pnet > self.Pds_min: # self.Pds_min<Pnet<self.Pds_max
                    self.Pdsref=Pnet # Diesel used to balance net power
                    self.Pldref=0
                    self.Prerref=0
            else: # Pnet<self.Pds_min
                self.Pdsref=self.Pds_min # Diesel output minmum diesel power
                self.Pldref=0 # Load shedding is 0
                if (self.Pds_min-Pnet)<self.Pch_max: # Remaining power to be balanced smaller than maximum charging power
                    self.Prerref=0
                else:
                    self.Prerref=-Pnet+self.Pds_min-self.Pch_max # ESS charged at maximum charging power,Wind curtailed
                #end
            #end
         ## Power smoothing & cycle charging
        elif Type==2:
             if ((SoC>=self.SoCref1 and SoC<=SoC_ref) and Disptch_mode!=1) or Disptch_mode==2: ##should disable or in type D
                self.disp_mode=2 # self.disp_mode locked at mode #2: power smoothing mode
                Pnet = -Prer+Pload # Net power mismatch is calculated as load minus generation
                self.Start_ds=1          # Diesel always ON
                #########################    # Judge sub-control-mode based on SoC
                if SoC<=self.SoCd:   # self.SoCd=self.SoC_min+0.1 (0.32)
                    self.disp_mode=1      # Go to cycle-charging mode
                    self.Start_ds=0       # Number of interval diesel ON begins at 0
                #end
                if  SoC>=self.SoCup:       # self.SoCup=self.SoC_min+0.5 (0.72)
                    self.disp_mode=0     # Go to load-following mode
                    self.Start_ds=0      # Number of interval diesel ON begins at 0
                #end
                ########################
                
                if (Pnet-self.Pds_max) >=0: # Net power larger than maximum diesel power
                    if (Pnet-self.Pds_max)<-self.Pdis_max:     # (Net power with maximum diesel power) smaller than largest discharge power
                        self.Pdsref=self.Pds_max # Diesel outputs maximum power
                        self.Pldref=0
                        self.Prerref=0
                    else: # Net power smaller than maximum diesel power
                        self.Pdsref=self.Pds_max # Diesel output maxium power  
                        self.Pldref=Pnet-self.Pds_max+self.Pdis_max # Load shed to maintain power balance
                        self.Prerref=0
                    #end
                elif Pnet > self.Pds_min: # self.Pds_min<Pnet<self.Pds_max
                        self.Pdsref=Pnet  # Diesel used to balance net power
                        self.Pldref=0
                        self.Prerref=0
                else:   # Pnet<self.Pds_min
                    self.Pdsref=self.Pds_min # Diesel output minmum diesel power
                    self.Pldref=0
                    if (self.Pds_min-Pnet)<self.Pch_max: # Remaining power to be balanced smaller than maximum charging power
                        self.Prerref=0 # wind power curtail is 0
                    else: # Remaining power larger than maximum charging power
                        self.Prerref=-Pnet+self.Pds_min-self.Pch_max # Wind curtailed to maintain power balance, ESS charged at maximum charging power
                    #end
                #end
             else: ## Not in power-smoothing: load following or cycle charging
               Pnet=Prer-Pload # Pnet calculated as generation minus load
               if Pnet>=0 and Disptch_mode==0:    # Load larger than generation and Disptch_mode=0
                    self.disp_mode=0 # Disptch_mode kept at 0
                    if SoC>=self.SoC_max:      # # SoC is larger or equal to maximum SoC
                        self.Prerref=Pnet        # Wind curtail power is the net power 
                        #Pessref=0 # Power refernece of ESS is 0
                        self.Pdsref=0 # Diesel is OFF
                        self.Pldref=0 # Power reference of load is 0
                        self.Start_ds=0 # Diesel kept OFF
                    else:     # SoC<self.SoC_max
                        if start_diesel>=1 and (start_diesel<=(self.Tdiesel-1)): # The number of intervals of diesel ON is between 1 and self.Tdiesel-1
                            self.Pdsref=self.Pds_min # Power reference of diesel is at mimimum
                            if (Pnet+self.Pdsref)<self.Pch_max: # Net power mismatch plus diesel power is less than maximum charge power of ESS
                                # Pessref=Pnet+self.Pds_min # ESS will be charged at Pnet+self.Pds_min
                                self.Prerref=0 # Wind power curtailment is 0
                                self.Pldref=0 # Load power shedding is 0
                                self.Pdsref=self.Pds_min
                                self.Start_ds=start_diesel+1
                            else: # (Pnet+self.Pdsref)>=self.Pch_max
                                # Pessref=self.Pch_max # ESS charged at the maximum charge power
                                self.Prerref=Pnet+self.Pdsref-self.Pch_max # Wind power curtailed to maintain power balance
                                self.Pldref=0 # Load shed is zero
                                self.Pdsref=self.Pds_min
                                self.Start_ds=start_diesel+1
                            #end
                        else: # Diesel is OFF, or the ON time of diesel larger than minimum
                            self.Start_ds=0    # Diesel OFF
                            if Pnet<self.Pch_max:  # Net power smaller than maximum charge power of ESS
                                # Pessref=Pnet  # Charge ESS with net power
                                self.Prerref=0
                                self.Pdsref=0
                                self.Pldref=0
                            else:  # Net power larger than maximum charge power of ESS
                                # Pessref=self.Pch_max # Charge ESS with net power
                                self.Prerref=Pnet-self.Pch_max # Wind power curtailed to maintain power balance
                                self.Pdsref=0
                                self.Pldref=0 
                            #end
                         #end
                    #end
               elif Pnet<0 and SoC>=self.SoC_min and Disptch_mode==0:    # Load smaller than generation and SoC>=self.SoC_min
                    self.disp_mode=0 # Disptch_mode kept at 0
                    if  start_diesel>=1 and (start_diesel<=(self.Tdiesel-1)): # The number of intervals of diesel ON is between 1 and self.Tdiesel-1
                           self.Pdsref=self.Pds_min
                           Pnet=Prer+self.Pds_min-Pload # self.Pdsref=self.Pds_min, readjust Pnet to include self.Pds_min
                           if -Pnet<-self.Pdis_max:   # Pnet is smaller than largest discharge power
                                #  Pessref=Pnet   # # Pessref is negative
                                self.Pldref=0
                                self.Pdsref=self.Pds_min
                                self.Start_ds=start_diesel+1
                                self.Prerref=0
                           else:
                                self.Pldref=-Pnet+self.Pdis_max  # Load shed to maintain power balance
                                # Pessref=self.Pdis_max # ESS discharge power at its maximum
                                self.Pdsref=self.Pds_min
                                self.Start_ds=start_diesel+1
                                self.Prerref=0
                           #end
                    else: # Diesel is OFF, or the ON time of diesel larger than minimum
                            self.Start_ds=0     # Diesel OFF
                            if -Pnet<-self.Pdis_max:   # Pnet is smaller than largest discharge power
                               # Pessref=Pnet   # ESS Power reference is net power
                                self.Pldref=0
                                self.Pdsref=0
                                self.Prerref=0
                            else:                 # Pnet is larger than the largest discharge power
                                self.Pldref=-Pnet+self.Pdis_max  #self.Pldref is positive
                                # Pessref=self.Pdis_max # ESS will discharge power at its maximum
                                self.Pdsref=0
                                self.Prerref=0
                            #end
                    #end               
               elif (Pnet<0 and SoC<self.SoC_min) or Disptch_mode==1:   ## Load larger than generation, SoC<self.SoC_min, cycle charging mode
                     self.disp_mode=1 # self.disp_mode kept at 1, cycle-charging mode
                     if SoC>=self.SoCup:                # Hysteresis control, self.SoCup=self.SoC_min+0.5
                         self.disp_mode=0 # Go to load following control
                       #end
                     if -Pnet<self.Pds_min:  # Pnet is smaller than the smallest diesel power self.Pds_min
                            if  start_diesel>=1 and (start_diesel<=(self.Tdiesel-1)):
                                self.Pdsref=self.Pds_min # Diesel power is at minimum
                                self.Start_ds=start_diesel+1
                                self.Pldref=0
                                # Pessref=self.Pds_min-Pnet # ESS to maintain power balance
                                self.Prerref=0
                            else: # Diesel is OFF or ON time larger than self.Tdiesel
                                self.Start_ds=start_diesel+1    # change 4
                                self.Pdsref=self.Pds_min
                                self.Pldref=0
                                self.Prerref=0
                            #end
                     else:  # Pnet is larger than self.Pds_min                    
                            if (-Pnet-self.Pds_max)<=0:  # self.Pds_min<-Pnet<self.Pds_max
                                self.Pdsref=self.Pds_max  # Diesel output maximum to charge BESS back
                                self.Start_ds=start_diesel+1
                                self.Prerref=0
                                self.Pldref=0

                            else:              # -Pnet>self.Pds_max
                                # Pessref=0   # ESS power reference is 0
                                self.Prerref=0
                                self.Pdsref=self.Pds_max # Diesel at Maximum
                                self.Start_ds=start_diesel+1 # Diesel ON interval increased by one
                                self.Pldref=-Pnet-self.Pds_max # Load shed to avoid ESS discharge
                            #end
                     #end
               #end 
             #end
         ## Load following without cycle charging
        elif Type==3:
            Pnet = Prer-Pload  # Net power calculated as generation minus load
            if Pnet>=0:    # # Load more than generation
                    if SoC>=self.SoC_max:     # Charge is
                        self.Prerref=Pnet    # Wind curtail power is the net power
                        #Pessref=0
                        self.Pdsref=0       # Diesel is OFF
                        self.Pldref=0       # Power reference of load is 0
                        self.Start_ds=0     # Diesel kept OFF
                    else:     # SoC<self.SoC_max
                        if start_diesel>=1 and (start_diesel<=(self.Tdiesel-1)): # The number of intervals of diesel ON is between 1 and Maximum
                            self.Pdsref=self.Pds_min # Power reference of diesel is at mimimum
                            if (Pnet+self.Pdsref)<self.Pch_max: # Net power mismatch plus diesel power is less than maximum charge power of ESS
                                # Pessref=Pnet+self.Pds_min # ESS will be charged at Pnet+self.Pds_min
                                self.Prerref=0 # Wind power curtailment is 0
                                self.Pldref=0 # Load power shedding is 0
                                self.Pdsref=self.Pds_min
                                self.Start_ds=start_diesel+1
                                if self.Start_ds>=self.Tdiesel:
                                    self.Start_ds=0
                                #end
                            else: # (Pnet+self.Pdsref)>=self.Pch_max
                                # Pessref=self.Pch_max # ESS been charged at the maximum charge power
                                self.Prerref=Pnet+self.Pdsref-self.Pch_max # Wind power curtailed to maintain power balance
                                self.Pldref=0 # Load shed is zero
                                self.Pdsref=self.Pds_min
                                self.Start_ds=start_diesel+1
                                if self.Start_ds>=self.Tdiesel:
                                    self.Start_ds=0  
                                #end
                            #end
                        else: # Diesel is OFF, or the ON time of diesel larger than minimum
                            self.Start_ds=0 # Diesel OFF
                            if Pnet<self.Pch_max:  # Net power smaller than maximum charge power of ESS
                                # Pessref=Pnet # Charge ESS with net power
                                self.Prerref=0
                                self.Pdsref=0
                                self.Pldref=0
                            else: # Net power larger than maximum charge power of ESS
                                # Pessref=self.Pch_max # Charge ESS with net power
                                self.Prerref=Pnet-self.Pch_max # Wind power curtailed to maintain power balance
                                self.Pdsref=0
                                self.Pldref=0 
                            #end
                         #end
                    #end
            elif SoC>=self.SoC_min:   ## Pnet<0(load larger than generation), and SoC>=self.SoC_min
                    if  start_diesel>=1 and (start_diesel<=(self.Tdiesel-1)): # The number of intervals of diesel ON is between 1 and Maximum
                           self.Pdsref=self.Pds_min
                           Pnet=Prer+self.Pds_min-Pload # self.Pdsref=self.Pds_min, readjust Pnet to include self.Pds_min
                           if -Pnet<-self.Pdis_max:   # Pnet is smaller than largest discharge power
                                # Pessref=Pnet   # ESS discharged power at Pnet
                                self.Pldref=0
                                self.Pdsref=self.Pds_min  # diesel run at minimum
                                self.Start_ds=start_diesel+1 # Number of interval diesel ON increased by one
                                self.Prerref=0 # wind power curtail is 0
                                if self.Start_ds>=self.Tdiesel: # Number of interval diesel ON larger than self.Tdiesel
                                    self.Start_ds=0
                                #end
                           else:
                                self.Pldref=-Pnet+self.Pdis_max  # Load shed to maintain power balance
                                # Pessref=self.Pdis_max # ESS discharge power at its maximum
                                self.Pdsref=self.Pds_min
                                self.Start_ds=start_diesel+1
                                self.Prerref=0
                                if self.Start_ds>=self.Tdiesel:
                                    self.Start_ds=0
                                #end
                           #end
                    else:
                            self.Start_ds=0
                            if -Pnet<-self.Pdis_max:   # Pnet is smaller than largest discharge power
                                # Pessref=Pnet   # ESS Power reference is net power
                                self.Pldref=0
                                self.Pdsref=0
                                self.Prerref=0
                            else:                 # Pnet is larger than the largest discharge power
                                self.Pldref=-Pnet+self.Pdis_max  # Load shed to maintain power balance
                                # Pessref=self.Pdis_max # ESS will discharge power at its maximum
                                self.Pdsref=0
                                self.Prerref=0
                            #end
                    #end           
            elif SoC<self.SoC_min:            ## SoC<self.SoC_min, ESS will not discharge any more
                     if -Pnet<self.Pds_min:  # Pnet is smaller than the smallest diesel power self.Pds_min
                            if  start_diesel>=1 and (start_diesel<=(self.Tdiesel-1)):
                                self.Pdsref=self.Pds_min # Diesel power is at minimum
                                self.Start_ds=start_diesel+1
                                self.Pldref=0 # Load shedding is 0
                                # Pessref=self.Pds_min-Pnet # ESS to maintain power balance
                                self.Prerref=0
                            else: # Diesel is OFF, or ON time larger than self.Tdiesel
                                self.Start_ds=0
                                self.Pldref=-Pnet   # Load shed to maintain power balance
#                               Pessref=0 # ESS power is zero
                                self.Pdsref=0
                                self.Prerref=0
                            #end
                     else:                   
                            if (-Pnet-self.Pds_max)<=0:  # self.Pds_min<-Pnet<self.Pds_max
                                # Pessref=0        # ESS power reference at 0
                                self.Pdsref=-Pnet      # Diesel used to balance net power
                                self.Start_ds=start_diesel+1 # Number of interval diesel ON increased by one
                                self.Prerref=0
                                self.Pldref=0
                            else:              # -Pnet>self.Pds_max
                                # Pessref=0 # ESS power reference at 0
                                self.Prerref=0 # Wind power reference at 0
                                self.Pdsref=self.Pds_max # Diesel output maximum
                                self.Start_ds=start_diesel+1
                                self.Pldref=-Pnet-self.Pds_max # Load shed to maintain power balance
                            #end
                     #end
            #end
        #end
            
#end
