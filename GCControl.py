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
#
#    The main structure is based on the tutorial provided by: https://wiki.wxpython.org/AnotherTutorial#First_Steps


import wx
import time 
from src.GCControl_Forms import MainFrame_preset
from src.GCControl_Forms import AboutFrame_preset
from src.GCControl_Forms import SettingsFrame_preset

import src.SettingsClass as SettingsClass
import src.SimulationClass as SimulationClass
import src.PlottingClass as plot
import src.ChromatogramClass as ChromatogramClass
import src.ArduinoClass as ArduinoClass

#----------------------------------------------------------------------
# Programming of the GUI
#----------------------------------------------------------------------
        
class AboutFrame(AboutFrame_preset):
    #
    # GUI programming of the About Window
    #
    def b_close_click( self, event ):
        self.Close()
        
    def AboutFrame_OnClose(self, event):
        self.Destroy()



class SettingsFrame(SettingsFrame_preset):
    #
    # GUI programming of the Settings Window
    #
    def __init__(self, parent):
        SettingsFrame_preset.__init__(self, parent)
        self.globalSettings = SettingsClass.Settings()
        self.globalSettings.loadSettings()
        
        self.m_columLength.SetValue( self.globalSettings.colLength )
        self.m_columnID.SetValue(  self.globalSettings.colDiameter  )
        self.text_ArduinoLoc.SetValue(  self.globalSettings.arduinoPath  )
        
        if (str(self.globalSettings.enableSimulation) == "True"):
            self.checkBox_Simulate.SetValue(True)
        else:
            self.checkBox_Simulate.SetValue(False)
        
    def b_settings_ok_click( self, event ):
        
        self.globalSettings.colLength = self.m_columLength.GetValue()
        self.globalSettings.colDiameter = self.m_columnID.GetValue()
        self.globalSettings.arduinoPath = self.text_ArduinoLoc.GetValue()
        
        if (self.checkBox_Simulate.GetValue() == True):
            self.globalSettings.enableSimulation = "True"
        else:
            self.globalSettings.enableSimulation = "False"
        
        self.globalSettings.saveSettings()
        self.Close();
        
    def SettingsFrame_OnClose(self, event):
        self.Destroy()
        
    
