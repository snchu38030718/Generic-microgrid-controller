# Author: Ilja Novickij

###############################################################################
# Imports
import os
#import array
import PID
import Unplan
#import Dispatch
import time
import Isldisp
import Gridisp
import Store
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
typecontrol=2
flag1=-5
flag=1
ph_min=0.005
ph_max=0.01
ph_min1=6.1
ph_max1=6.3
ph_flag=1
time_close=100  # should be large
tie_flag=1
time_delay=0
Pdiesel1=0
P_ES1=0
save0=0
save1=0
save2=0
save00=0
save11=0
save22=0
StartDs=1 #on; 0 off
savepess=0
windup_guard=2000
Kp=0.03
Ki=5
ITerm=0
PTerm=0
last_error=0
current_time=0
ITerm1=0
PTerm1=0
last_error1=0
SoC1=0.905   ###0.9
flag2=1
StDS=1
while 1:
     start_time = time.time()
     command=list(m.e.status())
     # PID controller
     feedback1=0
     spent_time=time.time()-init_time
     if spent_time>10: 
         feedback1=command[3]
         #print (feedback1)
     if spent_time>=129.8 and spent_time<129.9:
         Pdiesel1=command[1]
         P_ES1=-command[3]
         Pess=command[7]          #load following
     if spent_time>=70:
             SoC1=command[0]
     ph_chck=abs(command[2])
#     pid = PID.PID(P=0.01, I=1000000, D=0.000)  # give P,I,D, but not update now
     pid = PID.PID(P=0.01, I=5000, D=0.000)  # give P,I,D, but not update now
     pid.SetPoint=0.0
     pid.setSampleTime(0.000)
     unplan=Unplan.Unplan()
     Save=Store.Store()
     gdispatch=Gridisp.Gridisp()
     dispatch=Isldisp.Isldisp()
     if spent_time>0 and spent_time<=11:  # setpoint change
#         if flag==1:
                command[3]=0  # output
                command[4]=0
                command[0]=0
                command[1]=0
                command[2]=0
                StartDs=StDS
     
     if spent_time>11 and spent_time<=41:  # setpoint change
#        if flag==1:
#            gdispatch=Gridisp.Gridisp()
#            SoC=command[0]
#            Pwind=command[5]
#            Pload=command[6]
#            PES=0.5
#            gdispatch.gridispatch(Pwind,Pload,SoC,PES,StartDs)
#            command[0]=gdispatch.Pdsref
#            command[1]=gdispatch.Pwdref
#            command[2]=gdispatch.Pldref
#            pid = PID.PID(P=0.05, I=1000000, D=0.000)
#            pid.SetPoint = -0.5 # Setpoint reference
#            pid.update(feedback1) # update_feedback
#            command[3] = pid.output  # output
#            command[4]=0            
#            command[5]=0
#            command[6]=0
#            StartDs=gdispatch.Start_ds
##            global save_pess
#            save_pess=command[3] 
            command[3]=0  # output
            command[4]=0
            command[0]=0
            command[1]=0
            command[2]=0
            StartDs=StDS  # if soc<0.9,1 (SoC>0.9,0)
            last_time=time.time()
                
################################################################################
### grid-connected dispatch
     if spent_time>41 and spent_time<=60:
#        command=list(m.e.status())
        if flag1<1:
            gdispatch2=Gridisp.Gridisp()
            SoC=command[0]
#           print(SoC)
            Pwind=command[5]   # Load following
            Pload=command[6]
#            Pwind=command[6]   # cycle charging
#            Pload=command[7]
            PES=0.3            # Include the Power of ESS and POI.
            gdispatch2.gridispatch(Pwind,Pload,SoC,PES,StartDs,typecontrol)
            save0=gdispatch2.Pdsref
            save1=gdispatch2.Pwdref
            save2=gdispatch2.Pldref
            StartDs=gdispatch2.Start_ds
