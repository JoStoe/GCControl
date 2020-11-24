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


class ColumnClass():
    
    def __init__(self):
        #Set default Values
        self.carrierGas = "He"
        self.VD_dp = 0.00025
        self.VD_lambda = 2.0
        self.VD_df = 9.999999999999999e-06
        self.VD_Dgas = 3.554211378673236e-05
        self.VD_Dliq = 1.3794667876375783e-09
        
    def loadVanDeemterParam(self, filepath):
        """Load parameters of the column"""
        try:
            f = open(filepath, "r")
            t = (f.readline())
            t, mobilePhase = f.readline().split("=")
            t, dp = f.readline().split("=")
            t, lamb = f.readline().split("=")
            t, df = f.readline().split("=")
            t, Dgas = f.readline().split("=")
            t, Dliq = f.readline().split("=")
        
            dp = float(dp)
            lamb = float(lamb)
            df = float(df)
            Dgas = float(Dgas)
            Dliq = float(Dliq)
            
        except:
            print("ERROR loading column parameters ...")
            print("Set default parameters")
            #If error then set precalculated default values
            mobilePhase = "He"
            dp = 0.00025
            lamb = 2.0
            df = 9.999999999999999e-06
            Dgas = 3.554211378673236e-05
            Dliq = 1.3794667876375783e-09
            
        self.carrierGas = mobilePhase
        self.VD_lambda = lamb
        self.VD_dp = dp
        self.VD_df = df
        self.VD_Dgas = Dgas
        self.VD_Dliq = Dliq
        
        return 0