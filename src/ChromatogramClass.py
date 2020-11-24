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


###################################
###################################
#
# Class that contains the data of the used chromatogram
#
###################################
###################################
import numpy as np
import src.function_CalcNumberOfPlates as calculatePlates


class Chromatogram():
    
    #######################################
    #
    # Init Dataset
    #
    #######################################
    def __init__(self):
        ############################
        # Declare all variables of the dataset
        #
        self.startNewChromatogram(startTime = 0.0)
        
    def startNewChromatogram(self, startTime):
        self.resetCalculatedData()
        self.original = np.zeros([0,2]) 
        self.startTime = startTime
        
    def resetCalculatedData(self):
        #Data of full dataset
        self.denoised = np.zeros([0,2])  #denoised chromatographic data
        self.peakCount = 0
        
        #Data of single peaks
        self.peakPos = np.array([])
        self.peakArea = np.array([])
        self.peakWidthLeft = np.array([])
        self.peakWidthRight = np.array([])
        
        #Performance Data of Dataset
        self.N_measured_global = np.array([])
        self.N_calculated_global = np.array([])
        self.N_measured_avg = 0.0
        self.N_calculated_avg = 0.0
        self.relPerf = 0.0
        
    #######################################
    #
    # Add Dataset
    #
    #######################################
    def addDatasetToChromatogram(self, timemark, signal):
        runTime = round(timemark - self.startTime, 3)

        print("Laufzeit:", runTime)
        print("Signal:", signal)
        print()
        print()
        self.original = np.append(self.original,[[runTime, signal]], axis=0)
        pass
        
    def loadChromatogramFromFile(self, filepath):
        """Load the chromatogram"""
        data = np.loadtxt(filepath,delimiter=',')
        d_time = data[:,0]
        d_signal = data[:,1]

        doDriftCorrection = True
        if (doDriftCorrection==True):
            #Do Drift correction
            startOffset = np.median(d_signal[:20])
            endOffset = np.median(d_signal[-20:])
            #print("START OFFSET: ", startOffset)
            #print("END OFFSET: ", endOffset)
            
            startTime = d_time[0]
            endTime = d_time[-1]
            gradient = (endOffset-startOffset)/(endTime-startTime)
            for i in range(len(d_signal)):
                d_signal[i] = d_signal[i] - gradient*d_time[i]
                pass

        
        doOffsetCorrection = True
        if (doOffsetCorrection==True):
            offset = (startOffset+endOffset)/2.0
            d_signal = d_signal - offset

        self.original = np.transpose([d_time, d_signal])
    
    def saveChromatogramToFile(self, filename):
        print("Save Chromatogram...")
        np.savetxt(filename, self.original, delimiter=',')
        print("done...")
        
    
 
    
