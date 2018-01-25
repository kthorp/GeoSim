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
from builtins import object
import os

class ControlFile(object):
    "Read and write the simulation control file for Geospatial Simulation"
    
    def __init__(self):          
        self.ModelDirectory = ''
        self.BaseLayer = ''
        self.TemplateInput = {}
        self.AttributeCode = {}
        self.InstructionOutput = {}
        self.AttributeType = {}
        self.CommandLine = ''
                
    def ReadFile(self, cfile):
        #Check if file exists.  If so, read it.
        if (os.path.exists(cfile)) == False:
            return 1
        else:       
            f = open(cfile, 'r')
            lines = f.readlines()
            f.close()
        
        #Check file type
        if lines[0].rstrip() != 'Geospatial Simulation Control (GSC) File':
            return 2
            
        #Set working directory
        for i,line in enumerate(lines):
            if line[0:5] == '*GSC1':
                start = i
        self.ModelDirectory = lines[start+1].rstrip()

        #Get base layer
        for i,line in enumerate(lines):
            if line[0:5] == '*GSC2':
                start = i
        self.BaseLayer = lines[start+1].rstrip()
        
        #Get template file and input file relations
        for i,line in enumerate(lines):
            if line[0:5] == '*GSC3':
                start = i
            if line[0:5] == '*GSC4':
                end = i
        items = lines[start+1:end-1]
        for i,item in enumerate(items):
            item = item.split(',')
            self.TemplateInput.update({i : [item[0],item[1].rstrip()]})
            
        #Get attribute and code relations for model inputs
        for i,line in enumerate(lines):
            if line[0:5] == '*GSC4':
                start = i
            if line[0:5] == '*GSC5':
                end = i
        items = lines[start+1:end-1]
        for i,item in enumerate(items):
            item = item.split(',')
            self.AttributeCode.update({i : [item[0],item[1].rstrip()]})
            
        #Get instruction file and output file relations
        for i,line in enumerate(lines):
            if line[0:5] == '*GSC5':
                start = i
            if line[0:5] == '*GSC6':
                end = i
        items = lines[start+1:end-1]
        for i,item in enumerate(items):
            item = item.split(',')
            self.InstructionOutput.update({i : [item[0],item[1].rstrip()]})
        
        #Get attribute and type of model outputs
        for i,line in enumerate(lines):
            if line[0:5] == '*GSC6':
                start = i
            if line[0:5] == '*GSC7':
                end = i
        items = lines[start+1:end-1]
        self.AttributeType = {}
        for i,item in enumerate(items):
            item = item.split(',')
            self.AttributeType.update({i : [item[0],item[1].rstrip()]})
            
        #Get command line
        for i,line in enumerate(lines):
            if line[0:5] == '*GSC7':
                start = i
        self.CommandLine = lines[start+1].rstrip()
        
        return 0
    
    def WriteFile(self, cfile):  
        f = open(cfile, 'w')
        f.write('Geospatial Simulation Control (GSC) File\n\n')
        f.write('*GSC1: ModelDirectory\n')
        f.write(self.ModelDirectory + '\n\n')
        f.write('*GSC2: BaseLayer\n')
        f.write(self.BaseLayer + '\n\n')
        f.write('*GSC3: TemplateFile,InputFile\n')
        for key in sorted(self.TemplateInput.keys()):
            item = self.TemplateInput[key]
            f.write(item[0] + ',' + item[1] + '\n')
        f.write('\n')
        f.write('*GSC4: InputAttribute,Code\n')
        for key in sorted(self.AttributeCode.keys()):
            item = self.AttributeCode[key]
            f.write(item[0] + ',' + item[1] + '\n')
        f.write('\n')
        f.write('*GSC5: InstructionFile,OutputFile\n')
        for key in sorted(self.InstructionOutput.keys()):
            item = self.InstructionOutput[key]
            f.write(item[0] + ',' + item[1] + '\n')
        f.write('\n')
        f.write('*GSC6: OutputAttribute,Type\n')
        for key in sorted(self.AttributeType.keys()):
            item = self.AttributeType[key]
            f.write(item[0] + ',' + item[1] + '\n')
        f.write('\n')
        f.write('*GSC7: CommandLine\n')
        f.write(self.CommandLine + '\n')
        f.close()
        