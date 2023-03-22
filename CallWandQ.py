# -*- coding: utf-8 -*-
"""
## Weighted and queuing algorithm for DER management
Created on Wed Jan  9 10:46:47 2019

@author: buaa_
"""
import numpy as np
import WandQ
import Distribution
import Griddisp1
import Isldisp1
import Unplan1

#u=np.array(np.zeros(4))
#v=np.array(np.zeros(3))
##w=np.array(np.zeros(4))
##x=np.array(np.zeros(3))
##u=[0,0]
##v=[0]
#w=[0,0.3,0.4,0.5]
#x=[0,0.6,0.7]
#P=1.9
#


# measured signal
Pwdf=1
Pwdv=1.4
Pwd=Pwdf+Pwdv
Ppvf=0.6
Ppvv=1
Ppv=Ppvf+Ppvv
Pwind=Pwd+Ppv
Pldf=0.4
Pldv=0.6
Pload=Pldf+Pldv
SoC=0.93
PES=-0.2
start_ds=1
Type=4
Disp_mode=0
SoC_ref=0.52

###### Islanded or grid-connected or unplan####
island=0
emg=0


### Call dispatch###


if island==0 and emg==0:
#griddisp(Pwind,Pload,SoC,PES,start_ds,Type,Disp_mode,SoC_ref)
    Gdisp=Griddisp1.Griddisp()
    Gdisp.griddisp(Pwind,Pload,SoC,PES,start_ds,Type,Disp_mode,SoC_ref)
    start_dsnew=Gdisp.Start_ds
    disp_modenew=Gdisp.disp_mode
    Pcurt=Gdisp.Pwdref
    PSLd=Gdisp.Pldref
elif island==1 and emg==0:  
# islanded dispatch
    Idisp=Isldisp1.Isldisp1()
    Idisp.Isldispatch1(Pwind,Pload,SoC,start_ds,Type,Disp_mode,SoC_ref)
    Pcurt=Idisp.Pwdref
    PSLd=Idisp.Pldref
elif emg==1: 
    # unplanned islanding
    #emgdisp(self,Pdiesel,P_ES,start_ds,Pess,Type)
    Pdiesel=0.5
    Pess=1
    start_ds=1
    Uplan=Unplan1.Unplan1()
    Uplan.emgdisp(Pdiesel,PES,start_ds,Pess,Type)
    Pcurt=Uplan.PCwd
    PSLd=Uplan.PSLd


# Call distribution of Ppv and Pwd
#Ppv=0.5
#Pwd=0.7
#Pcurt=0.4
dist2=Distribution.distribution()
dist2.dist(Ppv,Pwd,Pcurt)
Pwdreft=dist2.Pwdref    #
Ppvreft=dist2.Ppvref

u=np.array(np.zeros(1))
v=np.array(np.zeros(1))

#Call WandQ of wind
WandQ1=WandQ.WandQ()
WandQ1.shed(u,v,np.array([Pwdf]),np.array([Pwdv]),Pwd-Pwdreft)
Pwdfref=WandQ1.P11_new
Pwdvref=WandQ1.P21_new


# Call WandQ of PV
WandQ2=WandQ.WandQ()
WandQ2.shed(u,v,np.array([Ppvf]),np.array([Ppvv]),Ppv-Ppvreft)
Ppvfref=WandQ2.P11_new
Ppvvref=WandQ2.P21_new


# Call WandQ of Load
WandQ3=WandQ.WandQ()
WandQ3.shed(u,v,np.array([Pldf]),np.array([Pldv]),Pload-PSLd)
Pldfref=WandQ3.P11_new
Pldvref=WandQ3.P21_new



