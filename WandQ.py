# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 16:42:13 2019

@author: csun26
"""
import numpy as np
import copy
class WandQ:
    def _init_(self):
        self.P11min=0.2
        self.P12min=0.1
        self.P13min=0.1
#        self.P11_new=np.zeros(2)
#        self.P21_new=np.zeros(1)
        self.N=1
        self.M=1

    def shed(self,u,v,w,x,Pplan):  ## u(1:ON/OFF),v(2,variable) is present, w(1), x(2) is the come, all are vectors
#        function [P11_new,P21_new] = fcn(u,v,w,x,Pplan)
        self.N=len(w)
        P1_array=np.zeros(self.N)  ## u,v are present variables
        P1f_array=np.zeros(self.N) ## w,x are coming variables
        P1_array=u
        P1f_array=w
        P1=0
        P1f=0
        for i in range(0,self.N):
            P1_array[i]=copy.deepcopy(u[i])
            P1f_array[i]=copy.deepcopy(w[i])
            P1f=P1f+w[i]
        
        self.M=len(x)
        P2_array=np.zeros(self.M)
        P2f_array=np.zeros(self.M)
        P2min_arr=np.zeros(self.M)
        P2=0
        P2f=0
        Pmin=0
        for i in range(0,self.M):
            P2_array[i]=copy.deepcopy(v[i])
            P2f_array[i]=copy.deepcopy(x[i])
            P2min_arr[i]=np.max([x[i]*0.5,0])
            P2f=P2f+x[i]
            Pmin=Pmin+P2min_arr[i]
        #end
        # P2=P21+P22
        # P2f=P21f+P22f
        # Pmin=P21min+P22min 
        # Pout=P1+P2
        
        Poutf=P1f+P2f
        tr=1  # Flag indicating ends of trip
        PcutA=0
        PcutB=0
        Pcut=0
        Porig=Pplan
        
        P1_Arr=np.zeros(self.N)
        P1_Brr=np.zeros(self.M)
        
        if Pplan>=P1f+Pmin and Pplan<=Poutf+0.01:               ## Case 1
            for i in range(0,self.N):
                P1f_array[i]=P1f_array[i]
            #end
            for j in range(0,self.M):
                P2_array[j]=np.max([P2min_arr[j],P2f_array[j]/P2f*(Pplan-P1f)])
            #end
            self.P11_new=P1f_array
            self.P21_new=P2_array
        else: #P1f>Pplan:                          ## Case 2
            while tr!=0:
        #     for m=1:N
        #         num(m)=nnz(P1>(Pplan-Pmin))
        #     #end
                Aflag_P1=P1f_array>(P1f-Pplan+Pmin)
                Aflag_P1=np.argwhere(Aflag_P1 != 0)## Aflag_P1 is an array
                if np.count_nonzero(Aflag_P1)!=0:                       ## Subcase a
                    PcutA=np.min(np.extract(P1f_array>(P1f-Pplan+Pmin),P1f_array))
    #                if length(find((P1f_array-PcutA)==0))>=1:
                    if np.count_nonzero((P1f_array-PcutA)==0)>=1:
                        i=0
                        while i<=self.N-2:
                            P1_Arr[i+1]= PcutA*(P1f_array[i+1]==PcutA)
                            if P1_Arr[i+1]!=0:
                                i=self.N+1
                            else:
                                i=i+1
                            #end
                        #end
                    #end          
            #         P1_Arr(P1f_array==PcutA)=PcutA
                    for i in range(0,self.N):
                        P1f_array[i]=P1f_array[i]-P1_Arr[i] ## remove P1_Arr
                    #end
                    PcutB=0
                    tr=0
                    P1_Arr=np.zeros(self.N)
                    P1f=P1f-PcutA-PcutB
                else:
            #         Bflag_P1=P1f_array<=(Pplan-Pmin)
                    Bflag_P1=P1f_array<=(P1f-Pplan+Pmin)
                    Bflag_P1=np.argwhere(Bflag_P1 != 0)
                    if np.count_nonzero(Bflag_P1)!=0:                   ## Subcase b
                        PcutB=np.max(np.extract(P1f_array<=(P1f-Pplan+Pmin),P1f_array))
            #             P1_Brr(P1f_array==PcutB)=PcutB
    #                    if length(find((P1f_array-PcutB)==0))>=1:
                        if np.count_nonzero((P1f_array-PcutB)==0)>1:
                            i=0
                            while i<=self.N-2:
                                P1_Brr[i+1]=PcutB*(P1f_array[i+1]==PcutB)
                                if P1_Brr[i+1]!=0:
                                    i=self.N+1
                                else:
                                    i=i+1
                                #end
                            #end
                        #end 
            #             P1f_array=P1f_array-P1_Brr
                        for i in range(0,self.N):
                            P1f_array[i]=P1f_array[i]-P1_Brr[i] ## remove P1_Arr
                        #end
                        P1f=P1f-PcutB
                        if (Pplan-P1f-Pmin)<0:   ## Subcase c
            #                 Pplan=Pplan-PcutB
                            tr=tr+1
                        else:
                            tr=0
                        #end
                        PcutA=0
                        P1_Brr=np.zeros(self.M)
                    else:
                        PcutA=0
                        PcutB=0
                    #end
                    P1f=P1f-PcutA
                #end
            #     Pcut=Pcut+PcutA+PcutB
                #end
                temp=0
                for m in range(0,self.M):
                    temp=np.max([P2min_arr[m],P2f_array[m]/P2f*(Pplan-P1f)])
                    P2_array[m]=np.min([temp,P2f_array[m]])
                self.P11_new=P1f_array
                self.P21_new=P2_array
    #            return self.P11_new,self.P21_new