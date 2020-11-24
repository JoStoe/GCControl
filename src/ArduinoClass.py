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


class ArduinoReader():
    def __init__(self, serialPort):
        
        import serial
        self.serialInput = serial.Serial(serialPort, 9600, timeout=1.0) 
        self.serialInput.reset_input_buffer()


    def readArduino(self):
        try:
            #Read all data from serial buffer
            bytesToRead = self.serialInput.inWaiting()
            data_raw = self.serialInput.read(bytesToRead)
            data_raw = data_raw.decode("utf-8")
            
            #Clear Buffer
            self.serialInput.reset_input_buffer()
            self.serialInput.reset_output_buffer()
            
            #Split
            signal = data_raw.split("\r\n")
            del data_raw
            
            #Cut-off last element if empty
            if (signal[-1]==''): 
                signal = signal[0:-1]
                
            if len(signal)<1: return None
            
            #Let's check if the data was fully transmitted
            #The data has the format "<<DATA>>"
            #To be verified, the first and last twi chars must be as expected
            sol = []
            for i in signal:
                if len(i)>4:
                    if ((i[0:2]=="<<") and (i[-2:]==">>")):
                        sol.append(i[2:-2])
            
            del signal
            
            import numpy as np
            signal_value = np.average( np.array(sol,dtype=float) )

            import math
            if math.isnan(signal_value) == False:
                return signal_value
            else:
                return None
            

        except:
            print("ERROR WHILE CONNECTING TO THE ARDUINO")
            return(None)
        
    
    def closeArduino(self):
        self.serialInput.close()
