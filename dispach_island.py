# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 02:19:05 2018

@author: csun26
"""
## A more complicated rule based dispatch

function [Pwdref,Pdsref,Pldref,Start_ds] = Ruledispatch(Pwind,Pload,SoC,start_ds)
SoC_max = 0.9;   %%95
SoC_min = 0.2;
Pch_max = 1;
Pdis_max = -1;  %%-1.5
Pds_min=0.2;
Pds_max=1;
Pnet=Pwind-Pload;
Pessref=0;
Pwdref=0;
Pdsref=0;
Pldref=0;
if Pnet>=0     %% More, wind is controllable, diesel is off, ESS depends
        if SoC>=SoC_max     %% Charge is
            Pwdref=Pnet;        %% pwdref is positive
            Pessref=0;
            Pdsref=0;
            Pldref=0;
            Start_ds=0;
        else     % SoC<SoC_max
            if start_ds>=1 && start_ds<=3
                Pdsref=Pds_min;
                if Pnet+Pdsref<Pch_max
                    Pessref=Pnet+Pds_min;
                    Pwdref=0;
                    Pdsref=Pds_min;
                    Start_ds=start_ds+1;
                    if Start_ds>=4;
                        Start_ds=0;
                    end
                    Pldref=0;
                else
                    Pessref=Pch_max;
                    Pwdref=Pnet+Pdsref-Pch_max;
                    Pldref=0;
                    Pdsref=Pds_min;
                    Start_ds=start_ds+1;
                    if Start_ds>=4;
                        Start_ds=0;
                    end
                end
            else
                Start_ds=0;
                if Pnet<Pch_max  %% ds is off or Ton>=3
                    Pessref=Pnet;
                    Pwdref=0;
                    Pdsref=0;
                    Pldref=0;
                else
                    Pessref=Pch_max;
                    Pwdref=Pnet-Pch_max;
                    Pdsref=0;
                    Pldref=0;
                end
            end  
        
        end
%     end
elseif SoC>=SoC_min    ## Less, load is controllable, diesel on/off, SoC_min<SoC<SoC_max
       if  start_ds>=1 && start_ds<=3
           Pdsref=Pds_min;
           Pnet=Pwind+Pds_min-Pload;
           if -Pnet<-Pdis_max   %% Pnet is smaller than largest discharge power
            Pessref=Pnet;   %% Pessref is negative
            Pldref=0;
            Pdsref=Pds_min;
            Start_ds=start_ds+1;
            if Start_ds>=4;
                Start_ds=0;
            end
            Pwdref=0;
           else
            Pldref=-Pnet+Pdis_max;  %%Pldref is positive
            Pessref=Pdis_max;
            Pdsref=Pds_min;
            Start_ds=start_ds+1;
            if Start_ds>=4;
                Start_ds=0;
            end
            Pwdref=0;
           end
       else
           Start_ds=0;
           if -Pnet<-Pdis_max   %% Pnet is smaller than largest discharge power
            Pessref=Pnet;   %% Pessref is negative
            Pldref=0;
            Pdsref=0;
            Pwdref=0;
           else                 ## Pnet is larger than the largest discharge power
            Pldref=-Pnet+Pdis_max;  %%Pldref is positive
            Pessref=Pdis_max;
            Pdsref=0;
            Pwdref=0;
           end
       end
else            ## SoC<SoC_min, diesel should be on

     if -Pnet<Pds_min  %% Pnet is smaller than the smallest diesel power
            if  start_ds>=1 && start_ds<=3
                Pdsref=Pds_min;
                Start_ds=start_ds+1;
                if Start_ds>=4;
                    Start_ds=0;
                end
                Pldref=0;
                Pessref=Pds_min-Pnet;
                Pwdref=0;
            else
                Start_ds=0;
                Pldref=-Pnet;   %%Pldref is positive, shedding
                Pessref=0; %% ESS is still master
                Pdsref=0;
                Pwdref=0;
            end
     else                   
            if -Pnet<=Pds_max  %% Pds_min<-Pnet<Pds_max
                Pessref=0;
                Pdsref=-Pnet;
                Start_ds=start_ds+1;
                if Start_ds>=4;
                    Start_ds=0;
                end
                Pwdref=0;
                Pldref=0;
            else              %% -Pnet>Pds_max
                Pessref=0;
                Pwdref=0;
                Pdsref=Pds_max;
                Start_ds=start_ds+1;
                if Start_ds>=4;
                    Start_ds=0;
                end
                Pldref=-Pnet+Pds_max;
             end
    end
end
end