#            if SoC>0.2 and SoC<0.9:
#                flag1=flag1+1
#            flag1=1   ## Avoid conflict with ESS, necessary or not
            
 #################### PID start#####################################           
#            pid = PID.PID(P=0.01, I=100000, D=0.000)
#            pid.SetPoint = -0.2 # Setpoint reference
#            pid.update(feedback1) # update_feedback
#            command[3] = pid.output  # output
        SetPoint = -0.1 # Setpoint reference
        error = SetPoint - feedback1 # new error
        current_time = time.time()
        delta_time = current_time - last_time
        delta_error = error-last_error
#        print(delta_time)

#        if (delta_time >= self.sample_time):  
#            print(delta_time)
        PTerm = Kp * error      # proportional term
        ITerm += error * delta_time  # integral term
        print(ITerm)
        if (ITerm < -windup_guard): # wind_up
             ITerm = -windup_guard
        elif (ITerm > windup_guard):
             ITerm = windup_guard
        last_time = current_time
        last_error = error
#        self.output = self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm) # PID combination
        output = PTerm + (Ki * ITerm)  # PID combination
###################PID ene##################################
        command[3] = output
        if (SoC<0.2 and output>0) or (SoC>0.9 and output<0):
            command[3]=0
        command[0]=save0
        command[1]=save1
        command[2]=save2
        command[4]=0            
        command[5]=0
        command[6]=0
#            global save_pess
        save_pess=command[3]
#            time.sleep(0.005)   # time_sleep
#            command[3]=0# output
#            command[4]=0
#            command[0]=0.2
#            command[1]=0
#            command[2]=0
#            StartDs=0

##############################################################################
 ##### planned islanding               
     if spent_time>60 and ph_flag==1 and spent_time<70:  # setpoint change
         pid = PID.PID(P=0.01, I=5000, D=0.000)  # give P,I,D, but not update now
#         command=list(m.e.status())
         if flag==1:
                gdispatch=Gridisp.Gridisp()
                SoC=command[0]
#                print(SoC)
                Pwind=command[5]   # Load following
                Pload=command[6]
#                Pwind=command[6]   # cycle charging
#                Pload=command[7]
                PES=0.3
                gdispatch.gridispatch(Pwind,Pload,SoC,PES,StartDs,typecontrol)
#                command[0]=gdispatch.Pdsref
#                save0=command[0]
#                command[1]=gdispatch.Pwdref
#                save1=command[1]
#                command[2]=gdispatch.Pldref
#                save2=command[2]
                save0=gdispatch.Pdsref
                save1=gdispatch.Pwdref
                save2=gdispatch.Pldref
                StartDs=gdispatch.Start_ds
                flag=0    #only once, avoid conflict with ESS
# #################              PID
         SetPoint = -0 # Setpoint reference
         error = SetPoint - feedback1 # new error
         current_time = time.time()
         delta_time = current_time - last_time
         delta_error = error-last_error1
#        print(delta_time)

#        if (delta_time >= self.sample_time):  
#            print(delta_time)
         PTerm1 = Kp * error      # proportional term
         ITerm1 += error * delta_time  # integral term
         print(ITerm1)
         if (ITerm1 < -windup_guard): # wind_up
             ITerm1 = -windup_guard
         elif (ITerm1 > windup_guard):
             ITerm1 = windup_guard
         last_time = current_time
         last_error1 = error
#        self.output = self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm) # PID combination
         output1 = PTerm1 + (Ki * ITerm1)  # PID combination
 #######################################################               
#                pid.update(feedback1) # update_feedback
#                print(pid.ITerm)
         command[3] = output1 # output
#         command[3]=0
         save_pess=command[3]
         command[0]=save0   ### Pdsref
         command[1]=save1   ### Pwdref
         command[2]=save2   ### Pldref
         command[4]=0
         command[5]=0
         command[6]=0
