import numpy as np
import math 
import matplotlib.pyplot as plt

def findRMS (x):
    rows,cols = x.shape
    
    rms = np.zeros((1,rows))
    
    for i in range(0,rows):
        sum = 0
        
        for j in range(0,cols):
            sum = sum + (x[i,j]**2)
            
        div = sum/cols
        rms[0,i] = math.sqrt(div)
    
    return rms 

def plotsubplot(x,y,rows,cols,xAxisData,theData,theXlabel,theYlabel):
    
    for i in range(x,y):
        plt.subplot(rows,cols,i)
        plt.plot(xAxisData[i-1],theData[i-1,:])
        plt.ylabel(theXlabel)
        plt.xlabel(theYlabel)
    
    return 0 
