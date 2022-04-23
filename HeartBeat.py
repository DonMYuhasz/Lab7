# -*- coding: utf-8 -*-
"""
noise curve v2

modified from noise curve
modified from damped sin wave
code pulled from
https://stackoverflow.com/questions/33213408/python-convert-an-array-to-wav

for reasons beyond my comprehension these wav files are considered encoded improperly by windows media player
but putting them through wav to wav conversion online fixes that issue. or using a different media player
"""

import numpy as np
import scipy.optimize as opt
import scipy.stats as st
import scipy.io.wavfile as wavf
import math
import matplotlib.pyplot as plt
import random as rd

pulse = 500
beats = 0         
minperiod = 4000   
name = "normal1.wav"
    
def sin(xin,amp,period):
    return[amp*math.sin(((2*np.pi)/period)*x) for x in xin]

def beatNo(xin):
    global pulse, beats,minperiod

    #A hysterysis inspired aproach to filtering
    xout2 = [0]
    beats = 0
    timelast = -minperiod
    for x in range(1,len(xin)):
        if (np.absolute(xin[x]) - 4500 > np.absolute(xin[x-pulse]) and x >(timelast + minperiod) ):
            xout2.append(4000)    
            timelast = x
        else:
            xout2.append(0)
            
    for x in range(1,len(xout2)):
        if xout2[x] == 4000 and xout2[x-1] == 0 :
            beats = beats + 1 
    
    
    xout1 = [xout2[x]/5000 for x in range (len(xin))]

    return xout1
    


rate = wavf.read(name)[0]
data = wavf.read(name)[1]


time = len(data)/rate

#creates full sine wave
xr = [ v for v in range(len(data))]
"""
#y = sin(xr,2,.3,2,.1)
a1 = sin(xr,2,2)
a2 = sin(xr,.3,.1)
a3 = sin(xr,.2,20)
a4 = randnoise(xr,.4)
#y = [a1[x]+a2[x]+a3[x]+a4[x] for x in range(len(xr))]

opt,cov = opt.curve_fit(sin,xr,y,(2,2))


ypred = sin(xr,*opt)

data = np.array(ypred)
"""


data2 = beatNo(data)
data2 = np.array(data2)

data = [data[x]/15000 for x in range (len(data))]
data = np.array(data)

BPM = 60/time * beats
print("BPM is",BPM)
print("time between beats is ",60/BPM, "s")
print("Breathing rate: yes")
plt.plot(xr,data,'b-',label = "original")
plt.plot(xr,data2,'g-',label = "filtered")
#plt.title("plot in python")
plt.title("Sound Graph")
plt.legend()
plt.show()