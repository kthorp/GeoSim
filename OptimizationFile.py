"""
/***************************************************************************
Name                 : Geospatial Simulation
Description          : Geospatial tool for managing point-based simulation models
Date                 : 05/Dec/11 
copyright            : (C) 2011 by Dr. Kelly Thorp, USDA-ARS
email                : kelly.thorp@ars.usda.gov 
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from builtins import str
from builtins import object
import os

class OptimizationFile(object):
    "Read and write the simulation optimization file for Geospatial Simulation"
    
    def __init__(self):          
        self.ControlFile = ''
        self.BaseLayer = ''
        self.OptAttributes = {}
        self.ObjAttributes = {}
        self.T0 = 10.0
        self.Tf = None
        self.dwell = 10
        self.feps=0.05
        self.maxeval = None
        self.maxiter = 20
        self.maxaccept = None
        self.m = 1.0
        self.n = 1.0
        self.quench = 1.0
        self.boltzmann = 0.05
                
    def ReadFile(self, ofile):
        #Check if file exists.  If so, read it.
        if (os.path.exists(ofile)) == False:
            return 1
        else:       
            f = open(ofile, 'r')
            lines = f.readlines()
            f.close()
        
        #Check file type
        if lines[0].rstrip() != 'Geospatial Simulation Optimization (GSO) File':
            return 2

        #Get control file
        for i,line in enumerate(lines):
            if line[0:5] == '*GSO1':
                start = i
        self.ControlFile = lines[start+1].rstrip()
        
        #Get base layer
        for i,line in enumerate(lines):
            if line[0:5] == '*GSO2':
                start = i
        self.BaseLayer = lines[start+1].rstrip()
        
        #Get input parameter attributes, initial conditions, lower bound, upper bound, and code
        for i,line in enumerate(lines):
            if line[0:5] == '*GSO3':
                start = i
            if line[0:5] == '*GSO4':
                end = i
        items = lines[start+1:end-1]
        for i,item in enumerate(items):
            item = item.split(',')
            self.OptAttributes.update({i : [item[0],item[1],item[2],item[3],item[4].rstrip()]})
            
        #Get measured and simulated attributes
        for i,line in enumerate(lines):
            if line[0:5] == '*GSO4':
                start = i
            if line[0:5] == '*GSO5':
                end = i
        items = lines[start+1:end-1]
        for i,item in enumerate(items):
            item = item.split(',')
            self.ObjAttributes.update({i : [item[0],item[1],item[2].rstrip()]})
            
        #Get simulated annealing parameters
        for i,line in enumerate(lines):
            if line[0:5] == '*GSO5':
                start = i 
        self.T0 = float(lines[start+1])
        try:
            self.Tf = float(lines[start+2])
        except:
            self.Tf = None
        self.dwell = int(float(lines[start+3]))
        try:
            self.feps = float(lines[start+4])
        except:
            self.feps = None
        try:
            self.maxeval = int(lines[start+5])
        except:
            self.maxeval = None
        try:
            self.maxiter = int(lines[start+6])
        except:
            self.maxiter = None
        try:
            self.maxaccept = int(lines[start+7])
        except:
            self.maxaccept = None
        self.m = float(lines[start+8])
        self.n = float(lines[start+9])
        self.quench = float(lines[start+10])
        self.boltzmann = float(lines[start+11])
        
        return 0
    
    def WriteFile(self, ofile):  
        f = open(ofile, 'w')
        f.write('Geospatial Simulation Optimization (GSO) File\n\n')
        f.write('*GSO1: ControlFile\n')
        f.write(self.ControlFile + '\n\n')
        f.write('*GSO2: BaseLayer\n')
        f.write(self.BaseLayer + '\n\n')
        f.write('*GSO3: Parameter,Initial,LB,UB,Code\n')
        for key in sorted(self.OptAttributes.keys()):
            item = self.OptAttributes[key]
            f.write(item[0] + ',' + item[1] + ',' + item[2] + ',' + item[3] + ',' + item[4] + '\n')
        f.write('\n')
        f.write('*GSO4: Measured,Simulated,Factor\n')
        for key in sorted(self.ObjAttributes.keys()):
            item = self.ObjAttributes[key]
            f.write(item[0] + ',' + item[1] + ',' + item[2] + '\n')
        f.write('\n')
        f.write('*GSO5: AnnealingParameters\n')
        f.write(str(self.T0) + '\n')
        f.write(str(self.Tf) + '\n')
        f.write(str(self.dwell) + '\n')
        f.write(str(self.feps) + '\n')
        f.write(str(self.maxeval) + '\n')
        f.write(str(self.maxiter) + '\n')
        f.write(str(self.maxaccept) + '\n')
        f.write(str(self.m) + '\n')
        f.write(str(self.n) + '\n')
        f.write(str(self.quench) + '\n')
        f.write(str(self.boltzmann) + '\n')     