class MainFrame(MainFrame_preset):
    #
    # GUI programming of the Main GCControl Window
    #
    def MainWindow_OnStartup( self, event ):
        #Create an data-object
        self.data = ChromatogramClass.Chromatogram()
        
        #Safe start-up time
        self.startUpTime = time.time()
        
        #Create Panel
        self.mainPanel = plot.CanvasPanel(self.panel_graphic)
        self.mainPanel.clearPlot()
        self.m_statusBar.SetStatusText('All practical experiments conducted in combination with this software can be dangerous and are carried out at your own risk! Take care!')
        
    def MainWindow_OnClose(self, event):
        self.Destroy()
        
        
    def timer_signal( self, event ):
        signal = self.arduino.readArduino()
        timemark = round(time.time() - self.startUpTime, 3)
        if (signal != None): #First Dataset after init alway none
            self.data.addDatasetToChromatogram(timemark, signal)
        
        self.mainPanel.clearPlot()
        self.mainPanel.plot(self.data.original,"chromatogram", timeLimit=120, autoScale=True)
        

    def timer_simulation_signal( self, event ):
        timemark = round(time.time() - self.startUpTime,3)
        runTime = round(timemark - self.data.startTime, 3)
        
        timeColumn = self.data.original[:,0]
        dt = (timeColumn[-1]-timeColumn[0])/len(timeColumn)
        actualIndex = int(runTime/dt)
        
        if (actualIndex >= len(timeColumn)): actualIndex=len(timeColumn)-1 #Stop chromatogram after reaching end of simulated area

        self.mainPanel.clearPlot()
        self.mainPanel.plot(self.data.original[:actualIndex,:actualIndex],"simulated chromatogram", timeLimit=120, autoScale=True)
        

    def m_load_click( self, event ):
        filePath = self.openDialog()
        if (filePath != None):
            self.data.loadChromatogramFromFile(filePath)
            #panel = plot.CanvasPanel(self.panel_graphic)
            self.mainPanel.clearPlot()
            self.mainPanel.plot(self.data.original,"chromatogram", timeLimit=None, autoScale=True)
    
    def m_save_click(self, event):
        filePath = self.saveDialog()
        if (filePath != None):
            self.data.saveChromatogramToFile(filePath)
        
    def m_close_click( self, event ):
        self.Close()

    def m_about_click( self, event ):
        aboutFrame = AboutFrame(None)
        aboutFrame.ShowModal()

    def b_readArduino_click( self, event ):
        #Load Arduino Adress
        Settings = SettingsClass.Settings()
        Settings.loadSettings()
        
        if (Settings.enableSimulation == "False"):
            self.arduino = ArduinoClass.ArduinoReader(serialPort=Settings.arduinoPath)
            self.timer_arduinoRead.Start( 250 ) #Enable timer event
            self.data.startNewChromatogram(time.time() - self.startUpTime) #Start a new Chromatogram
        else:
            simParam = SimulationClass.LoadSimParameters("sample.dat")
            parameters = [simParam.skewFactor, simParam.noiseLevel, simParam.driftFactor, simParam.speed]
            simChromatogram = SimulationClass.SimulatedChromatogram(simParam.peakTimes,simParam.peakArea,simParam.N_calculated,parameters)
            
            self.data.startNewChromatogram(time.time() - self.startUpTime) #Start a new Chromatogram
            self.data.original = simChromatogram.data
            self.timer_simulation.Start( 250 ) #Disable timer event #Disable timer event.Start( 250 ) #Enable timer event
        
    def b_simulate_click(self, event):     
        simParam = SimulationClass.LoadSimParameters("sample.dat")
        self.m_DeadTime.SetValue(float(simParam.deadTime*60))
        
        parameters = [simParam.skewFactor, simParam.noiseLevel, simParam.driftFactor, simParam.speed]
        simChromatogram = SimulationClass.SimulatedChromatogram(simParam.peakTimes,simParam.peakArea,simParam.N_calculated,parameters)

        self.mainPanel.clearPlot()
        self.mainPanel.plot(simChromatogram.data, "simulated chromatogram", timeLimit=None, autoScale=False)

    def b_stopArduino_click( self, event ):
        self.t_perfOutput.AppendText("Arduino stoped!\n")
        self.timer_arduinoRead.Stop() #Disable timer event
        self.timer_simulation.Stop() #Disable timer event
        self.arduino.closeArduino()

    def b_saveData_click( self, event ):
        #Save the data
        filePath = self.saveDialog()
        if (filePath != None):
            self.data.saveChromatogramToFile(filePath)

    def b_GCSettings_click( self, event ):
        settingsFrame = SettingsFrame(None)
        settingsFrame.ShowModal()
        
    def b_evaluate_click( self, event ):
        #Read in deadTime from GUI
        deadTime = float(self.m_DeadTime.GetValue())
        
        #plot chromatogram
        self.mainPanel.clearPlot()
        self.mainPanel.plot(self.data.original,"chromatogram", timeLimit=120, autoScale=False)
        
        #Do the evaluations of the chromatogram
        time_original = self.data.original[:,0]
        signal_original = self.data.original[:,1]
        self.denoisedChrom = ChromatogramClass.OptimizedChromatogram(time_original, signal_original)
        

        import numpy as np
        for index, peak in enumerate(self.denoisedChrom.denoisedPeaks):
            x = self.denoisedChrom.time
            y = self.denoisedChrom.denoisedPeaks[index]
            
            #self.mainPanel.plot(np.transpose(np.array([x,y])),labelText="optimized peak",timeLimit=None, autoScale=False)
        
        self.idealChrom = ChromatogramClass.IdealChromatogram(deadTime, self.denoisedChrom)
        
        self.data.peakPos = np.array(self.denoisedChrom.peakTime)
        self.data.peakArea = np.array(self.denoisedChrom.area)
        self.data.N_calculated_global = self.idealChrom.N_calculated
        self.data.N_calculated_avg = np.average(self.idealChrom.N_calculated)
        self.data.N_measured_global = self.idealChrom.N_measured       
        self.data.N_measured_avg = np.average(self.idealChrom.N_measured)
        self.data.totalRelPerf = self.data.N_measured_avg / self.data.N_calculated_avg
        
        #Plot the ideal Chromatogram
        
        """Load Settings"""
        globalSettings = SettingsClass.Settings()
        globalSettings.loadSettings()
        
        columnLength = globalSettings.colLength  #Säulenlänge in Meter
    
        print("#######################################################")
        print("#######################################################")
        print("")
        print("PeakPos: ", self.data.peakPos)
        print("PeakArea: ", self.data.peakArea)
        print("Calculated Number of Plates: ", self.data.N_calculated_global)
        print("Measured Number of Plates: ", self.data.N_measured_global)    
        print("")
        print("#######################################################")
        print("#######################################################")
        
        #Plot the denoised chromatogram
        #panel.plot(self.data.denoised,"Data denoised")

        #Print to output-box
        self.t_perfOutput.Clear()
        self.t_perfOutput.AppendText("Deadtime: " + '{:.1f}'.format(deadTime) + " sec\n")
        self.t_perfOutput.AppendText("Column-length: " + '{:.1f}'.format(columnLength) + " m\n")
        self.t_perfOutput.AppendText("Measured number of plates: " + '{:.1f}'.format(self.data.N_measured_avg) + "\n")
        self.t_perfOutput.AppendText("Expected number of plates: " + '{:.1f}'.format(self.data.N_calculated_avg) + "\n")
        self.t_perfOutput.AppendText("relative performance: " + '{:.1f}'.format(self.data.totalRelPerf*100) + " %\n")
        
        simChromatogram = SimulationClass.SimulatedChromatogram(self.data.peakPos, self.data.peakArea, self.data.N_calculated_global)
        self.mainPanel.plot(simChromatogram.data, "ideal chromatogram", timeLimit=None, autoScale=False)
    
        
    def openDialog(self):
        with wx.FileDialog(self, "Open chromatography data", wildcard="chromatography files (*.txt)|*.txt", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return None   # the user changed their mind
            # save the current contents in the file
            pathName = fileDialog.GetPath()
            try:
                print(pathName + " loaded...")
            except IOError:
                wx.LogError("Error while loading data '%s'." % pathName)
                print("Error while loading data '%s'." % pathName)
                return None
            
        return pathName
    
    def saveDialog(self):
        with wx.FileDialog(self, "Save chromatography data", wildcard="chromatography files (*.txt)|*.txt", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return None    # the user changed their mind
            
            # save the current contents in the file
            pathName = fileDialog.GetPath()
            try:
                print("Path to save: " + pathName)
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % pathName)
            
        return pathName            

#----------------------------------------------------------------------
# Application Startup
#----------------------------------------------------------------------

class Application(wx.App):
    def OnInit(self):
        frame = MainFrame(None)
        self.SetTopWindow(frame)
       
        #Set minimum size of the window
        sizeOfFrame = frame.GetSize()
        frame.SetMinSize((sizeOfFrame[0], sizeOfFrame[1]))
        
        #Set Icon
        frame.SetIcon(wx.Icon("./img/icon.png"))

        frame.Show(True)

        return True
        
if __name__ == '__main__':    
    main = Application(redirect=False)
    main.MainLoop()
