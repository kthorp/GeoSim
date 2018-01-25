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
from PyQt4.QtCore import pyqtSignature
from qgis.PyQt.QtWidgets import QDialog, QFileDialog, QComboBox, QMessageBox, QTableWidgetItem
from qgis.core import QgsMapLayer, QGis, QgsMapLayerRegistry
from .Ui_OptimizationFileDlg import Ui_OptimizationFileDlg

from . import OptimizationFile
import os

# create the dialog for ControlFileDlg
class OptimizationFileDlg(QDialog):
    def __init__(self, iface): 
        QDialog.__init__(self) 
        # Set up the user interface from Designer. 
        self.ui = Ui_OptimizationFileDlg()
        self.ui.setupUi(self)
        self.iface = iface
        self.mc = iface.mapCanvas() 
        self.layers = self.mc.layers() #Only returns visible (active) layers
        
        for i in self.layers:
            if i.type() == QgsMapLayer.VectorLayer:
                if i.geometryType() == QGis.Polygon:
                    self.ui.cmbBaseLayer.addItem(i.name(), i.id())
        bindex = self.ui.cmbBaseLayer.currentIndex()
        self.on_cmbBaseLayer_activated(bindex)
        
        self.ui.btnBrowse.setFocus()
                    
    @pyqtSignature("on_btnBrowse_clicked()")
    def on_btnBrowse_clicked(self):    
        f, __ = QFileDialog.getOpenFileName(self,
                                        'Specify Simulation Control File:',
                                        os.getcwd(),
                                        '*.gsc') 
        
        if f != '':
            self.ui.tbxControlFile.setText(f)
            os.chdir(os.path.dirname(str(f)))
   
    @pyqtSignature("on_cmbBaseLayer_activated(int)")
    def on_cmbBaseLayer_activated(self, index):
        if self.ui.cmbBaseLayer.count() > 0:
            bid = self.ui.cmbBaseLayer.itemData(index)
            self.blayer = QgsMapLayerRegistry.instance().mapLayer(str(bid))
            
    @pyqtSignature("on_tblOptAttributes_cellDoubleClicked(int,int)")
    def on_tblOptAttributes_cellDoubleClicked(self, row, col):
        if self.ui.cmbBaseLayer.count() > 0 and col == 0:
            newcmb = QComboBox()
            bprovider = self.blayer.dataProvider()
            fields = bprovider.fields()   
            for fld in fields.toList():
                newcmb.addItem(fld.name())
            self.ui.tblOptAttributes.setCellWidget(row,col,newcmb)
    
    @pyqtSignature("on_tblObjAttributes_cellDoubleClicked(int,int)")
    def on_tblObjAttributes_cellDoubleClicked(self, row, col):
        if self.ui.cmbBaseLayer.count() > 0 and col <= 1:
            newcmb = QComboBox()
            bprovider = self.blayer.dataProvider()
            fields = bprovider.fields()   
            for fld in fields.toList():
                newcmb.addItem(fld.name())
            self.ui.tblObjAttributes.setCellWidget(row,col,newcmb)
            
    @pyqtSignature("on_btnLoad_clicked()")
    def on_btnLoad_clicked(self):
        f, __ = QFileDialog.getOpenFileName(self,
                                        'Load Optimization Control File:',
                                        os.getcwd(),
                                        '*.gso')
        if f == '':
            return
        
        os.chdir(os.path.dirname(str(f)))
        ofile = OptimizationFile.OptimizationFile()
        result = ofile.ReadFile(f)
        if result:
            QMessageBox.critical(self, 'Optimization File Creator', 'Error Reading File.')
            return
        self.ui.tbxControlFile.setText(ofile.ControlFile)
        index = self.ui.cmbBaseLayer.findText(ofile.BaseLayer)
        if index < 0:
            QMessageBox.critical(self, 'Optimization File Creator', 'Base Layer Not Found.')
            return
        else:
            self.ui.cmbBaseLayer.setCurrentIndex(index)
        bprovider = self.blayer.dataProvider()
        fields = bprovider.fields()
        for key in sorted(ofile.OptAttributes.keys()):
            newcmb = QComboBox()
            for fld in fields.toList():
                newcmb.addItem(fld.name())
            index = newcmb.findText(ofile.OptAttributes[key][0])
            newcmb.setCurrentIndex(index)
            if index < 0:
                QMessageBox.critical(self, 'Optimization File Creator', 'Attribute Not Found.')
                return
            else:
                self.ui.tblOptAttributes.setCellWidget(key,0,newcmb)
                self.ui.tblOptAttributes.setItem(key,1,QTableWidgetItem(ofile.OptAttributes[key][1]))
                self.ui.tblOptAttributes.setItem(key,2,QTableWidgetItem(ofile.OptAttributes[key][2]))
                self.ui.tblOptAttributes.setItem(key,3,QTableWidgetItem(ofile.OptAttributes[key][3]))
                self.ui.tblOptAttributes.setItem(key,4,QTableWidgetItem(ofile.OptAttributes[key][4]))
        for key in sorted(ofile.ObjAttributes.keys()):
            for i in [0,1]:
                newcmb = QComboBox()
                for fld in fields.toList():
                    newcmb.addItem(fld.name())
                index = newcmb.findText(ofile.ObjAttributes[key][i])
                newcmb.setCurrentIndex(index)
                if index < 0:
                    QMessageBox.critical(self, 'Optimization File Creator', 'Attribute Not Found.')
                    return
                else:
                    self.ui.tblObjAttributes.setCellWidget(key,i,newcmb)
            self.ui.tblObjAttributes.setItem(key,2,QTableWidgetItem(ofile.ObjAttributes[key][2]))
        self.ui.tbxT0.setText(str(ofile.T0))
        self.ui.tbxTf.setText(str(ofile.Tf))
        self.ui.tbxDwell.setText(str(ofile.dwell))
        self.ui.tbxTolerance.setText(str(ofile.feps))
        self.ui.tbxMaxEval.setText(str(ofile.maxeval))
        self.ui.tbxMaxIter.setText(str(ofile.maxiter))
        self.ui.tbxMaxAccept.setText(str(ofile.maxaccept))
        self.ui.tbxm.setText(str(ofile.m))
        self.ui.tbxn.setText(str(ofile.n))
        self.ui.tbxQuench.setText(str(ofile.quench))
        self.ui.tbxBoltzmann.setText(str(ofile.boltzmann))
                   
    @pyqtSignature("on_btnSave_clicked()")
    def on_btnSave_clicked(self):
        f, __ = QFileDialog.getSaveFileName(self,
                                        'Save Optimization Control File:',
                                        os.getcwd(),
                                        '*.gso')
        if f == '':
            return
        
        os.chdir(os.path.dirname(str(f)))
        ofile = OptimizationFile.OptimizationFile()
        ofile.ControlFile = self.ui.tbxControlFile.text()
        ofile.BaseLayer = self.ui.cmbBaseLayer.currentText()
        for i in range(self.ui.tblOptAttributes.rowCount()):
            col1 = self.ui.tblOptAttributes.item(i,0) or self.ui.tblOptAttributes.cellWidget(i,0)
            col2 = self.ui.tblOptAttributes.item(i,1)
            col3 = self.ui.tblOptAttributes.item(i,2)
            col4 = self.ui.tblOptAttributes.item(i,3)
            col5 = self.ui.tblOptAttributes.item(i,4)
            if col1 and col2 and col3 and col4 and col5:
                try:
                    col1 = str(self.ui.tblOptAttributes.cellWidget(i,0).currentText())    
                except:
                    col1 = str(self.ui.tblOptAttributes.item(i,0).text())
                col2 = str(self.ui.tblOptAttributes.item(i,1).text())
                col3 = str(self.ui.tblOptAttributes.item(i,2).text())
                col4 = str(self.ui.tblOptAttributes.item(i,3).text())
                col5 = str(self.ui.tblOptAttributes.item(i,4).text())
                ofile.OptAttributes.update({i : [col1,col2,col3,col4,col5]})
        for i in range(self.ui.tblObjAttributes.rowCount()):
            col1 = self.ui.tblObjAttributes.item(i,0) or self.ui.tblObjAttributes.cellWidget(i,0)
            col2 = self.ui.tblObjAttributes.item(i,1) or self.ui.tblObjAttributes.cellWidget(i,1)
            if col1 and col2:
                try:
                    col1 = str(self.ui.tblObjAttributes.cellWidget(i,0).currentText())
                except:
                    col1 = str(self.ui.tblObjAttributes.item(i,0).text())
                try:
                    col2 = str(self.ui.tblObjAttributes.cellWidget(i,1).currentText())
                except:
                    col2 = str(self.ui.tblObjAttributes.item(i,1).text())
                col3 = str(self.ui.tblObjAttributes.item(i,2).text())
                ofile.ObjAttributes.update({i : [col1,col2,col3]})
                
        ofile.T0 = self.ui.tbxT0.text()
        ofile.Tf = self.ui.tbxTf.text()
        ofile.dwell = self.ui.tbxDwell.text()
        ofile.feps = self.ui.tbxTolerance.text()
        ofile.maxeval = self.ui.tbxMaxEval.text()
        ofile.maxiter = self.ui.tbxMaxIter.text()
        ofile.maxaccept = self.ui.tbxMaxAccept.text()
        ofile.m = self.ui.tbxm.text()
        ofile.n = self.ui.tbxn.text()
        ofile.quench = self.ui.tbxQuench.text()
        ofile.boltzmann = self.ui.tbxBoltzmann.text()  
        ofile.WriteFile(f)
                
    @pyqtSignature("on_btnExit_clicked()")
    def on_btnExit_clicked(self):
        self.close()
