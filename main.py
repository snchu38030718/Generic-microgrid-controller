# Author: Ilja Novickij

###############################################################################
# Imports
import os
#import array
#import time
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
while 1:
     #start_time = time.time()
     command=list(m.e.status())
     print(len(command))
     print(m.e.message_header)
     #command1=array.array('d',command)
     command[0]=command[0]*2
     command[1]=command[1]*2
#     command[2]=command[2]*2
     command1=tuple(command)
     m.e.send(command1)
#     print (command1[0])
     
     #elapsed_time = time.time() - start_time;
     #print(elapsed_time)
