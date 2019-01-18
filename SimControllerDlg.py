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
from __future__ import absolute_import
from builtins import str
from builtins import range
from qgis.PyQt.QtCore import Qt, pyqtSlot, QVariant 
from qgis.PyQt.QtWidgets import QApplication, QDialog, QFileDialog, QMessageBox
from qgis.core import QgsField
from .Ui_SimControllerDlg import Ui_SimControllerDlg
import os
import subprocess
from . import ControlFile

# create the dialog for SimControllerDlg
class SimControllerDlg(QDialog):
    def __init__(self, iface): 
        QDialog.__init__(self) 
        # Set up the user interface from Designer. 
        self.ui = Ui_SimControllerDlg()
        self.ui.setupUi(self)
        self.iface = iface
        self.mc = iface.mapCanvas() 
        self.layers = self.mc.layers() #Only returns visible (active) layers
        self.ui.textBrowser.document().setMaximumBlockCount(500)
        self.ui.btnRun.setEnabled(False)

    @pyqtSlot()
    def on_btnBrowse_clicked(self):            
        self.ui.btnRun.setEnabled(False)
        ofile, __ = QFileDialog.getOpenFileName(self,
                                           'Specify Simulation Control File:',
                                           os.getcwd(),
                                           '*.gsc') 
        
        if ofile != '':
            self.cfilename = ofile
            self.ui.tbxFile.setText(self.cfilename)
            os.chdir(os.path.dirname(str(ofile)))
            self.CheckControlFile()
                
    @pyqtSlot()
    def on_tbxFile_editingFinished(self):
        self.ui.btnRun.setEnabled(False)
        self.cfilename = self.ui.tbxFile.text()
        self.CheckControlFile()
 
    def CheckControlFile(self):
        
        #Open control file
        if not os.path.exists(self.cfilename):
            QMessageBox.critical(self,'Simulation Controller','Control file does not exist.')
            return
        else:
            self.cfile = ControlFile.ControlFile()
            ret = self.cfile.ReadFile(self.cfilename)
            if ret:
                QMessageBox.critical(self,'Simulation Controller','Error reading control file.')
                return 
                    
        #Set working directory
        if not os.path.exists(self.cfile.ModelDirectory):
            QMessageBox.critical(self,'Simulation Controller','Model directory does not exist.')
            return
        else:
            os.chdir(self.cfile.ModelDirectory)

        #Get base layer
        count = 0
        for i in self.layers:
            if i.name() == self.cfile.BaseLayer:
                self.blayer = i
                self.bprovider = self.blayer.dataProvider()
                count+=1
        if not count: #Count==0
            QMessageBox.critical(self,'Simulation Controller','Base layer not found.')
            return
        if count > 1:
            QMessageBox.critical(self,'Simulation Controller','Found more than one layer with base layer name.')
            return

        #Check template files
        for key in sorted(self.cfile.TemplateInput.keys()):
            if not os.path.exists(self.cfile.TemplateInput[key][0]):
                QMessageBox.critical(self,'Simulation Controller',
                                     'File does not exist: %s' % self.cfile.TemplateInput[key][0])
                return
            else:
                f = open(self.cfile.TemplateInput[key][0], 'r')
                lines = f.readlines()
                f.close()
                if lines[0][0:41] != 'Geospatial Simulation Template (GST) File':
                    QMessageBox.critical(self, 'Simulation Controller', 'Check template file.')
                    return
        
        #Check for input attributes in base layer
        for key in sorted(self.cfile.AttributeCode.keys()):
            bfindx = self.bprovider.fieldNameIndex(self.cfile.AttributeCode[key][0])
            if bfindx < 0:
                QMessageBox.critical(self,'Simulation Controller',
                                     'Missing attribute in base layer: %s' % self.cfile.AttributeCode[key][0])
                return
                
        #Check instruction files
        for key in sorted(self.cfile.InstructionOutput.keys()):
            if not os.path.exists(self.cfile.InstructionOutput[key][0]):
                QMessageBox.critical(self,'Simulation Controller',
                                     'File does not exist: %s' % self.cfile.InstructionOutput[key][0])
                return
            else:
                f = open(self.cfile.InstructionOutput[key][0], 'r')
                lines = f.readlines()
                f.close()
                if lines[0][0:44] != 'Geospatial Simulation Instruction (GSI) File':
                    QMessageBox.critical(self, 'Simulation Controller','Check instruction file.')
                    return
                for line in lines[1:]:
                    line = line.split(',')
                    if len(line) < 2:
                        continue
                    found = 0
                    for key in sorted(self.cfile.AttributeType.keys()):
                        if self.cfile.AttributeType[key][0] == line[0]:
                            found = 1
                            break
                    if not found:
                        QMessageBox.critical(self, 'Simulation Controller',
                                              'Check control file for missing output attribute: ' + line[0])
                        return 
                        
        #Check for output attributes in base layer.  Add if missing.
        for key in sorted(self.cfile.AttributeType.keys()):                                              
            typename = self.cfile.AttributeType[key][1].split('(')[0]
            length = self.cfile.AttributeType[key][1].split('(')[1]
            bfindx = self.bprovider.fieldNameIndex(self.cfile.AttributeType[key][0])
            if bfindx < 0: #Field not found, must add it
                newfield = QgsField()
                newfield.setName(self.cfile.AttributeType[key][0])
                if typename in ['String','string','STRING']:
                    newfield.setType(QVariant.String)
                    newfield.setTypeName('String')
                    newfield.setLength(int(length.split(')')[0]))
                elif typename in ['Integer', 'integer', 'INTEGER']:
                    newfield.setType(QVariant.Int)
                    newfield.setTypeName('Integer')
                    newfield.setLength(int(length.split(')')[0]))
                elif typename in ['Real', 'real', 'REAL']:
                    newfield.setType(QVariant.Double)
                    newfield.setTypeName('Real')
                    newfield.setLength(int(length.split('.')[0]))
                    newfield.setPrecision(int(length.split('.')[1].split(')')[0]))
                self.bprovider.addAttributes([newfield])
                
        #Enable Run button
        self.ui.btnRun.setEnabled(True)

    @pyqtSlot()
    def on_btnRun_clicked(self):
        
        #Initializations
        b1 = 0
        attr={}
        bfields = self.bprovider.fields()
        b2 = self.bprovider.featureCount()
        self.ui.ProgressBar.setValue(0)
        self.setCursor(Qt.WaitCursor)
        if self.ui.cbxOnlySelected.isChecked():
            selectedIDs = self.blayer.selectedFeatureIds()
            b2 = len(selectedIDs)
                 
        #Run simulations
        for bfeat in self.bprovider.getFeatures(): 
            
            if self.ui.cbxOnlySelected.isChecked():
                if bfeat.id() not in selectedIDs:
                    continue 
            
            b1+=1          
            #Write model input files
            for key1 in list(self.cfile.TemplateInput.keys()):
                f = open(self.cfile.TemplateInput[key1][0], 'r')
                lines = f.readlines()
                f.close()
                lines.pop(0)
                for key2 in list(self.cfile.AttributeCode.keys()):
                    bfindx = self.bprovider.fieldNameIndex(self.cfile.AttributeCode[key2][0])
                    value = bfeat.attribute(self.cfile.AttributeCode[key2][0])
                    ftype = str(bfields[bfindx].typeName())
                    code = self.cfile.AttributeCode[key2][1]
                    for i,line in enumerate(lines):
                        if ftype in ['String']:
                            svalue = value.rjust(len(code))
                        elif ftype in ['Integer','Integer64']:
                            myfmt = '%' + str(len(code)) + 'd'
                            svalue = myfmt % int(value)
                        elif ftype in ['Real','Double']:
                            if float(value) >= 0:
                                decnum = len(code) - len(str(int(value))) - 1
                            elif float(value) < 0:
                                decnum = len(code) - len(str(int(value))) - 2
                            myfmt = '%' + str(len(code)) + '.' + str(decnum) + 'f'
                            svalue = myfmt % round(float(value),decnum)
                        else:
                            self.setCursor(Qt.ArrowCursor)
                            QMessageBox.critical(self, 'Simulation Controller',
                                                 'ftype not found:' + str(ftype))
                            return
                        lines[i] = lines[i].replace(code,svalue)                
                f = open(self.cfile.TemplateInput[key1][1], 'w')
                for line in lines:
                    f.write(line)
                f.close()

            #Run model
            self.p = subprocess.run(self.cfile.CommandLine, 
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               shell=True,
                               text = True)
            self.ui.textBrowser.append(self.p.stdout)
            self.ui.textBrowser.append(self.p.stderr)
            
            #Read model output files
            attr.clear()
            for key in list(self.cfile.InstructionOutput.keys()):
                f = open(self.cfile.InstructionOutput[key][0], 'r')
                lines = f.readlines()
                f.close()
                lines.pop(0)
                f = open(self.cfile.InstructionOutput[key][1], 'r', errors='replace')
                output = f.readlines()
                f.close()
                for line in lines:
                    line = line.split(',')
                    if len(line) < 2:
                        continue
                    rownum = 0
                    bfindx = self.bprovider.fieldNameIndex(line[0])
                    for item in line[1:]:
                        if item[0:4] in ['Plus', 'plus', 'PLUS']:
                            rownum+=int(item[4:])
                        elif item[0:4] in ['Find', 'find', 'FIND']:
                            for i in range(rownum, len(output)):
                                start = output[i].find(item[4:])
                                if start >= 0:
                                    rownum = i
                                    break
                        elif item[0:3] in ['Get', 'get', 'GET']:
                            extents = item[3:].split(':')
                            extents = [int(i) for i in extents]
                            value = output[rownum][extents[0]:extents[1]]
                            attr.update({bfindx:value})
                        else:
                            self.setCursor(Qt.ArrowCursor)
                            QMessageBox.critical(self, 'Simulation Controller', 'Check instruction file commands.')
                            return
            result = self.bprovider.changeAttributeValues({bfeat.id():attr})
            if not result:
                self.setCursor(Qt.ArrowCursor)
                QMessageBox.critical(self, 'Simulation Controller', 'Could not change attribute value.')
                return  
                                      
            self.ui.ProgressBar.setValue(float(b1)/float(b2) * 100.0)
            QApplication.processEvents()
        
        self.setCursor(Qt.ArrowCursor)       
                                 
    @pyqtSlot()
    def on_btnExit_clicked(self):
        self.close() 
