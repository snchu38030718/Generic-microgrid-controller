# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 18:22:55 2019

@author: buaa_
"""

# Author: Ilja Novickij

###############################################################################
# Imports

#import array
#import PID
#import Unplan
##import Dispatch
#
#import Isldisp
#import Gridisp
#import Store

import os
import time
import numpy as np
import WandQ1
import Distribution
import Griddisp1
import Isldisp1
import Unplan1

from microgrid import Microgrid
###############################################################################
# OS checks and setup 
try:
    machine_name = os.uname()[1]
except AttributeError:
    print('Not running on controller!')
    pi = False
else:
    if machine_name == 'ugcpi':
        print('Running on correct machine!')
        pi = True
    else:
        print('Not running on controller!')
        pi = False
        
###############################################################################
# Main Code

m  = Microgrid()
#command = array.array('d',[])
#for i in range(1):
#    command.append(1.0)
init_time=time.time()


###### Islanded or grid-connected or unplan####
island=0
emg=0


############### input signals##################

while 1:
    start_time = time.time()
    command=list(m.e.status())
    spent_time=time.time()-init_time




#Pwdf=1 command[0]
#Pwdv=1.4 command[1]
#Pwd=Pwdf+Pwdv
#Ppvf=0.6 command[2]
#Ppvv=1 command[3]
#Ppv=Ppvf+Ppvv
#Pwind=Pwd+Ppv
#Pldf=0.4 command[4]
#Pldv=0.6 command[5]
#Pload=Pldf+Pldv
#SoC=0.93 command[6]
#PES=-0.2 command[7]
#start_ds=1 command[8]
#Type=4
#Disp_mode=0
#SoC_ref=0.52

    Pwdf=command[0]
    Pwdv=command[1]
    Pwd=Pwdf+Pwdv
    Ppvf=command[2]
    Ppvv=command[3]
    Ppv=Ppvf+Ppvv
    Pwind=Pwd+Ppv
    Pldf=command[4]
    Pldv=command[5]
    Pload=Pldf+Pldv
    SoC=command[6]
    PES=0.5  #grid power
    if spent_time>=100:
        PES=0
    Ppoiref=PES
    start_ds=command[7]
    Type=3
    Disp_mode=0
    SoC_ref=0.51


### Call dispatch###

    if island==0 and emg==0:    # grid-connected dispatch
    #griddisp(Pwind,Pload,SoC,PES,start_ds,Type,Disp_mode,SoC_ref)
        Gdisp=Griddisp1.Griddisp1()
        Gdisp.griddisp1(Pwind,Pload,SoC,PES,start_ds,Type,Disp_mode,SoC_ref)
        Pcurt=Gdisp.Pwdref
        PSLd=Gdisp.Pldref
        Pessref=Gdisp.Pessref
        Pdsref=Gdisp.Pdsref
        start_ds=Gdisp.Start_ds
        Disp_mode=Gdisp.disp_mode
    elif island==1 and emg==0:    # islanded dispatch
    # islanded dispatch
        Idisp=Isldisp1.Isldisp1()
        Idisp.Isldispatch1(Pwind,Pload,SoC,start_ds,Type,Disp_mode,SoC_ref)
        Pcurt=Idisp.Pwdref
        PSLd=Idisp.Pldref
        Pessref=Idisp.Pessref
        Pdsref=Idisp.Pdsref
        start_ds=Idisp.Start_ds
        Disp_mode=Idisp.disp_mode
        
    elif emg==1:    # unplanded islanding
        # unplanned islanding
        #emgdisp(self,Pdiesel,P_ES,start_ds,Pess,Type)
        Pdiesel=0.5
        Pess=1
        start_ds=1
        Uplan=Unplan1.Unplan1()
        Uplan.emgdisp(Pdiesel,PES,start_ds,Pess,Type)
        Pcurt=Uplan.PCwd
        PSLd=Uplan.PSLd
        Pdsref=Uplan.dPdiesel
        Pessref=Uplan.Pessref
        start_ds=Uplan.Start_ds
    
# Call distribution of Ppv and Pwd
#Ppv=0.5
#Pwd=0.7
#Pcurt=0.4
    dist2=Distribution.distribution()
    dist2.dist(Ppv,Pwd,Pcurt)
    Pwdreft=dist2.Pwdref    #
    Ppvreft=dist2.Ppvref
    
#    u=np.array(np.zeros(1))
#    v=np.array(np.zeros(1))
    
#    #Call WandQ of wind
#    WandQ2=WandQ1.WandQ1()
#    WandQ2.shed(u,v,np.array([Pwdf]),np.array([Pwdv]),Pwdreft)
#    Pwdfref=WandQ2.P11_new
#    Pwdvref=WandQ2.P21_new
#    
#    
#    # Call WandQ of PV
#    WandQ2=WandQ.WandQ()
#    WandQ2.shed(u,v,np.array([Ppvf]),np.array([Ppvv]),Ppv-Ppvreft)
#    Ppvfref=WandQ2.P11_new
#    Ppvvref=WandQ2.P21_new
#    
#    
#    # Call WandQ of Load
#    WandQ3=WandQ.WandQ()
#    WandQ3.shed(u,v,np.array([Pldf]),np.array([Pldv]),Pload-PSLd)
#    Pldfref=WandQ3.P11_new
#    Pldvref=WandQ3.P21_new
##############send  to output###################
    command[0]=Pdsref
    command[1]=PSLd
    command[2]=Pwdreft
    command[3]=Ppvreft
    command[4]=start_ds
    command[5]=Pessref
    command[6]=Ppoiref
    command[7]=0

#############################################################################         
        
        # send back
    command1=tuple(command)
    m.e.send(command1)
#     print (command1[0])
     
    elapsed_time = time.time() - start_time
#     print(elapsed_time)
