# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 15:49:31 2019

@author: csun26
"""
class Isldisp1:
    def _init_(self):
        self.SoC_max = 0.9   #95
        self.SoC_min = 0.3
        self.Pch_max = 3
        self.Pdis_max = -3  #-1.5
        self.Pds_min=0.6
        self.Pds_max=3
        self.Pwdref=0
        self.Tdiesel=4
        self.Pldref=0
        self.Pessref=0
        self.disp_mode=0     
        self.Pdsref=0
        self.Start_ds=0
		
    def Isldispatch1(self,Pwind,Pload,SoC,start_ds,Type,Disp_mode,SoC_ref):
        self.SoC_max = 0.9   #95
        self.SoC_min = 0.3
        self.Pch_max = 3
        self.Pdis_max = -3  #-1.5
        self.Pds_min=0.6
        self.Pds_max=3
        self.Pwdref=0
        self.Tdiesel=4
        self.Pldref=0
        self.Pessref=0
        self.disp_mode=0     
        self.Pdsref=0
        self.Start_ds=0
        ## Load following&cycle charge
        if Type==1:
            Pnet = Pwind-Pload
            if Pnet>=0 and Disp_mode==0:    # More, wind is controllable, diesel is off, ESS dep#ends
                    self.disp_mode=0
                    if SoC>=self.SoC_max:     # Charge is
                        self.Pwdref=Pnet        # self.Pwdref is positive
                        #self.Pessref=0
                        self.Pdsref=0
                        self.Pldref=0
                        self.Start_ds=0
                    else:     # SoC<self.SoC_max
                        if start_ds>=1 and (start_ds<=(self.Tdiesel-1)):
                            self.Pdsref=self.Pds_min
                            if (Pnet+self.Pdsref)<self.Pch_max:
                                # self.Pessref=Pnet+self.Pds_min
                                self.Pwdref=0
                                self.Pldref=0
                                self.Pdsref=self.Pds_min
                                self.Start_ds=start_ds+1
                                if self.Start_ds>=self.Tdiesel:
                                    self.Start_ds=0
                                #end
                            else:
                                # self.Pessref=self.Pch_max
                                self.Pwdref=Pnet+self.Pdsref-self.Pch_max
                                self.Pldref=0
                                self.Pdsref=self.Pds_min
                                self.Start_ds=start_ds+1
                                if self.Start_ds>=self.Tdiesel:
                                    self.Start_ds=0  # turn off diesel
                                #end
                            #end
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
                            #end
                         #end
                    #end
    #                  self.Pdsref=0.7
    #                  self.Pwdref=0
    #                  self.Pldref=0
    #                  self.Start_ds=1
            elif SoC>=self.SoC_min and Disp_mode==0:    ## Pnet<0, load is controllable, diesel on/off, self.SoC_min
                    self.disp_mode=0
                    if  start_ds>=1 and (start_ds<=(self.Tdiesel-1)):
                           self.Pdsref=self.Pds_min
                           Pnet=Pwind+self.Pds_min-Pload
                           if -Pnet<-self.Pdis_max:   # Pnet is smaller than largest discharge power
                        # # self.Pessref=Pnet   # # self.Pessref is negative
                                self.Pldref=0
                                self.Pdsref=self.Pds_min
                                self.Start_ds=start_ds+1
                                self.Pwdref=0
                                if self.Start_ds>=self.Tdiesel:
                                    self.Start_ds=0
                                #end
                           else:
                                self.Pldref=-Pnet+self.Pdis_max  #self.Pldref is positive
                                # self.Pessref=self.Pdis_max
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
                            # self.Pessref=Pnet   # # self.Pessref is negative
                                self.Pldref=0
                                self.Pdsref=0
                                self.Pwdref=0
                            else:                 ## Pnet is larger than the largest discharge power
                                self.Pldref=-Pnet+self.Pdis_max  #self.Pldref is positive
                                # self.Pessref=self.Pdis_max
                                self.Pdsref=0
                                self.Pwdref=0
                            #end
                    #end
    #                  self.Pdsref=0.2
    #                  self.Pwdref=0
    #                  self.Pldref=0
    #                  self.Start_ds=1
                
            elif SoC<self.SoC_min or Disp_mode==1:            ## SoC<self.SoC_min, diesel should be on
    #                  self.Pdsref=0.5
    #                  self.Pwdref=0
    #                  self.Pldref=0
    #                  self.Start_ds=1
                       self.disp_mode=1
                       if SoC>=self.SoC_min+0.5:   #Hysteresis control
                           self.disp_mode=0
                       #end
                       if -Pnet<self.Pds_min:  # Pnet is smaller than the smallest diesel power self.Pds_min
                            if  start_ds>=1 and (start_ds<=(self.Tdiesel-1)):
                                self.Pdsref=self.Pds_min
                                self.Start_ds=start_ds+1
                                self.Pldref=0
                                # self.Pessref=self.Pds_min-Pnet
                                self.Pwdref=0
#                                 if self.Start_ds>=self.Tdiesel
#                                     self.Start_ds=0
#                                     self.Pldref=-Pnet
#                                 #end
                            else:
                                self.Start_ds=1    # change 4
                                self.Pdsref=self.Pds_min
                                self.Pldref=0
#                                 self.Start_ds=0
#                                 self.Pldref=-Pnet   #self.Pldref is positive, shedding
                                # self.Pessref=0 # ESS is still master
#                                 self.Pdsref=0
                                self.Pwdref=0
                            #end
                       else:                   
                            if (-Pnet-self.Pds_max)<=0:  # self.Pds_min<-Pnet<self.Pds_max
                                # self.Pessref=0
                                self.Pdsref=self.Pds_max  # to charge BESS back
#                                 self.Pdsref=-Pnet
                                self.Start_ds=start_ds+1
                                self.Pwdref=0
                                self.Pldref=0
#                                 if self.Start_ds>=self.Tdiesel
#                                     self.Start_ds=0
#                                 #end
                            else:              # -Pnet>self.Pds_max
                                # self.Pessref=0
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
            Pnet = -Pwind+Pload
            self.Start_ds=1
            if (Pnet-self.Pds_max) >=0:## More, wind is controllable, diesel is off, ESS dep#ends
                if (Pnet-self.Pds_max)<-self.Pdis_max:      ## Discharge
                    self.Pdsref=self.Pds_max
                    self.Pldref=0
                    self.Pwdref=0
                else:
                    self.Pdsref=self.Pds_max
                    self.Pldref=Pnet-self.Pds_max+self.Pdis_max
                    self.Pwdref=0
                #end
            elif Pnet > self.Pds_min:
                    self.Pdsref=Pnet
                    self.Pldref=0
                    self.Pwdref=0
            else:
                self.Pdsref=self.Pds_min
                self.Pldref=0
                if (self.Pds_min-Pnet)<self.Pch_max:
                    self.Pwdref=0
                else:
                    self.Pwdref=-Pnet+self.Pds_min-self.Pch_max
                #end
            #end
         ## Power smoothing & cycle charging
        elif Type==2:
             if (SoC>=0.45 and SoC<=SoC_ref) or Disp_mode==2: ##should disable or in type D
                self.disp_mode=2
                Pnet = -Pwind+Pload
                self.Start_ds=1
                if (Pnet-self.Pds_max) >=0: ## More, wind is controllable, diesel is off, ESS dep#ends
                    if (Pnet-self.Pds_max)<-self.Pdis_max:      ## Discharge
                        self.Pdsref=self.Pds_max
                        self.Pldref=0
                        self.Pwdref=0
                    else:
                        self.Pdsref=self.Pds_max
                        self.Pldref=Pnet-self.Pds_max+self.Pdis_max
                        self.Pwdref=0
                    #end
                elif Pnet > self.Pds_min:
                        self.Pdsref=Pnet
                        self.Pldref=0
                        self.Pwdref=0
                else:   # Pnet<self.Pds_min
                    self.Pdsref=self.Pds_min
        #                self.Pdsref=0.5
                    self.Pldref=0
                    if (self.Pds_min-Pnet)<self.Pch_max:
                        self.Pwdref=0
                    else:
                        self.Pwdref=-Pnet+self.Pds_min-self.Pch_max 
                    #end
                #end
             else:
               Pnet=Pwind-Pload
               if Pnet>=0 and Disp_mode==0:    # More, wind is controllable, diesel is off, ESS dep#ends
                    self.disp_mode=0
                    if SoC>=self.SoC_max:     # Charge is
                        self.Pwdref=Pnet        # self.Pwdref is positive
                        #self.Pessref=0
                        self.Pdsref=0
                        self.Pldref=0
                        self.Start_ds=0
                    else:     # SoC<self.SoC_max
                        if start_ds>=1 and (start_ds<=(self.Tdiesel-1)):
                            self.Pdsref=self.Pds_min
                            if (Pnet+self.Pdsref)<self.Pch_max:
                                # self.Pessref=Pnet+self.Pds_min
                                self.Pwdref=0
                                self.Pldref=0
                                self.Pdsref=self.Pds_min
                                self.Start_ds=start_ds+1
                                if self.Start_ds>=self.Tdiesel:
                                    self.Start_ds=0
                                #end
                            else:
                                # self.Pessref=self.Pch_max
                                self.Pwdref=Pnet+self.Pdsref-self.Pch_max
                                self.Pldref=0
                                self.Pdsref=self.Pds_min
                                self.Start_ds=start_ds+1
                                if self.Start_ds>=self.Tdiesel:
                                    self.Start_ds=0  # turn off diesel
                                #end
                            #end
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
                            #end
                         #end
                    #end
    #                  self.Pdsref=0.7
    #                  self.Pwdref=0
    #                  self.Pldref=0
    #                  self.Start_ds=1
               elif SoC>=self.SoC_min and Disp_mode==0:    ## Pnet<0, load is controllable, diesel on/off, self.SoC_min
                    self.disp_mode=0
                    if  start_ds>=1 and (start_ds<=(self.Tdiesel-1)):
                           self.Pdsref=self.Pds_min
                           Pnet=Pwind+self.Pds_min-Pload
                           if -Pnet<-self.Pdis_max:   # Pnet is smaller than largest discharge power
                        # # self.Pessref=Pnet   # # self.Pessref is negative
                                self.Pldref=0
                                self.Pdsref=self.Pds_min
                                self.Start_ds=start_ds+1
                                self.Pwdref=0
                                if self.Start_ds>=self.Tdiesel:
                                    self.Start_ds=0
                                #end
                           else:
                                self.Pldref=-Pnet+self.Pdis_max  #self.Pldref is positive
                                # self.Pessref=self.Pdis_max
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
                            # self.Pessref=Pnet   # # self.Pessref is negative
                                self.Pldref=0
                                self.Pdsref=0
                                self.Pwdref=0
                            else:                 ## Pnet is larger than the largest discharge power
                                self.Pldref=-Pnet+self.Pdis_max  #self.Pldref is positive
                                # self.Pessref=self.Pdis_max
                                self.Pdsref=0
                                self.Pwdref=0
                            #end
                    #end
    #                  self.Pdsref=0.2
    #                  self.Pwdref=0
    #                  self.Pldref=0
    #                  self.Start_ds=1
                
               elif SoC<self.SoC_min or Disp_mode==1:            ## SoC<self.SoC_min, diesel should be on
    #                  self.Pdsref=0.5
    #                  self.Pwdref=0
    #                  self.Pldref=0
    #                  self.Start_ds=1
                       self.disp_mode=1
                       if SoC>=self.SoC_min+0.2:   #Hysteresis control
                           self.disp_mode=0
                       #end
                       if -Pnet<self.Pds_min:  # Pnet is smaller than the smallest diesel power self.Pds_min
                            if  start_ds>=1 and (start_ds<=(self.Tdiesel-1)):
                                self.Pdsref=self.Pds_min
                                self.Start_ds=start_ds+1
                                self.Pldref=0
                                # self.Pessref=self.Pds_min-Pnet
                                self.Pwdref=0
#                                 if self.Start_ds>=self.Tdiesel
#                                     self.Start_ds=0
#                                     self.Pldref=-Pnet
#                                 #end
                            else:
                                self.Start_ds=start_ds+1    # change 4
                                self.Pdsref=self.Pds_min
                                self.Pldref=0
#                                 self.Start_ds=0
#                                 self.Pldref=-Pnet   #self.Pldref is positive, shedding
                                # self.Pessref=0 # ESS is still master
#                                 self.Pdsref=0
                                self.Pwdref=0
                            #end
                       else:                   
                            if (-Pnet-self.Pds_max)<=0:  # self.Pds_min<-Pnet<self.Pds_max
                                # self.Pessref=0
                                self.Pdsref=self.Pds_max  # to charge BESS back
#                                 self.Pdsref=-Pnet
                                self.Start_ds=start_ds+1
                                self.Pwdref=0
                                self.Pldref=0
#                                 if self.Start_ds>=self.Tdiesel
#                                     self.Start_ds=0
#                                 #end
                            else:              # -Pnet>self.Pds_max
                                # self.Pessref=0
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
         ## Load following   
        elif Type==3:
            Pnet = Pwind-Pload
            if Pnet>=0:    # More, wind is controllable, diesel is off, ESS dep#ends
                    if SoC>=self.SoC_max:     # Charge is
                        self.Pwdref=Pnet        # self.Pwdref is positive
                        #self.Pessref=0
                        self.Pdsref=0
                        self.Pldref=0
                        self.Start_ds=0
                    else:     # SoC<self.SoC_max
                        if start_ds>=1 and (start_ds<=(self.Tdiesel-1)):
                            self.Pdsref=self.Pds_min
                            if (Pnet+self.Pdsref)<self.Pch_max:
                                # self.Pessref=Pnet+self.Pds_min
                                self.Pwdref=0
                                self.Pldref=0
                                self.Pdsref=self.Pds_min
                                self.Start_ds=start_ds+1
                                if self.Start_ds>=self.Tdiesel:
                                    self.Start_ds=0
                                #end
                            else:
                                # self.Pessref=self.Pch_max
                                self.Pwdref=Pnet+self.Pdsref-self.Pch_max
                                self.Pldref=0
                                self.Pdsref=self.Pds_min
                                self.Start_ds=start_ds+1
                                if self.Start_ds>=self.Tdiesel:
                                    self.Start_ds=0  # turn off diesel
                                #end
                            #end
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
                            #end
                         #end
                    #end
    #                  self.Pdsref=0.7
    #                  self.Pwdref=0
    #                  self.Pldref=0
    #                  self.Start_ds=1
            elif SoC>=self.SoC_min:   ## Pnet<0, load is controllable, diesel on/off, self.SoC_min
                    if  start_ds>=1 and (start_ds<=(self.Tdiesel-1)):
                           self.Pdsref=self.Pds_min
                           Pnet=Pwind+self.Pds_min-Pload
                           if -Pnet<-self.Pdis_max:   # Pnet is smaller than largest discharge power
                        # # self.Pessref=Pnet   # # self.Pessref is negative
                                self.Pldref=0
                                self.Pdsref=self.Pds_min
                                self.Start_ds=start_ds+1
                                self.Pwdref=0
                                if self.Start_ds>=self.Tdiesel:
                                    self.Start_ds=0
                                #end
                           else:
                                self.Pldref=-Pnet+self.Pdis_max  #self.Pldref is positive
                                # self.Pessref=self.Pdis_max
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
                            # self.Pessref=Pnet   # # self.Pessref is negative
                                self.Pldref=0
                                self.Pdsref=0
                                self.Pwdref=0
                            else:                 ## Pnet is larger than the largest discharge power
                                self.Pldref=-Pnet+self.Pdis_max  #self.Pldref is positive
                                # self.Pessref=self.Pdis_max
                                self.Pdsref=0
                                self.Pwdref=0
                            #end
                    #end
    #                  self.Pdsref=0.2
    #                  self.Pwdref=0
    #                  self.Pldref=0
    #                  self.Start_ds=1
                
            elif SoC<self.SoC_min:            ## SoC<self.SoC_min, diesel should be on
    #                  self.Pdsref=0.5
    #                  self.Pwdref=0
    #                  self.Pldref=0
    #                  self.Start_ds=1
                     if -Pnet<self.Pds_min:  # Pnet is smaller than the smallest diesel power self.Pds_min
                            if  start_ds>=1 and (start_ds<=(self.Tdiesel-1)):
                                self.Pdsref=self.Pds_min
                                self.Start_ds=start_ds+1
                                self.Pldref=0
                                # self.Pessref=self.Pds_min-Pnet
                                self.Pwdref=0
#                                 if self.Start_ds>=self.Tdiesel
#                                     self.Start_ds=0
#                                     self.Pldref=-Pnet
#                                 #end
                            else:
#                                 self.Start_ds=1    # change 4
#                                 self.Pdsref=self.Pds_min
#                                 self.Pldref=0
                                self.Start_ds=0
                                self.Pldref=-Pnet   #self.Pldref is positive, shedding
#                                 self.Pessref=0 # ESS is still master
                                self.Pdsref=0
                                self.Pwdref=0
                            #end
                     else:                   
                            if (-Pnet-self.Pds_max)<=0:  # self.Pds_min<-Pnet<self.Pds_max
                                # self.Pessref=0
#                                 self.Pdsref=self.Pds_max  # to charge BESS back
                                self.Pdsref=-Pnet
                                self.Start_ds=start_ds+1
                                self.Pwdref=0
                                self.Pldref=0
#                                 if self.Start_ds>=self.Tdiesel
#                                     self.Start_ds=0
#                                 #end
                            else:              # -Pnet>self.Pds_max
                                # self.Pessref=0
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
            
#end