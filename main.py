# Author: Ilja Novickij

###############################################################################
# Imports
import os
#import array
import PID
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
ph_min=0.01
ph_max=0.04
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
     #command1=array.array('d',command)
     command[0]=command[0]
     command[1]=command[1]*2
     
     # PID controller
     feedback1=0
     spent_time=time.time()-init_time
     if spent_time>10: 
         feedback1=command[3]
         #print (feedback1)
     pid = PID.PID(P=0.01, I=1000000, D=0.000)  # give P,I,D, but not update now
     pid.SetPoint=0.0
     pid.setSampleTime(0.00)
     command[3]=0 # default, no PI control
     if spent_time>10 and spent_time<=22:  # setpoint change
         if flag==1:
                pid.SetPoint = -0.5 # Setpoint reference
                pid.update(feedback1) # update_feedback
                command[3] = pid.output  # output
#            #time.sleep(0.001)   # time_sleep

     if spent_time>22 and abs(feedback1)>=0.001 and ph_flag==1:  # setpoint change
         if flag==1:
                pid.SetPoint = 0 # Setpoint reference
                pid.update(feedback1) # update_feedback
                command[3] = pid.output  # output
#               time.sleep(0.001)   # time_sleep
                #print(command[4])

     if spent_time>23 and abs(feedback1)<=0.05 and ph_flag==1: # open breaker
         command[4]=1
         command[3]=0
#         pid.clear
         #print(command[4])
         flag=0      # flage is ued to lock the open state
        
     ph_chck=abs(command[2])
     if spent_time>35 and tie_flag==1:
         print (ph_chck)
         if command[2]>=0.2:
            if ph_chck>=ph_min1 and ph_chck<=ph_max1: # close breaker
                 command[4]=0
                 command[3]=0
#                 pid.clear
#                 pid1=PID.PID(P=0.01, I=1000000, D=0.000)
                 pid.clear
                 ph_flag=0  # log close state
                 time_close=time.time()
            elif ph_flag==1:  # keep open
                 command[4]=1
                 command[3]=0
                 pid.clear
            elif ph_flag==0:             # keep closed
                 command[4]=0
                 command[3]=0
         else:
            if ph_chck>=ph_min and ph_chck<=ph_max: # close breaker
                 command[4]=0
                 command[3]=0
                 ph_flag=0
                 pid.clear
#                 pid1=PID.PID(P=0.01, I=1000000, D=0.000)
#                 pid1.clear
                 time_close=time.time()
            elif ph_flag==1:  # keep open
                 command[4]=1
                 command[3]=0
                 pid.clear
            elif ph_flag==0:             # keep closed
                 command[4]=0
                 command[3]=0
#                 
#     tie_delay=time.time()-time_close
#     if (tie_delay)>=8 and ph_flag==0: # re-enable tie_line control 
#         #print (tie_delay)
#         command[4]=0             # keep closed
##         print(feedback1)
#         pid.setSampleTime(0.00)
#         pid.SetPoint = -0.1 # Setpoint reference
#         pid.update(feedback1) # update_feedback
#         command[3] = pid.output  # output
##         command[3]=0
#         tie_flag=0
     # send back
     command1=tuple(command)
     m.e.send(command1)
#     print (command1[0])
     
     elapsed_time = time.time() - start_time;
     print(elapsed_time)