#                time.sleep(0.005)   # time_sleep
                #print(command[4])

     if (spent_time>=70 and abs(feedback1)<=0.0005 and ph_flag==1) or flag==2: # open breaker
         flag=2      # flag is ued to lock the open state
         command[4]=1
         command[3]=0
         command[0]=save0
         command[1]=save1
         command[2]=save2
         command[5]=0
         command[6]=0
         Kp=0.01
         Ki=5
         ITerm=0
         PTerm=0
         last_error=0
         current_time=0
         StartDs=StDS
         Pwind=command[5]            ## For islanded operation btw 70 and 90
         Pload=command[6]+0.2        # 0.2 is the power from ESS
         StartDs1=StartDs
         dispatch.isldispatch(Pwind,Pload,SoC1,StartDs1,typecontrol)
         save0=dispatch.Pdsref
#        print(command[0])
         save1=dispatch.Pwdref
         save2=dispatch.Pldref
         
         
#         pid.clear
         #print(command[4])
         
###############################################################################
##### Reconnection
     if spent_time>90 and tie_flag==1:           # phase-check and synchronization
#         print (ph_chck)
         if command[2]>=0.5:               # phase_difference
            if ph_chck>=ph_min1 and ph_chck<=ph_max1 and ph_flag==1: # close breaker
                 command[4]=0
                 command[3]=0
                 command[0]=save0
                 command[1]=save1
                 command[2]=save2
                 pid.clear
#                 pid1=PID.PID(P=0.01, I=1000000, D=0.000)
                 ph_flag=0  # log close state
                 time_close=time.time()
            elif ph_flag==1:  # keep open
                 command[4]=1
                 command[3]=0
                 command[0]=save0
                 command[1]=save1
                 command[2]=save2
                 pid.clear
            elif ph_flag==0:             # keep closed
                 command[4]=0
                 command[3]=0
                 command[0]=save0
                 command[1]=save1
                 command[2]=save2
                 last_time=time.time()
                 StartDs=StDS
                 flag=3
         else:
            if ph_chck>=ph_min and ph_chck<=ph_max and ph_flag==1: # close breaker
                 command[4]=0
                 command[3]=0
                 command[0]=save0
                 command[1]=save1
                 command[2]=save2
                 ph_flag=0
                 pid.clear
#                 pid1=PID.PID(P=0.01, I=1000000, D=0.000)
#                 pid1.clear
                 time_close=time.time()
            elif ph_flag==1:  # keep open
                 command[4]=1
                 command[3]=0
                 command[0]=save0
                 command[1]=save1
                 command[2]=save2
                 pid.clear
            elif ph_flag==0:             # keep closed
                 command[4]=0
                 command[3]=0
                 command[0]=save0
                 command[1]=save1
                 command[2]=save2
                 last_time=time.time()
                 StartDs=StDS
                 flag=3

###############################################################################               
### reenable tie_line control  
     tie_delay=time.time()-time_close
     if (tie_delay)>=8 and ph_flag==0 and spent_time<=130.0: # re-enable tie_line control 
#     if (tie_delay)>=8 and ph_flag==0: # re-enable tie_line control 
         #print (tie_delay)
#         command=list(m.e.status())
         command[4]=0             # keep closed, PQ control
#         print(feedback1)
#         SoC1=command[0]
         if flag==3:
                gdispatch1=Gridisp.Gridisp()
                Pwind=command[5]
                Pload=command[6]
                PES=0.6
                gdispatch1.gridispatch(Pwind,Pload,SoC1,PES,StartDs,typecontrol)
        #                command[0]=gdispatch.Pdsref
        #                save0=command[0]
        #                command[1]=gdispatch.Pwdref
        #                save1=command[1]
        #                command[2]=gdispatch.Pldref
        #                save2=command[2]
                save00=gdispatch1.Pdsref
                save11=gdispatch1.Pwdref
                save22=gdispatch1.Pldref
                StartDs=gdispatch1.Start_ds