class OptimizedChromatogram():
    def __init__(self, timeOriginal, signalOriginal):

        #Prepeare read-in chromatogram 
        time, signal = self.denoiseSignal(timeOriginal, signalOriginal)
        peakTime, yMin, yMax, xLeft, xRight, peakOffset = self.findPeaks(time, signal)

        self.time = time
        self.peakTime = peakTime.tolist()
        self.denoisedChromatogram = np.zeros(len(timeOriginal))
        self.denoisedPeaks = []
        self.area = []
        self.height = []
        self.xLeft = []
        self.xRight = []
        for index, peak in enumerate(peakTime):
            time, singePeakSignal, properties = self.fitPeak(time, signal, peakTime[index], xLeft[index], xRight[index], peakOffset[index])
            self.area.append(properties[0])
            self.height.append(properties[1])
            self.xLeft.append(properties[2])
            self.xRight.append(properties[3])
            
            self.denoisedPeaks.append(singePeakSignal)
            self.denoisedChromatogram += singePeakSignal


    def denoiseSignal(self, time, signal):
        #Smooth dataset and retun smoothend array
        dtime = (time[-1]-time[0])/len(time)
        print("dt of measured signal: ", dtime)
        windowLength = int(10/dtime)
        if (windowLength%2==0): windowLength+=1
        
        DEBUG_DISABLEDENOISE = False #!!!DISABLE DENOISE FOR PROFESSIONAL CHROMATOGRAMS!!!
        if DEBUG_DISABLEDENOISE == True:
            smoothSignal = signal
        else:
            import scipy.signal
            for i in range(10):
                smoothSignal = scipy.signal.savgol_filter(signal, windowLength, 6) 
        
        
        #No negativ values wanted for evaluation
        offset = np.amin(smoothSignal)
        if (offset<0): smoothSignal += abs(offset)
        if (offset>0): smoothSignal -= abs(offset)
        
        return time, smoothSignal
    
    
    
    def findPeaks(self, time, signal):
        """Find Peaks using SciPy, claculate Height and Width"""
        from scipy.signal import find_peaks
        from scipy.signal import peak_widths

        dt = (time[-1]-time[0])/len(time)
        noise = signal[-int(10/dt):]    #Sample last 10 seconds for noise
        std = np.std(noise)
        
        threshold = np.amax(signal)*0.20 #Evaluate only bigpeaks
        peakIndex, properties = find_peaks(signal, prominence=(threshold), width=5)      # Find peaks with Scipy
        
        peakTime = time[peakIndex]
    
        yMin = signal[peakIndex] - properties["prominences"]
        yMax = signal[peakIndex]
        peakHeight = yMax-yMin
        peakOffset = yMin

        #Calculate Peakwidth at rel.height=widthHeight
        widthHeight = 0.1
        peakWidth = peak_widths(signal, peakIndex, rel_height=(1.0-widthHeight))
           
        xError = abs(peakTime - peakIndex*dt) #Correct lost data-points
        
        xLeft = dt * peakWidth[2] + xError #Left Width
        xRight = dt * peakWidth[3] + xError #Right Width
        
        xLeft = peakTime-xLeft
        xRight = xRight-peakTime

        return peakTime, yMin, yMax, xLeft, xRight, peakOffset
    

    def exGauss(self, x, area, mu, sigma, lam):
        SQRT2 = 1.414213562
        
        K = 1.0/(sigma*lam)
        
        if (K<=0.05):
            print("ERROR! Peak skew is NOT possible with these settings. Fallback to symmetric peaks!")
            result = self.symGauss(x, area, mu, sigma)
        elif (K<100):
            from scipy.stats import exponnorm
            result = area * exponnorm.pdf(x, K, mu, sigma) 
        else:
            print("ERROR! Peak skew is NOT possible with these settings. Fallback to symmetric peaks!")
            result = self.symGauss(x, area, mu, sigma)

        return result
        
        
    def symGauss(self, x, area, mu, sigma):
        #Returns an Gauss-shaped Peak
        SQRT2 = 1.414213562
        return area * (1/(2*np.pi*sigma**2)**0.5) * np.exp(-((x-mu)/(SQRT2*sigma))**2.0)
    
    
    def fitPeak(self, time, signal, peakTime, xLeft, xRight, peakOffset):
        #
        # This function fits an exgaussian on the mesaured Data
        # Depending on the peakshapes, the options below may need changes
        #
        
        OPTION_DOUBLEPEAKS=True
        OPTION_PEAKSHAPE = "STANDARD"
        #OPTION_PEAKSHAPE = "SYMMETRIC"     
        #OPTION_PEAKSHAPE = "OPENTUBULAR"  
        #OPTION_PEAKSHAPE = "BIGBROAD" 
        
        #
        #
        #
        #
        #
        
        from scipy.optimize import curve_fit

        #Copy single peak from dataset
        dt = (time[-1]-time[0])/len(time)
        
        if (OPTION_DOUBLEPEAKS == True):
            if (xLeft>xRight): xLeft=xRight
            if (xRight>xLeft): xRight=xLeft
        
        startIndex = int((peakTime-1.5*xLeft)/dt)
        endIndex = int((peakTime+1.5*xRight)/dt)

        peakIndex = int(peakTime/dt)

        singleSignal = np.zeros(len(signal))
        singleSignal[startIndex:endIndex] += (signal[startIndex:endIndex])
        
        if (OPTION_PEAKSHAPE == "SYMMETRIC"): parameters, covariance = curve_fit(self.symGauss, time, singleSignal, p0=([1,peakTime,1])) #OPTION FOR SYMMETRIC PEAKS
        if (OPTION_PEAKSHAPE == "STANDARD"): parameters, covariance = curve_fit(self.exGauss, time, singleSignal, p0=([1,peakTime,10,1])) #STANDARD
        if (OPTION_PEAKSHAPE == "OPENTUBULAR"): parameters, covariance = curve_fit(self.exGauss, time, singleSignal, p0=([1e4,peakTime,10,0.5])) #OPTION FOR BIG BROAD PEAKS
        if (OPTION_PEAKSHAPE == "BIGBROAD"): parameters, covariance = curve_fit(self.exGauss, time, singleSignal, p0=([1e8,peakTime,1,1])) #OPTION FOR Professional OpenTubular GC
        
        #generate a seperate curve for this specific peak
        #time_fitted = np.linspace(0, int(time[-1]), len(time))
        signal_fitted = self.exGauss(time,parameters[0],parameters[1],parameters[2],parameters[3])

        from scipy.signal import find_peaks
        
        peakIndex, properties = find_peaks(signal_fitted, prominence=0, width=5)
        peakTime = time[peakIndex]
        
        #print("SIGNAL FITTED: ", properties)
                
        from scipy.signal import peak_widths
        widthHeight = 0.1
        peakWidth = peak_widths(signal_fitted, np.atleast_1d(peakIndex), rel_height=(1.0-widthHeight))

        xLeft = peakTime - (dt * peakWidth[2]) #Left Width
        xRight = (dt * peakWidth[3]) - peakTime  #Right Width
        
        area = np.trapz(signal_fitted, time)
        height = np.amax(signal_fitted)-np.amin(signal_fitted)
        parameters = [area, height, xLeft, xRight]
        
        #print("PARAMETERS: ", parameters)

        return time, signal_fitted, parameters
    
    
