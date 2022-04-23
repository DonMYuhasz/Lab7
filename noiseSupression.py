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
#sums 2 sine waves in this case one being noise(in hindsight i can just sum up multiple sin calls)
# def sin2(xin,amp,amp2,period,period2):
#     return[amp*math.sin(((2*np.pi)/period)*x)+amp2*math.sin(((2*np.pi)/period2)*x)+(amp2/2)*math.sin(((2*np.pi)/(period2**1.5))*x) for x in xin]

def randnoise(xin,amp):
    return[rd.uniform(0,amp*10)/10 for x in xin]
           
           
def sin(xin,amp,period):
    return[amp*math.sin(((2*np.pi)/period)*x) for x in xin]

#creates full sine wave
xr = [ v/50 for v in range(100000)]
#y = sin(xr,2,.3,2,.1)
a1 = sin(xr,2,2)
a2 = sin(xr,.3,.1)
a3 = sin(xr,.2,20)
a4 = randnoise(xr,.4)
y = [a1[x]+a2[x]+a3[x]+a4[x] for x in range(len(xr))]

opt,cov = opt.curve_fit(sin,xr,y,(2,2))


ypred = sin(xr,*opt)

data = np.array(ypred)
data2 = np.array(y)

wavf.write('toneUn.wav', 10000, data2)
wavf.write('tone.wav', 10000, data)


plt.plot(xr,y,'b-',label = "original")
plt.plot(xr,ypred,'g-',label = "prediction")
#plt.title("plot in python")
plt.title("noise fit for order sin")
plt.legend()
plt.show()
