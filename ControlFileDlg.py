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
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QDialog, QFileDialog, QComboBox, QMessageBox, QTableWidgetItem
from qgis.core import QgsMapLayer, QgsProject, QgsWkbTypes
from .Ui_ControlFileDlg import Ui_ControlFileDlg
from . import ControlFile
import os

# create the dialog for ControlFileDlg
class ControlFileDlg(QDialog):
    def __init__(self, iface): 
        QDialog.__init__(self) 
        # Set up the user interface from Designer. 
        self.ui = Ui_ControlFileDlg()
        self.ui.setupUi(self)
        self.iface = iface
        self.mc = iface.mapCanvas() 
        self.layers = self.mc.layers() #Only returns visible (active) layers
        
        for i in self.layers:
            if i.type() == QgsMapLayer.VectorLayer:
                if i.geometryType() == QgsWkbTypes.PolygonGeometry:
                    self.ui.cmbBaseLayer.addItem(i.name(), i.id())
        bindex = self.ui.cmbBaseLayer.currentIndex()
        self.on_cmbBaseLayer_activated(bindex)
        
        self.ui.btnBrowse.setFocus()
                    
    @pyqtSlot()
    def on_btnBrowse_clicked(self):    
        mdir = QFileDialog.getExistingDirectory(self,'Specify Model Directory:') 
        if mdir != '':
            self.ui.tbxModelDirectory.setText(mdir)
    
    @pyqtSlot(int)
    def on_cmbBaseLayer_activated(self, index):
        if self.ui.cmbBaseLayer.count() > 0:
            bid = self.ui.cmbBaseLayer.itemData(index)
            self.blayer = QgsProject.instance().mapLayer(str(bid))
            
    @pyqtSlot(int,int)
    def on_tblAttributeCode_cellDoubleClicked(self, row, col):
        if self.ui.cmbBaseLayer.count() > 0 and col == 0:
            newcmb = QComboBox()
            bprovider = self.blayer.dataProvider()
            fields = bprovider.fields()   
            for fld in fields.toList():
                newcmb.addItem(fld.name())
            self.ui.tblAttributeCode.setCellWidget(row,col,newcmb)
            
    @pyqtSlot()
    def on_btnLoad_clicked(self):
        f, __ = QFileDialog.getOpenFileName(self,
                                        'Load Simulation Control File:',
                                        os.getcwd(),
                                        '*.gsc')
        if f == '':
            return
        
        os.chdir(os.path.dirname(str(f)))
        cfile = ControlFile.ControlFile()
        result = cfile.ReadFile(f)
        if result:
            QMessageBox.critical(self, 'Control File Creator', 'Error Reading File.')
            return
        self.ui.tbxModelDirectory.setText(cfile.ModelDirectory)
        index = self.ui.cmbBaseLayer.findText(cfile.BaseLayer)
        if index < 0:
            QMessageBox.critical(self, 'Control File Creator', 'Base Layer Not Found.')
            return
        else:
            self.ui.cmbBaseLayer.setCurrentIndex(index)
        for key in sorted(cfile.TemplateInput.keys()):
            self.ui.tblTemplateInput.setItem(key,0,QTableWidgetItem(cfile.TemplateInput[key][0]))
            self.ui.tblTemplateInput.setItem(key,1,QTableWidgetItem(cfile.TemplateInput[key][1]))
        bprovider = self.blayer.dataProvider()
        fields = bprovider.fields()
        for key in sorted(cfile.AttributeCode.keys()):
            newcmb = QComboBox()
            for fld in fields.toList():
                newcmb.addItem(fld.name())
            index = newcmb.findText(cfile.AttributeCode[key][0])
            newcmb.setCurrentIndex(index)
            if index < 0:
                QMessageBox.critical(self, 'Control File Creator', 'Attribute Not Found.')
                return
            else:
                self.ui.tblAttributeCode.setCellWidget(key,0,newcmb)
                self.ui.tblAttributeCode.setItem(key,1,QTableWidgetItem(cfile.AttributeCode[key][1]))
        for key in sorted(cfile.InstructionOutput.keys()):
            self.ui.tblInstructionOutput.setItem(key,0,QTableWidgetItem(cfile.InstructionOutput[key][0]))
            self.ui.tblInstructionOutput.setItem(key,1,QTableWidgetItem(cfile.InstructionOutput[key][1]))
        for key in sorted(cfile.AttributeType.keys()):
            self.ui.tblAttributeType.setItem(key,0,QTableWidgetItem(cfile.AttributeType[key][0]))
            self.ui.tblAttributeType.setItem(key,1,QTableWidgetItem(cfile.AttributeType[key][1]))
        self.ui.tbxCommandLine.setText(cfile.CommandLine)
                   
    @pyqtSlot()
    def on_btnSave_clicked(self):
        f, __ = QFileDialog.getSaveFileName(self,
                                        'Save Simulation Control File:',
                                        os.getcwd(),
                                        '*.gsc')
        if f == '':
            return
        
        os.chdir(os.path.dirname(str(f)))
        cfile = ControlFile.ControlFile()
        cfile.ModelDirectory = self.ui.tbxModelDirectory.text()
        cfile.BaseLayer = self.ui.cmbBaseLayer.currentText()
        for i in range(self.ui.tblTemplateInput.rowCount()):
            col1 = self.ui.tblTemplateInput.item(i,0)
            col2 = self.ui.tblTemplateInput.item(i,1)
            if col1 and col2:
                col1 = str(self.ui.tblTemplateInput.item(i,0).text())
                col2 = str(self.ui.tblTemplateInput.item(i,1).text())
                cfile.TemplateInput.update({i : [col1,col2]})
        for i in range(self.ui.tblAttributeCode.rowCount()):
            col1 = self.ui.tblAttributeCode.item(i,0) or self.ui.tblAttributeCode.cellWidget(i,0)
            col2 = self.ui.tblAttributeCode.item(i,1)
            if col1 and col2:
                try:
                    col1 = str(self.ui.tblAttributeCode.cellWidget(i,0).currentText())    
                except:
                    col1 = str(self.ui.tblAttributeCode.item(i,0).text())
                col2 = str(self.ui.tblAttributeCode.item(i,1).text())
                cfile.AttributeCode.update({i : [col1,col2]})
        for i in range(self.ui.tblInstructionOutput.rowCount()):
            col1 = self.ui.tblInstructionOutput.item(i,0)
            col2 = self.ui.tblInstructionOutput.item(i,1)
            if col1 and col2:
                col1 = str(self.ui.tblInstructionOutput.item(i,0).text())
                col2 = str(self.ui.tblInstructionOutput.item(i,1).text())
                cfile.InstructionOutput.update({i : [col1,col2]})
        for i in range(self.ui.tblAttributeType.rowCount()):
            col1 = self.ui.tblAttributeType.item(i,0)
            col2 = self.ui.tblAttributeType.item(i,1)
            if col1 and col2:
                col1 = str(self.ui.tblAttributeType.item(i,0).text())
                col2 = str(self.ui.tblAttributeType.item(i,1).text())
                cfile.AttributeType.update({i : [col1,col2]})
        cfile.CommandLine = self.ui.tbxCommandLine.text()
        cfile.WriteFile(f)
                
    @pyqtSlot()
    def on_btnExit_clicked(self):
        self.close()
