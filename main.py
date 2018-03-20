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
while 1:
     start_time = time.time()
     command=list(m.e.status())
#     print(len(command))
#     print(m.e.message_header)
     #command1=array.array('d',command)
     command[0]=command[0]
     command[1]=command[1]*2
     command[2]=command[2]*2
     
     # PID controller
     feedback1=0
     spent_time=time.time()-init_time
     if spent_time>10: 
         feedback1=command[3]
     pid = PID.PID(1, 20, 0.000)  # give P,I,D, but not update now
     pid.SetPoint=0.0
     pid.setSampleTime(0.0000)
     command[3]=0 # default, no PI control
     if spent_time>10:  # setpoint change
            pid.SetPoint = -0.2 # Setpoint reference
            pid.update(feedback1) # update_feedback
            command[3] = pid.output  # output
     if spent_time>10:  # setpoint change
            pid.SetPoint = -0.2 # Setpoint reference  
            pid.update(feedback1) # update_feedback
            command[3] = pid.output  # output
    
     # send back
     command1=tuple(command)
     m.e.send(command1)
#     print (command1[0])
     
     elapsed_time = time.time() - start_time;
     print(elapsed_time)
