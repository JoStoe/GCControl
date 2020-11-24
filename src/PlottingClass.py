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


import wx
import numpy as np

import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
matplotlib.use('WXAgg')

#Set the fontsize of graphics globally
matplotlib.rcParams.update({'font.size': 14})


#----------------------------------------------------------------------
#plot an 2D-Array
#----------------------------------------------------------------------
class CanvasPanel(wx.Panel):
    def __init__(self, parent):
        
        wx.Panel.__init__(self, parent = parent)
        
        #Create the graphical panel
        width,height = parent.GetSize()
        self.figure = Figure(figsize=(width/90,height/90),dpi=90)
        self.canvas = FigureCanvas(parent, -1, self.figure)
        self.axes = self.figure.add_subplot(111)
 
        #Size the Graphical output
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.EXPAND, 5)
        parent.SetSizer( self.sizer )
        self.Fit()
        
    def clearPlot(self):
        #Clear
        self.axes.clear()
    
    def resetPlot(self):
        #Clear
        self.axes.clear()
        #Do the labeling
        self.axes.set_xlabel("Time [s]")
        self.axes.set_ylabel("Signal []")
        self.axes.set_xlim(0.0,120.0)
        #self.axes.set_ylim(0.0,0.2)
        self.canvas.draw()

    def plot(self,data,labelText,timeLimit,autoScale):
        
        #self.axes.clear()
        x = data[:,0]
        y = data[:,1]
        
        #Do auto-offset correction
        try:
            autoOffset = np.around(np.amin(y), decimals=3)
        except:
            autoOffset = 0.01
            print("Auto-offset failed...")
            
        #Do y-Axis streching / norming to 1
        try:
            yNorm = (1.0/np.around(np.amax(y-autoOffset), decimals=3))
            if (yNorm == np.inf) or  (yNorm == -np.inf): 
                yNorm=1.0
        except:
            yNorm = 1
            print("y-normation failed...")       
        
        #plot Graph
        if autoScale == True:
            self.axes.plot(x,(y-autoOffset)*yNorm,label=labelText,  linewidth=2.5)
        else:
            self.axes.plot(x,(y-autoOffset),label=labelText,  linewidth=2.5)
        
        endTime = x[-1]
        if (timeLimit == None):
            self.axes.set_xlim((0.0, endTime))
        else:
            self.axes.set_xlim((endTime-timeLimit, endTime))


        if autoScale == True:
            self.axes.set_ylim(bottom=0.0, top=1.0)
        
        #Do the labeling
        self.axes.set_xlabel("Time [s]")
        self.axes.set_ylabel("Signal []")    
        self.axes.legend()
        
        self.canvas.draw()
        
    
    def plotPeakInformation(self,peakIndex,yMin,yMax,xLeft,xRight):
        #Get info about the height of the peak
        peakHalfWidth = yMax-yMin

        #Plot Peaks
        self.axes.plot(peakIndex, yMax, "x")
    
        #Plot height of peaks
        self.axes.vlines(x=peakIndex, ymin=yMin,ymax = yMax, color = "C1", linestyle="--", linewidth=0.5)
    
        #Plot w01 of Peaks
        yPos = yMin+0.1*(yMax-yMin)*np.ones(peakIndex.size)
        self.axes.hlines(y=yPos, xmin=xLeft,xmax=xRight, color = "C1", linestyle="--", linewidth=0.5)


    





