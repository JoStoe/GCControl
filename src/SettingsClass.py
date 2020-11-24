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


import matplotlib
matplotlib.use('WXAgg')

class Settings():
    def __init__(self):
        #Constructor
        #Set variables to the default
        self.colLength = 1.0
        self.colDiameter = 4.0
        self.arduinoPath = "/dev/ttyACM0"
        self.enableSimulation = "False"

        
    def loadSettings(self):
        #Read in Settings
        try:
         file1 = open("settings.ini", "r")
         SettingsFile = file1.readlines() 
         file1.close()
         
         print(SettingsFile)
         
         for x in SettingsFile:
            ID = (x[0:x.find("=")]) 
            value = (x[x.find("=")+1 :]) 
       
            if (ID == "COLUMN_LENGTH"): self.colLength = float(value)
            if (ID == "COLUMN_DIAMETER"): self.colDiameter = float(value)
            if (ID == "ARDUINO_PATH"): self.arduinoPath = str(value[:-1]) #Cut-off \n
            if (ID == "SIMULATION"): self.enableSimulation = str(value[:-1]) #Cut-off \n
            
        except:
            print("ERROR while loading settings data")
  
    def saveSettings(self):
        try:
            #Write Settings file
            f = open("settings.ini", "w")
            f.write("COLUMN_LENGTH=" + str(self.colLength) + "\n") 
            f.write("COLUMN_DIAMETER=" + str(self.colDiameter) + "\n")
            f.write("ARDUINO_PATH=" + str(self.arduinoPath) + "\n")
            f.write("SIMULATION=" + str(self.enableSimulation) + "\n") 
            f.close()
        except:
            print("ERROR while saving settings data")
        
