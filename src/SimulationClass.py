# -*- coding: utf-8 -*
#    GCControl, a program to record and evaluate chromatograms
#              
#    Copyright (C) 2020 Johannes Stoeckelmaier <j.stoeckelmaier@gmx.at>
#
#    This file is part of GCControl.
#
#    GCControl is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    GCControl is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with GCControl.  If not, see <http://www.gnu.org/licenses/>.


import numpy as np
import src.function_CalcNumberOfPlates as calculatePlates

class SimulatedChromatogram():
       
    def __init__(self, peakTime, peakArea, N_calculated, parameters=None):
        
        if (parameters==None):
            time, signal = self.simulateIdealChromatogram(peakTime, peakArea, N_calculated, 0)  #skewFactor = 0 -->Symmetric peaks
            self.data = np.transpose(np.array([time,signal]))
        
        else:
            try:
                self.skewFactor = parameters[0]
                self.noiseLevel = parameters[1]
                self.driftFactor = parameters[2]
                self.speed = parameters[3]
            except:
                print("ERROR WHILE LOADING PARAMETERS OF SIMULATED CHROMATOGRAM")
            
            time, signal = self.simulateIdealChromatogram(peakTime, peakArea, N_calculated, self.skewFactor)
            
            time = time/self.speed
            time, signal = self.addNoise(time, signal, self.noiseLevel)
            time, signal = self.addDrift(time, signal, self.driftFactor)
            
            self.data = np.transpose(np.array([time,signal]))
            
            

    def simulateIdealChromatogram(self, peakTime, peakArea, N_calculated, skewFactor):
        #Transform skew-factor to lam
        enableSkew = True
        if (skewFactor < 0.01): 
            enableSkew = False
            skewFactor = 0.0
        
        tr = peakTime
        #ideal peaks are symetric, so we use N=5.545*((tr/w05)**2)
        w05 = tr*(1.0/np.sqrt(N_calculated/5.545))
    
        sigma = w05/2.3548  #Convert HalfWidth to sigma
        mean = peakTime
        
        t_End = peakTime[-1]*1.5
        x = np.linspace(0,t_End,int(t_End*4))
        signal = np.zeros(int(t_End*4))
    
        #Create Peaks in Chromatogram
        for i in range(peakTime.size):
            area = peakArea[i]
            
            if (enableSkew==True):
                lam = (1/skewFactor)
                signal = signal + self.exGauss(x, area, mean[i], sigma[i], lam)
            else:
                signal = signal + self.symGauss(x, area, mean[i], sigma[i])
            
        return x, signal



    def symGauss(self, x, area, mu, sigma):
        #Returns an Gauss-shaped Peak
        SQRT2 = 1.414213562
        return area * (1/(2*np.pi*sigma**2)**0.5) * np.exp(-((x-mu)/(SQRT2*sigma))**2.0)

    
    def exGauss(self, x, area, mu, sigma, lam):
            SQRT2 = 1.414213562
            
            K = 1.0/(sigma*lam)
            
            if (K<=0.05):
                print("ERROR! Peak skew is NOT possible with these settings. Fallback to symmetric peaks!")
                print("Symmetric Peak is a good approximation for this case")
                result = self.symGauss(x, area, mu, sigma)
            elif (K<100):
                from scipy.stats import exponnorm
                result = area * exponnorm.pdf(x, K, mu, sigma) 
            else:
                print("ERROR! Peak skew is NOT possible with these settings. Fallback to symmetric peaks!")
                print("Lambda too small / Skewfactor too big")
                result = self.symGauss(x, area, mu, sigma)

            return result
        
    
    def addNoise(self, time, signal, noiseFactor):
        noise = np.random.normal(0,noiseFactor,time.size)
        signal = signal + noise
        return time, signal
        
    def addDrift(self, time, signal, noiseDrift):
        return time, signal





class LoadSimParameters():
    def __init__(self, filePath):
        self.filePath = filePath
        self.deadTime = (120/60)
        self.tr_Methane = 0.3
        self.tr_Octane = 15.6
        
        self.qualityIndex = 0.6 #Value between 0 and 1
        self.noiseLevel = 1
        self.skewFactor = 0
        self.driftFactor = 0
        self.speed = 1
        self.totalInjVolume = 10
        self.sample = []
        self.sampleKovats = np.array([])
        self.sampleShare = np.array([])
        self.peakArea = np.array([])
        
        self.N_calculated = 1000
        
        self.loadSettings() #Do load the settings
        self.peakArea = self.calcPeakArea(self.totalInjVolume, self.sampleShare)
        self.peakTimes = self.calcRetentionTime(self.sampleKovats, self.deadTime, self.tr_Methane, self.tr_Octane)
        print("RETENTION TIME: ", self.peakTimes)
        print("PEAK AREA: ", self.peakArea)
        
        
        self.N_calculated = calculatePlates.calculatePlates(self.peakTimes, self.deadTime)
        self.N_calculated = self.N_calculated * self.qualityIndex
        
        print("CALCULATED PLATES: ", self.N_calculated)
        
    def loadSettings(self):
        #Read in Settings
        try:
         file1 = open(self.filePath, "r")
         settingsFile = file1.readlines() 
         file1.close()
         
         for x in settingsFile:
            ID = (x[0:x.find("=")]) 
            value = (x[x.find("=")+1 :]) 
       
            if (ID == "DEAD_TIME"): self.deadTime = float(value)
            if (ID == "TR_METHANE"): self.tr_Methane = float(value)
            if (ID == "TR_OCTANE"): self.tr_Octane = float(value)
            
            if (ID == "QUALITY"): self.qualityIndex = float(value)
            if (ID == "NOISE_LEVEL"): self.noiseLevel = float(value)
            if (ID == "SKEW_FACTOR"): self.skewFactor = float(value)
            #if (ID == "DRIFT"): self.driftFactor = float(value)
            if (ID == "SPEED"): self.speed = float(value)
            if (ID == "VOLUME"): self.totalInjVolume = float(value)
            if (ID == "SAMPLE"): self.sample.append(str(value[:-1]))
            
        except:
            print("ERROR while loading settings data")
            
        self.sampleKovats = np.zeros(len(self.sample))
        self.sampleShare =  np.zeros(len(self.sample))
        
        for index, data in enumerate(self.sample):
            sampleInfo = data.split(",")
            self.sampleKovats[index] = sampleInfo[0]
            self.sampleShare[index] = sampleInfo[1]
            
        print("RETENTION INDICES: ", self.sampleKovats)
        print("SAMPLE SHARE: ", self.sampleShare)
        print("SKEW FACTOR: ", self.skewFactor)
        
        
        
    def calcPeakArea(self, totalInjVolume, sampleShare):
        sampleArea = (sampleShare/100) * totalInjVolume
        sampleArea = sampleArea * 1000   #Defines SNR
        return sampleArea
    
    def calcRetentionTime(self, kovatsIndices, deadTime, tr_Methane, tr_Octane):
        
        tr_Methane = tr_Methane - deadTime
        tr_Octane = tr_Octane - deadTime
        
        deadtime = self.deadTime
        
        exponent = (kovatsIndices-100)/700 * (np.log(tr_Octane) - np.log(tr_Methane)) + np.log(tr_Methane)
        retentionTime = deadtime + np.exp(exponent)
        return retentionTime*60
    
