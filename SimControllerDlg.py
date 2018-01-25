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
from qgis.PyQt.QtCore import Qt 
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
        self.cfilename = ''
        self.stdout = ''
        self.stderr = ''
        
        self.ui.textBrowser.document().setMaximumBlockCount(500)

    @pyqtSignature("on_btnBrowse_clicked()")
    def on_btnBrowse_clicked(self):            
        ofile, __ = QFileDialog.getOpenFileName(self,
                                           'Specify Simulation Control File:',
                                           os.getcwd(),
                                           '*.gsc') 
        
        if ofile != '':
            self.cfilename = ofile
            self.ui.tbxFile.setText(self.cfilename)
            os.chdir(os.path.dirname(str(ofile)))
                
    @pyqtSignature("on_tbxFile_textEdited(QString)")
    def on_tbxFile_textEdited(self):
        self.cfilename = self.ui.tbxFile.text()
 
    @pyqtSignature("on_btnRun_clicked()")
    def on_btnRun_clicked(self):
                
        #Open control file
        if not os.path.exists(self.cfilename):
            QMessageBox.critical(self,'Simulation Controller','File does not exist.')
            return
        else:
            cfile = ControlFile.ControlFile()
            ret = cfile.ReadFile(self.cfilename)
            if ret:
                QMessageBox.critical(self,'Simulation Controller','Error reading file.')
                return 
                    
        #Set working directory
        if not os.path.exists(cfile.ModelDirectory):
            QMessageBox.critical(self,'Simulation Controller','Model directory does not exist.')
            return
        else:
            os.chdir(cfile.ModelDirectory)

        #Get base layer
        flag = 1
        for i in self.layers:
            if i.name() == cfile.BaseLayer:
                blayer = i
                bprovider = blayer.dataProvider()
                bfields = bprovider.fields()
                flag = 0
                break
        if flag:
            QMessageBox.critical(self,'Simulation Controller','Base layer not found.')
            return
        
        #Initializations
        b1 = 0
        attr={}
        b2 = bprovider.featureCount()
        self.ui.ProgressBar.setValue(0)
        self.setCursor(Qt.WaitCursor)
        if self.ui.cbxOnlySelected.isChecked():
            selectedIDs = blayer.selectedFeaturesIds()
            b2 = len(selectedIDs)
            
        #Add new attributes to base layer
        for key in sorted(cfile.AttributeType.keys()):                                              
            typename = cfile.AttributeType[key][1].split('(')[0]
            length = cfile.AttributeType[key][1].split('(')[1]
            bfindx = bprovider.fieldNameIndex(cfile.AttributeType[key][0])
            if bfindx < 0: #Field not found, must add it
                newfield = QgsField()
                newfield.setName(cfile.AttributeType[key][0])
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
                bprovider.addAttributes([newfield])
                 
        #Run simulations
        for bfeat in bprovider.getFeatures(): 
            
            if self.ui.cbxOnlySelected.isChecked():
                if bfeat.id() not in selectedIDs:
                    continue 
            
            b1+=1          
            #Write model input files
            for key1 in list(cfile.TemplateInput.keys()):
                f = open(cfile.TemplateInput[key1][0], 'r')
                lines = f.readlines()
                f.close()
                if lines[0][0:41] != 'Geospatial Simulation Template (GST) File':
                    self.setCursor(Qt.ArrowCursor)
                    QMessageBox.critical(self, 'Simulation Controller',
                                         'Check template file.')
                    return
                else:
                    lines.pop(0)
                    
                for key2 in list(cfile.AttributeCode.keys()):    
                    bfindx = bprovider.fieldNameIndex(cfile.AttributeCode[key2][0])
                    value = bfeat.attribute(cfile.AttributeCode[key2][0])
                    ftype = str(bfields[bfindx].typeName())
                    code = cfile.AttributeCode[key2][1]
                    for i,line in enumerate(lines):
                        start = 1
                        while start > 0:
                            start = lines[i].find(code)
                            if start >= 0:
                                if ftype in ['Integer']:
                                    myfmt = '%' + str(len(code)) + 'd'
                                    lines[i] = lines[i][:start] + myfmt % int(value) + lines[i][(start+len(code)):]
                                elif ftype in ['Real', 'Double']:
                                    if float(value) >= 0:
                                        decnum = len(code) - len(str(int(value))) - 1
                                    elif float(value) < 0:
                                        decnum = len(code) - len(str(int(value))) - 2
                                    myfmt = '%' + str(len(code)) + '.' + str(decnum) + 'f'
                                    lines[i] = lines[i][:start] + myfmt % round(float(value),decnum) + lines[i][(start+len(code)):]
                f = open(cfile.TemplateInput[key1][1], 'w')
                for line in lines:
                    f.write(line)
                f.close()
            
            #os.system(command)
            p = subprocess.Popen(cfile.CommandLine, 
                                 stdout=subprocess.PIPE, 
                                 stdin=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 shell=True)
            self.stdout = p.stdout.readlines()
            for line in self.stdout:
                self.ui.textBrowser.append(line)
            self.stderr = p.stderr.readlines()
            for line in self.stderr:
                self.ui.textBrowser.append(line)
            
            #Read model output files
            attr.clear()
            for key1 in list(cfile.InstructionOutput.keys()):
                f = open(cfile.InstructionOutput[key1][0], 'r')
                lines = f.readlines()
                f.close()
                if lines[0][0:44] != 'Geospatial Simulation Instruction (GSI) File':
                    self.setCursor(Qt.ArrowCursor)
                    QMessageBox.critical(self, 'Simulation Controller',
                                         'Check instruction file.')
                    return
                else:
                    lines.pop(0)
                
                f = open(cfile.InstructionOutput[key1][1], 'r')
                output = f.readlines()
                f.close()
                
                for line in lines:
                    line = line.split(',')
                    if len(line) < 2:
                        continue
                    rownum = 0
                    found = 0
                    for key2 in sorted(cfile.AttributeType.keys()):
                        if cfile.AttributeType[key2][0] == line[0]:
                            found = 1
                            break
                    if found:                                
                        bfindx = bprovider.fieldNameIndex(line[0]) 
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
                         QMessageBox.critical(self, 'Simulation Controller',
                                              'Check control file for missing output attribute:' + line[0])
                         return                
            result = bprovider.changeAttributeValues({bfeat.id():attr})
            if not result:
                self.setCursor(Qt.ArrowCursor)
                QMessageBox.critical(self, 'Simulation Controller', 'Could not change attribute value.')
                return  

                            
            self.ui.ProgressBar.setValue(float(b1)/float(b2) * 100.0)
            QApplication.processEvents()
        
        self.setCursor(Qt.ArrowCursor)       
                                 
    @pyqtSignature("on_btnExit_clicked()")
    def on_btnExit_clicked(self):
        self.close() 
