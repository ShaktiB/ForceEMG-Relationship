import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
from scipy import signal 
from scipy import integrate
from rehabLab1functions import findRMS
from rehabLab1functions import plotsubplot

# Loading data 
x = sio.whosmat('TA_data1.mat')
#print(x)
theData = sio.loadmat('TA_data1.mat')

rawEmg = theData['increase_ta_emg']
rawForce = theData['increase_ta_force']
mvcEmg = theData['mvc_ta_emg']
mvcForce = theData['mvc_ta_force']

############### Converting the data from Volts to mV; taking the 500 amplifier gain into account ###########################

fs = 2000; # sampling frequency
gain = 500; # amplifier gain

convertedEmg = (rawEmg*1000)/gain # converting EMG from V to mV
dlen = len(convertedEmg)
t = (np.arange(dlen))/fs # time in seconds 

################ Normalization of the force and EMG using the MVC data ##############################

""" It is common practice to normalize the signals by maximal voluntary contraction (MVC) 
This is done by expressing the values as percentage of MVC 
MVC signal is obtained by recording the maximal voluntary contraction """

maxMvcEmg = max(mvcEmg)
maxMvcForce = max(mvcForce)

normEmg = convertedEmg/maxMvcEmg # Normalized EMG 
normForce = (rawForce/maxMvcForce) # Normalized Force 

################## Segmentation of the EMG and Force signals  ###############################

numSegments = 10; # Number of rows 
segLength = int(dlen/numSegments) # Number of columns

segEMG = np.reshape(normEmg,(numSegments,segLength))
segForce = np.reshape(normForce,(numSegments,segLength))
segt = np.reshape(t,(numSegments,segLength))

################ Rectification of the EMG signal  ###################################

rectEMG = abs(segEMG)

######### Envelopping the EMG (applying a low-pass 4th order butterworth filter) ###########################

fc = 2.5 # cut-off frequency 
Wn = fc/(fs/2) 
N = 4 # order of the filter 

b, a = signal.butter(N, Wn, 'low')
envlpEMG = np.zeros((numSegments,segLength))

for i in range(0,10):
    envlpEMG[i,:] = signal.filtfilt(b,a,rectEMG[i,:])

######### RMS of the EMG and Force ######################
    
rmsEMG = np.transpose(findRMS(envlpEMG)) # Pyplot will not plot it if it is not transposed this way 
rmsForce = np.transpose(findRMS(segForce))

########## iEMG #############################
# The cumulative trapezoidal numerical integration of each segment
# 'iemg'

iemg = np.zeros((numSegments,segLength))

for i in range(0,10):
    iemg[i,:] = integrate.cumtrapz(envlpEMG[i,:],initial=0)/1000
    
######### Mean and Max Force Per Contraction AND EMG Median Frequency Per Contraction ####################

meanForce = np.zeros((1,numSegments))
maxForce = np.zeros((1,numSegments))

medFreq = np.zeros((1,numSegments))
maxAmplitude = np.zeros((1,numSegments))

for i in range (0,10):
    meanForce[0,i] = sum(segForce[i,:])/segLength # Mean force of the segment
    maxForce[0,i] = max(segForce[i,:]) #Max force of the segment 
    
    maxAmplitude[0,i] = max(envlpEMG[i,:])

################### Plotting Graphs  ###################################################

# Plotting Behaviour Trends 
    
fig1 = plt.figure()
plt.subplot(2,1,1)
plt.plot(np.transpose(maxAmplitude))
plt.ylabel('mV')
plt.title('Maximum EMG Amplitude Per Segment')
plt.show()

plt.subplot(2,1,2)
plt.plot(np.transpose(maxForce))
plt.ylabel('Newtons')
plt.xlabel('Segment #')
plt.title('Maximum Force Per Segment')

plt.show()

# Plotting the Rectified EMG segments 
fig2 = plt.figure()

for i in range(1,11):
    plt.subplot(5,2,i)
    plt.plot(segt[i-1],rectEMG[i-1,:])
    plt.ylabel('mV')
    plt.xlabel('time (s)')
    
fig2.suptitle('Rectified EMG')
plt.show()

#Plotting the envelopped EMG segments (low-pass filtered: 4th order butterworth)

fig3 = plt.figure()

for i in range(1,11):
    plt.subplot(5,2,i)
    plt.plot(segt[i-1],envlpEMG[i-1,:])
    plt.ylabel('mV')
    plt.xlabel('time (s)')
    
fig3.suptitle('Enveloped EMG')
plt.show()


# Plotting the segmented force 

fig4 = plt.figure()
    
xaxislabel = 'Newtons'
yaxislabel = 'time(s)'
plotsubplot(1,11,5,2,segt,segForce,xaxislabel,yaxislabel)
    
fig4.suptitle('Segmented Forces')
plt.show()

# Plotting segmented IEMG 

fig5 = plt.figure()

xaxislabel = 'mV-sec'
yaxislabel = 'time(s)'
plotsubplot(1,11,5,2,segt,iemg,xaxislabel,yaxislabel)
    
fig5.suptitle('IEMG')
plt.show()

# Plotting the entire signals 

finalForce  = segForce.flatten()
finalEMG = envlpEMG.flatten()
finalIEMG = integrate.cumtrapz(finalEMG,initial=0)/1000

fig6 = plt.figure()
    
plt.subplot(3,1,1)
plt.plot(t,finalEMG)
plt.ylabel('mV')
plt.title('EMG')


plt.subplot(3,1,2)
plt.plot(t,finalForce)
plt.ylabel('N')
plt.title('Force')


plt.subplot(3,1,3)
plt.plot(t,finalIEMG)
plt.ylabel('mV-sec')
plt.xlabel('time(s)')
plt.title('IEMG')

        




