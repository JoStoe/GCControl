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
import src.SettingsClass as SettingsClass
import src.ColumnClass as ColumnClass


def calculatePlates(peakTimes, deadTime):
    """
    # 
    # This function calculates the number of theoretical plates for each peak
    #
    """

    tr = peakTimes
    tm = deadTime

    """Load Settings"""
    globalSettings = SettingsClass.Settings()
    globalSettings.loadSettings()
    
    columnDiameter = globalSettings.colDiameter
    length = globalSettings.colLength  #Säulenlänge in Meter
    
    #Create a Column-Object
    column = ColumnClass.ColumnClass()
    column.loadVanDeemterParam("VanDeemterParam.dat")
 
    #Set Parameters
    dp = column.VD_dp  #250*1e-6   #Partikeldurchmesser µm
    #!!Die Trennleistung wird besser wenn Dliq größer und Dgas kleiner wird.
    Dgas = column.VD_Dgas
    Dliq = column.VD_Dliq
    lamda = column.VD_lambda
    gamma = 0.6
    columnDiameter = globalSettings.colDiameter
    length = globalSettings.colLength  #Säulenlänge in Meter
    
    k = (tr-tm)/tm
    df = column.VD_df   #10microns, #Wert von Van-Deempter Paper, Seite 286

    A = 2.0*lamda*dp
    B = 2.0*gamma*Dgas
    C = (8.0/(np.pi**2.)) * (k/((1.+k)**2.)) * (df**2.)/(Dliq)
    Cavg = np.average(C)
    
    """
    print("A: ", A)
    print("B: ", B)
    print("C: ", Cavg)
    """
    
    #Find Optimums
    uOpt = np.sqrt(B/C)
    hMin = A + 2.0*np.sqrt(B*C)
    
    N_calculated = length/hMin
    return N_calculated