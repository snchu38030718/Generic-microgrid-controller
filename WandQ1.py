# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 16:42:13 2019

@author: csun26
"""
import numpy as np
import copy
class WandQ1:
    def _init_(self):
        self.Curtratio=0.1
        self.Pwdref=0
        self.Ppvref=0

    def shed(self,Ppv,Pwind,Pcurt):  ## u(1:ON/OFF),v(2,variable) is present, w(1), x(2) is the come, all are vectors
#        function [P11_new,P21_new] = fcn(u,v,w,x,Pplan)
        self.Curtratio=np.min([Ppv/(Ppv+Pwind),1]) # Curtratio calculation
        if self.Curtratio<=0.1:                   # Curtratio lower limit
            self.Curtratio=0
        elif self.Curtratio>=100:               # Curtratio upper limit
            self.Curtratio=1
#        end
        self.Ppvref=Pcurt*self.Curtratio             # PV power reference calculation
        if self.Ppvref>=Ppv:                      # PV power limt
            self.Ppvref=Ppv
#        end
        self.Pwdref=Pcurt*(1-self.Curtratio)         # Wind power limt
        if self.Pwdref>=Pwind:
            self.Pwdref=Pwind
#        end