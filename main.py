# Author: Ilja Novickij

###############################################################################
# Imports
import os
#import array
import PID
import Unplan
#import Dispatch
import time
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
flag=1
ph_min=0.005
ph_max=0.01
ph_min1=6.1
ph_max1=6.3
ph_flag=1
time_close=100  # should be large
tie_flag=1
time_delay=0
while 1:
     start_time = time.time()
     command=list(m.e.status())
#     print(len(command))
#     print(m.e.message_header)
#     command1=array.array('d',command)
     
     # PID controller
     feedback1=0
     spent_time=time.time()-init_time
     if spent_time>10: 
         feedback1=command[3]
         #print (feedback1)
     ph_chck=abs(command[2])
     pid = PID.PID(P=0.01, I=1000000, D=0.000)  # give P,I,D, but not update now
     pid.SetPoint=0.0
     pid.setSampleTime(0.00)
     command[3]=0 # default, no PI control
     command[0]=0
     command[1]=0
     command[2]=0
     if spent_time>10 and spent_time<=22:  # setpoint change
         if flag==1:
                pid.SetPoint = -0.5 # Setpoint reference
                pid.update(feedback1) # update_feedback
                command[3] = pid.output  # output
                command[4]=0
                command[0]=0
                command[1]=0
                command[2]=0
#            #time.sleep(0.001)   # time_sleep

     if spent_time>22 and abs(feedback1)>=0.001 and ph_flag==1:  # setpoint change
         if flag==1:
                pid.SetPoint = 0 # Setpoint reference
                pid.update(feedback1) # update_feedback
                command[3] = pid.output  # output
                save_pess=command[3]
                command[4]=0
                command[0]=0
                command[1]=0
                command[2]=0
#               time.sleep(0.001)   # time_sleep
                #print(command[4])

     if (spent_time>=30 and abs(feedback1)<=0.01 and ph_flag==1) or flag==0: # open breaker
         flag=0      # flag is ued to lock the open state
         command[4]=1
         command[3]=0
         command[0]=0
         command[1]=0
         command[2]=0
#         pid.clear
         #print(command[4])
         
        
     if spent_time>45 and tie_flag==1:
         print (ph_chck)
         if command[2]>=0.5:
            if ph_chck>=ph_min1 and ph_chck<=ph_max1 and ph_flag==1: # close breaker
                 command[4]=0
                 command[3]=0
                 command[0]=0
                 command[1]=0
                 command[2]=0
                 pid.clear
#                 pid1=PID.PID(P=0.01, I=1000000, D=0.000)
                 ph_flag=0  # log close state
                 time_close=time.time()
            elif ph_flag==1:  # keep open
                 command[4]=1
                 command[3]=0
                 command[0]=0
                 command[1]=0
                 command[2]=0
                 pid.clear
            elif ph_flag==0:             # keep closed
                 command[4]=0
                 command[3]=0
                 command[0]=0
                 command[1]=0
                 command[2]=0
         else:
            if ph_chck>=ph_min and ph_chck<=ph_max and ph_flag==1: # close breaker
                 command[4]=0
                 command[3]=0
                 command[0]=0
                 command[1]=0
                 command[2]=0
                 ph_flag=0
                 pid.clear
#                 pid1=PID.PID(P=0.01, I=1000000, D=0.000)
#                 pid1.clear
                 time_close=time.time()
            elif ph_flag==1:  # keep open
                 command[4]=1
                 command[3]=0
                 command[0]=0
                 command[1]=0
                 command[2]=0
                 pid.clear
            elif ph_flag==0:             # keep closed
                 command[4]=0
                 command[3]=0
                 command[0]=0
                 command[1]=0
                 command[2]=0
                 
     tie_delay=time.time()-time_close
     if (tie_delay)>=8 and ph_flag==0 and spent_time<=80: # re-enable tie_line control 
         #print (tie_delay)
         command[4]=0             # keep closed
#         print(feedback1)
         pid.setSampleTime(0.00)
         pid.SetPoint = -0.5 # Setpoint reference
         pid.update(feedback1) # update_feedback
         command[3] = pid.output  # output
         command[0]=0
         command[1]=0
         command[2]=0
         save_pess=command[3]
#         command[3]=0
         tie_flag=0
     
     
###############################################################################       
 # Unplanned islanding       
     if spent_time>80 and spent_time<80.001 and tie_flag==0:  # change power reference
            unplan=Unplan.Unplan()
            unplan.edispatch(Pdiesel=command[1], P_ES=command[3])
            command[0]=unplan.dPdiesel
            command[1]=unplan.PCwd
            command[2]=unplan.PSLd
            command[4]=0            # ess stays at PQ control
            command[3]=save_pess    # ess is the power reference change of ess

     if spent_time>=80.001:                                # change ESS mode
            unplan=Unplan.Unplan()
            unplan.edispatch(Pdiesel=command[1], P_ES=command[3])
            command[0]=unplan.dPdiesel
            command[1]=unplan.PCwd
            command[2]=unplan.PSLd
            command[4]=1            # ess changes to Vf control
            command[3]=0
                    
###############################################################################       
        
        
  ###############################################################################       
 # Unplanned islanding       
#    dispatch=Dispatch.Dispatch()
#    dispatch.rdispatch()
                        
###############################################################################         
        
        
        
        
        
        
        # send back
     command1=tuple(command)
     m.e.send(command1)
#     print (command1[0])
     
     elapsed_time = time.time() - start_time;
     print(elapsed_time)
