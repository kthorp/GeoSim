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
from qgis.PyQt.QtCore import QFileInfo, Qt, QVariant
from qgis.PyQt.QtWidgets import QDialog, QFileDialog, QApplication, QMessageBox 
from qgis.core import QgsMapLayer, QgsMapLayerRegistry, QgsFeature, QgsVectorLayer
from qgis.core import QgsField, QgsPoint, QgsRectangle, QgsGeometry, QgsVectorFileWriter
from .Ui_Raster2VectorDlg import Ui_Raster2VectorDlg
import os
# create the dialog for Raster2VectorDlg
class Raster2VectorDlg(QDialog):
    def __init__(self, iface): 
        QDialog.__init__(self) 
        # Set up the user interface from Designer. 
        self.ui = Ui_Raster2VectorDlg()
        self.ui.setupUi(self)
        self.iface = iface
        self.mc = iface.mapCanvas() 
        self.layers = self.mc.layers() #Only returns visible (active) layers
        
        #Set up process layer combo box with all raster layers
        for i in self.layers:
            if i.type() == QgsMapLayer.RasterLayer:
                self.ui.cmbProcessLayer.addItem(i.name(), i.id())
        index = self.ui.cmbProcessLayer.currentIndex()
        self.on_cmbProcessLayer_activated(index)
        
    @pyqtSignature("on_cmbProcessLayer_activated(int)")
    def on_cmbProcessLayer_activated(self, index):
        self.ui.ProgressBar.setValue(0)
        if self.ui.cmbProcessLayer.count() > 0:
            pid = self.ui.cmbProcessLayer.itemData(index)
            self.player = QgsMapLayerRegistry.instance().mapLayer(str(pid))

    @pyqtSignature("on_btnBrowse_clicked()")
    def on_btnBrowse_clicked(self):
        if self.ui.cmbProcessLayer.count() > 0:            
            path = QFileInfo(self.player.source()).absolutePath()
        else:
            return             
            
        ofile, __ = QFileDialog.getSaveFileName(self,
                                           'Specify Output Shapefile:',
                                           path,
                                           '*.shp') 
        
        if ofile != '':
            self.outfile = ofile
            self.ui.tbxOutput.setText(self.outfile)
        
    @pyqtSignature("on_tbxOutput_textEdited(QString)")
    def on_tbxOutput_textEdited(self):
        if os.path.exists(self.ui.tbxOutput.text()):
            ofile = os.path.basename(str(self.ui.tbxOutput.text())) 
            QApplication.beep()
            res = QMessageBox.question(self,
                                       'Confirm Save As',
                                       ofile + ' already exists\n' +
                                       'Do you want to replace it?',
                                       QMessageBox.Yes,
                                       QMessageBox.No)
            if res == QMessageBox.Yes:
                self.outfile = self.ui.tbxOutput.text()
            else:
                self.ui.tbxOutput.setText(self.outfile)

    @pyqtSignature("on_btnRun_clicked()")
    def on_btnRun_clicked(self):
                
        if self.ui.cmbProcessLayer.count() <= 0:
            return
        if self.ui.tbxOutput.text() == '':
            QMessageBox.critical(self,'Raster to Vector Converter',
                                 'Please specify output shapefile.')
            return
        
        self.setCursor(Qt.WaitCursor)
            
        #Get raster properties
        numX = self.player.width()
        numY = self.player.height()
        pixsizeX = self.player.rasterUnitsPerPixelX()
        pixsizeY = self.player.rasterUnitsPerPixelY()
        extents = self.player.extent()
        LLX = extents.xMinimum()
        LLY = extents.yMinimum()
        URX = extents.xMaximum()
        URY = extents.yMaximum()
        rprovider = self.player.dataProvider()
            
        if LLX > URX or LLY > URY:
            self.setCursor(Qt.ArrowCursor)
            QMessageBox.critical(self,'Raster to Vector Converter',
                                 'Unexpected image extents.')
            return
        
        #Create vector layer of pixel polygons or points at pixel centers
        #Assumes image extents are given as the LL coordinate of LL pixel
        #and UR coordinate of UR pixel.
        pfeat = QgsFeature()
        crsid = str(self.player.crs().authid())              
        if self.ui.rbPoints.isChecked():        
            pvlayer = QgsVectorLayer("Point?crs="+crsid, "templayer", "memory")
        elif self.ui.rbPolygons.isChecked():
            pvlayer = QgsVectorLayer("Polygon?crs="+crsid, "templayer", "memory")
        fields = [QgsField("ID", QVariant.Int)]
        for i in range(self.player.bandCount()):
            bandname = self.player.bandName(i+1)          
            fields.append(QgsField(bandname, QVariant.Double))
        pprovider = pvlayer.dataProvider()
        pprovider.addAttributes(fields)
        pvlayer.startEditing()
        count = 0
        attr = []
        totpix = float(numX*numY)
        for y in range(numY):
            for x in range(numX):       
                newpt = QgsPoint(LLX+x*pixsizeX+pixsizeX/2.0,
                                 LLY+y*pixsizeY+pixsizeY/2.0)
                data = rprovider.identify(newpt, 1).results()
                if self.ui.rbPoints.isChecked():
                    pfeat.setGeometry(QgsGeometry.fromPoint(newpt))                
                elif self.ui.rbPolygons.isChecked():
                    newrect = QgsRectangle(LLX+x*pixsizeX,
                                           LLY+y*pixsizeY,
                                           LLX+x*pixsizeX+pixsizeX,
                                           LLY+y*pixsizeY+pixsizeY)
                    pfeat.setGeometry(QgsGeometry.fromRect(newrect))
                attr = list(data.values())
                attr.insert(0,count)
                pfeat.setAttributes(attr) 
                result = pvlayer.addFeature(pfeat)
                if not result:
                    self.setCursor(Qt.ArrowCursor)
                    QMessageBox.critical(self,'Raster to Vector Converter',
                                         'Processing error 2.')
                    return        
                del newpt
                if self.ui.rbPolygons.isChecked():
                    del newrect
                count+=1
                self.ui.ProgressBar.setValue(float(count)/totpix * 100.0)
                QApplication.processEvents()  
        pvlayer.commitChanges()
        pvlayer.updateExtents()
        
        #Write the output shapefile
        if os.path.exists(self.outfile):
            QgsVectorFileWriter.deleteShapeFile(self.outfile)
        result = QgsVectorFileWriter.writeAsVectorFormat(pvlayer, 
                                                         self.outfile, 
                                                         'utf-8', 
                                                         self.player.crs())
        if result != QgsVectorFileWriter.NoError:
            QMessageBox.critical(self,'Raster to Vector Converter',
                              'Error creating shapefile.')
        else: #Ask to add shapfile to map
            name = QFileInfo(self.outfile).completeBaseName()
            result = QMessageBox.question(self,'Raster to Vector Converter',
                                          'Add shapefile to map?',
                                          QMessageBox.Yes,
                                          QMessageBox.No)
            if result == QMessageBox.Yes:
                self.iface.addVectorLayer(self.outfile, name, 'ogr')
                
        self.setCursor(Qt.ArrowCursor)
        self.close()
                 
    @pyqtSignature("on_btnExit_clicked()")
    def on_btnExit_clicked(self):
        self.close() 