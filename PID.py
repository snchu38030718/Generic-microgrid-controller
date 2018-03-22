# -*- coding: utf-8 -*-
# https://github.com/ivmech/ivPID/blob/master/README.md

import time

class PID:
    """PID Controller
    """

    def __init__(self, P=0.3, I=0.0, D=0.0):

        self.Kp = P
        self.Ki = I
        self.Kd = D

        self.sample_time = 0.00
        self.current_time = time.time()
        self.last_time = self.current_time

        self.clear()

    def clear(self):
        """Clears PID computations and coefficients"""
        self.SetPoint = 0.0

        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0

        # Windup Guard
        self.int_error = 0.0
        self.windup_guard = 2000.0

        self.output = 0.0

    def update(self, feedback_value):  # key script
        """Calculates PID value for given reference feedback
        .. math::
            u(t) = K_p e(t) + K_i \int_{0}^{t} e(t)dt + K_d {de}/{dt}
        .. figure:: images/pid_1.png
           :align:   center
           Test PID with Kp=1.2, Ki=1, Kd=0.001 (test_pid.py)
        """
        error = self.SetPoint - feedback_value # new error

        self.current_time = time.time()
        delta_time = self.current_time - self.last_time
        delta_error = error - self.last_error
#        print(delta_time)

        #if (delta_time >= self.sample_time):  
#            print(delta_time)
        self.PTerm = self.Kp * error      # proportional term
        self.ITerm += error * delta_time  # integral term
#        print(self.ITerm)

        if (self.ITerm < -self.windup_guard): # wind_up
            self.ITerm = -self.windup_guard
        elif (self.ITerm > self.windup_guard):
            self.ITerm = self.windup_guard

        self.DTerm = 0.0
        if delta_time > 0:
            self.DTerm = delta_error / delta_time   # derivative term

            # Remember last time and last error for next calculation
        self.last_time = self.current_time
        self.last_error = error

#        self.output = self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm) # PID combination
        self.output = self.PTerm + (self.Ki * self.ITerm)  # PID combination

    def setKp(self, proportional_gain):
        """Determines how aggressively the PID reacts to the current error with setting Proportional Gain"""
        self.Kp = proportional_gain

    def setKi(self, integral_gain):
        """Determines how aggressively the PID reacts to the current error with setting Integral Gain"""
        self.Ki = integral_gain

    def setKd(self, derivative_gain):
        """Determines how aggressively the PID reacts to the current error with setting Derivative Gain"""
        self.Kd = derivative_gain

    def setWindup(self, windup):
        """Integral windup, also known as integrator windup or reset windup,
        refers to the situation in a PID feedback controller where
        a large change in setpoint occurs (say a positive change)
        and the integral terms accumulates a significant error
        during the rise (windup), thus overshooting and continuing
        to increase as this accumulated error is unwound
        (offset by errors in the other direction).
        The specific problem is the excess overshooting.
        """
        self.windup_guard = windup

    def setSampleTime(self, sample_time):
        """PID that should be updated at a regular interval.
        Based on a pre-determined sampe time, the PID decides if it should compute or return immediately.
        """
        self.sample_time = sample_time
