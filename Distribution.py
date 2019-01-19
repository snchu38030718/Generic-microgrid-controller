# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 22:07:53 2019

@author: buaa_
"""
import numpy as np
class distribution:
    def _init_(self):
        self.Curtratio=1
        self.Pwdref=0
        self.Ppvref=0
        
    def dist(self,Ppv,Pwind,Pcurt):
        self.Curtratio=np.min([Ppv/(Ppv+Pwind),1])
        if self.Curtratio<=0.1:
            self.Curtratio=0
        elif self.Curtratio>=100:
            self.Curtratio=1
#        end
        self.Ppvref=Pcurt*self.Curtratio
        if self.Ppvref>=Ppv:
            self.Ppvref=Ppv
#        end
        self.Pwdref=Pcurt*(1-self.Curtratio)
        if self.Pwdref>=Pwind:
            self.Pwdref=Pwind
#        end
#end