class IdealChromatogram():
    def __init__(self, deadTime, denoisedChromatogram):
        self.peakTime = np.array(denoisedChromatogram.peakTime)
        self.xLeft = np.array(denoisedChromatogram.xLeft)
        self.xRight = np.array(denoisedChromatogram.xRight)
        
        self.N_measured = self.measurePlates(self.peakTime, self.xLeft, self.xRight)
        self.N_calculated = calculatePlates.calculatePlates(self.peakTime, deadTime)
        self.performance = self.calcRelPerformance(self.N_measured, self.N_calculated)
    
    def measurePlates(self, peakTime, xLeft, xRight):
        #Calculate the plate Height using the Dorsey-Foley equation
        
        w01 = (xLeft+xRight)  #xLeft and xRight are absolute values
        w01 = w01.ravel()
        a = xLeft    #Convert absolute position to width
        b = xRight
        
        
        N_m = []
        for index,peak in enumerate(peakTime):
            N_measured = (41.7*((peakTime[index]/w01[index])**2)) / ((b[index]/a[index])+1.25) #Dorsey-Foley equation
            print("N MEASSURED: ", N_measured)
            N_m.append(N_measured)

        return np.transpose(np.array(N_m))


    def calcRelPerformance(self, N_measured, N_calculated):
        #Compare the measured performance with the calculated performance
        print("gemessene Trennstufenanzahl: ", N_measured)
        print("berechnete Trennstufenanzahl: ", N_calculated)
        
        avgRelPerformance = (np.average(N_measured) / np.average(N_calculated))

        print("Erreichte Performance: ", avgRelPerformance*100 , " Prozent")
        print()
        print()
        
        return avgRelPerformance