#                if SoC1>0.2 or SoC1>0.9:  # avoid conflict
                flag=4
# #################              PID
         SetPoint = -0.4 # Setpoint reference
         error = SetPoint - feedback1 # new error
         current_time = time.time()
         delta_time = current_time - last_time
         delta_error = error-last_error
         PTerm = Kp * error      # proportional term
         ITerm += error * delta_time  # integral term
         if (ITerm < -windup_guard): # wind_up
             ITerm = -windup_guard
         elif (ITerm > windup_guard):
             ITerm = windup_guard
         last_time = current_time
         last_error = error
#        self.output = self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm) # PID combination
         output = PTerm + (Ki * ITerm)  # PID combination
 #######################################################               
#                pid.update(feedback1) # update_feedback
#                print(pid.ITerm)
         command[3] = output # output
         if (SoC1<0.2 and output>0) or (SoC1>0.9 and output<0):
            command[3]=0
         command[0]=save00
         command[1]=save11
         command[2]=save22
         command[5]=0
         command[6]=0
#         command=list(m.e.status())
#         gdispatch=Gridisp.Gridisp()
#         SoC=command[0]
#         print(SoC)
#         Pwind=command[5]
#         Pload=command[6]
#         PES=0.5
#         gdispatch.gridispatch(Pwind,Pload,SoC,PES,StartDs)
#         command[0]=gdispatch.Pdsref
#         save0=command[0]
#         command[1]=gdispatch.Pwdref
#         save1=command[1]
#         command[2]=gdispatch.Pldref
#         save2=command[2]
#         StartDs=gdispatch.Start_ds
#         pid = PID.PID(P=0.01, I=200000, D=0.000)
#         pid.setSampleTime(0.0005)
#         pid.SetPoint = -0.5 # Setpoint reference
#         pid.update(feedback1) # update_feedback
#         command[3] = pid.output  # output
         save_pess=command[3]
#         command[3]=0
         tie_flag=0
#     
#     
################################################################################       
 # Unplanned islanding 
     if spent_time>130.0 and spent_time<130.02 and tie_flag==0:  # change power reference
         if flag2==1:
             unplan.edispatch(Pdiesel1, P_ES1, StartDs, Pess, typecontrol)
             save0=unplan.dPdiesel
             save1=unplan.PCwd
             save2=unplan.PSLd
             flag2=2
#         command[4]=0            # ess stays at PQ control,type I
         command[4]=1            # type II
         command[3]=save_pess    # ess is the power reference change of ess
#         Save.store(save0,save1,save2)#         
         command[0]=save0
         command[1]=save1
         command[2]=save2
     
     if spent_time>=130.02 and spent_time<=135:                                # change ESS mode
#     if spent_time>=130.02:                                # change ESS mode
            command[0]=save0
#            save1=Save.gety()
            command[1]=save1
#            save2=Save.getz()
            command[2]=save2
            command[4]=1            # ess changes to Vf control
            command[3]=save_pess
            StartDs=StDS
                    
##############################################################################       
        
        #Pwdref,Pdsref,Pldref,Start_ds
##############################################################################       
### Island dispatch
     if spent_time>135:
#        command=list(m.e.status())
        print(SoC1)
#        print(dispatch)
        Pwind=command[5]
        Pload=command[6]
        StartDs1=StartDs
        dispatch.isldispatch(Pwind,Pload,SoC1,StartDs1,typecontrol)
        command[0]=dispatch.Pdsref
#        print(command[0])
        command[1]=dispatch.Pwdref
        command[2]=dispatch.Pldref
        command[4]=1            # ess changes to Vf control
        command[3]=0
        command[5]=0
        command[6]=0
        StartDs=dispatch.Start_ds
#        print(StartDs)
 
#############################################################################         
        
        # send back
     command1=tuple(command)
     m.e.send(command1)
#     print (command1[0])
     
     elapsed_time = time.time() - start_time
#     print(elapsed_time)
