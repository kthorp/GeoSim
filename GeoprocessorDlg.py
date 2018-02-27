"""
/***************************************************************************
Name			 	 : Geospatial Simulation
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
from builtins import next
from builtins import str
from qgis.PyQt.QtCore import Qt, pyqtSlot
from qgis.PyQt.QtWidgets import QDialog, QMessageBox, QListWidgetItem, QApplication
from qgis.core import QgsMapLayer, QgsProject, QgsField, QgsSpatialIndex, QgsFeatureRequest, QgsWkbTypes
from .Ui_GeoprocessorDlg import Ui_GeoprocessorDlg
# create the dialog for GeoprocessorDlg
class GeoprocessorDlg(QDialog):
    def __init__(self, iface): 
        QDialog.__init__(self) 
        # Set up the user interface from Designer. 
        self.ui = Ui_GeoprocessorDlg()
        self.ui.setupUi(self)
        self.iface = iface
        self.mc = iface.mapCanvas() 
        self.layers = self.mc.layers() #Only returns visible (active) layers

        #Setup GUI combo boxes for processing actions
        self.ui.cmbObjective.addItem('Find mean value of points within polygons')   #0
        self.ui.cmbObjective.addItem('Find median value of points within polygons') #1
        self.ui.cmbObjective.addItem('Find maximum value of points within polygons')#2
        self.ui.cmbObjective.addItem('Find minimum value of points within polygons')#3
        self.ui.cmbObjective.addItem('Find mean value of polygons within polygons') #4
        self.ui.cmbObjective.addItem('Find maximum area polygon within polygons')   #5
        self.ui.cmbObjective.addItem('Add attributes of polygons to points')        #6
        index = self.ui.cmbObjective.currentIndex()
        self.on_cmbObjective_activated(index)

    @pyqtSlot(int)
    def on_cmbObjective_activated(self, index):
        self.ui.ProgressBar.setValue(0)
        self.ui.cmbBaseLayer.clear()
        self.ui.cmbProcessLayer.clear()
        self.oindex = index
        if index in [0,1,2,3]: #Point in polygon processing
            for i in self.layers:
                if i.type() == QgsMapLayer.VectorLayer:
                    if i.geometryType() == QgsWkbTypes.PolygonGeometry:
                        self.ui.cmbBaseLayer.addItem(i.name(), i.id())
                    if i.geometryType() == QgsWkbTypes.PointGeometry:
                        self.ui.cmbProcessLayer.addItem(i.name(), i.id())
        elif index in [4,5]: #Polygon in polygon processing
            for i in self.layers:
                if i.type() == QgsMapLayer.VectorLayer:
                    if i.geometryType() == QgsWkbTypes.PolygonGeometry:
                        self.ui.cmbBaseLayer.addItem(i.name(), i.id())
                        self.ui.cmbProcessLayer.addItem(i.name(), i.id())
        elif index in [6]: #Polygon attribute to points
            for i in self.layers:
                if i.type() == QgsMapLayer.VectorLayer:
                    if i.geometryType() == QgsWkbTypes.PointGeometry:
                        self.ui.cmbBaseLayer.addItem(i.name(), i.id())
                    if i.geometryType() == QgsWkbTypes.PolygonGeometry:
                        self.ui.cmbProcessLayer.addItem(i.name(), i.id())                                
        else:
            QMessageBox.critical(self, 'Vector Geoprocessor', 'Unknown Objective')
                          
        bindex = self.ui.cmbBaseLayer.currentIndex()
        self.on_cmbBaseLayer_activated(bindex)
        
        pindex = self.ui.cmbProcessLayer.currentIndex()    
        self.on_cmbProcessLayer_activated(pindex)  
            
    @pyqtSlot(int)
    def on_cmbBaseLayer_activated(self, index):
        self.ui.ProgressBar.setValue(0)
        if self.ui.cmbBaseLayer.count() > 0:
            bid = self.ui.cmbBaseLayer.itemData(index)
            self.blayer = QgsProject.instance().mapLayer(str(bid))
    
    @pyqtSlot(int)
    def on_cmbProcessLayer_activated(self, index):            
        if self.ui.cmbProcessLayer.count() > 0:
            pid = self.ui.cmbProcessLayer.itemData(index)
            self.player = QgsProject.instance().mapLayer(str(pid))
        else:
            return
        self.ui.listFields.clear()
        self.ui.ProgressBar.setValue(0)
        pprovider = self.player.dataProvider()
        fields = pprovider.fields()   
        for fld in fields.toList():
            if self.oindex in [0,1,2,3,4] and fld.typeName() != 'String': #Numeric fields
                self.ui.listFields.addItem(QListWidgetItem(fld.name()))
            elif self.oindex in [5,6] and fld.typeName() == 'String': #String fields
                self.ui.listFields.addItem(QListWidgetItem(fld.name()))
                
    @pyqtSlot()
    def on_btnRun_clicked(self):
        
        #Check for combo and list box selections
        if self.ui.cmbBaseLayer.count() < 1 or self.ui.cmbProcessLayer.count() < 1:
            QMessageBox.critical(self, 'Vector Geoprocessor', 'Invalid layer selection.')
            return
        if len(self.ui.listFields.selectedItems()) < 1:
            QMessageBox.critical(self, 'Vector Geoprocessor', 'Invalid field selection.')
            return            
      
        #Initializations
        self.ui.ProgressBar.setValue(0)
        self.setCursor(Qt.WaitCursor)
        data = []
            
        #Add new attributes to base layer
        bprovider = self.blayer.dataProvider()
        pprovider = self.player.dataProvider()
        pfields = pprovider.fields()
        for item in self.ui.listFields.selectedItems():
            fname = item.text()
            for fld in pfields.toList():
                if fname == fld.name():                                               
                    newfield = QgsField()
                    newfield.setName(fld.name())
                    newfield.setType(fld.type())
                    newfield.setTypeName(fld.typeName())
                    newfield.setLength(fld.length())
                    newfield.setPrecision(fld.precision())
                    newfield.setComment(fld.comment())
                    bprovider.addAttributes([newfield])            

        #Create a spatial index for faster processing
        spindex = QgsSpatialIndex()
        for pfeat in pprovider.getFeatures():
            spindex.insertFeature(pfeat)
        
        #Find the intersection of process layer features with base layer
        #To increase speed, intersect with a bounding box rectangle first
        #Then further process within the geometric shape
        #Add requested processed information to base layer                
        featreq = QgsFeatureRequest()
        bfields = bprovider.fields()
        ddic = {}
        len1 = len(self.ui.listFields.selectedItems())
        len2 = len(bfields)
        b1 = 0
        b2 = bprovider.featureCount()
        attr={}
        for bfeat in bprovider.getFeatures():
            b1+=1
            attr.clear()
            bgeom = bfeat.geometry()                                          
            intersect = spindex.intersects(bgeom.boundingBox())
            data[:] = []
            for fid in intersect:               
                pfeat = next(self.player.getFeatures(featreq.setFilterFid(fid)))
                if pfeat.geometry().intersects(bgeom) == False:
                    data.append(fid)           
            for fid in data:        
                intersect.pop(intersect.index(fid))
                              
            count = 0
            for item in self.ui.listFields.selectedItems():
                pfindx = pprovider.fieldNameIndex(item.text())
                if pfindx < 0:
                    self.setCursor(Qt.ArrowCursor)
                    QMessageBox.critical(self, 'Vector Geoprocessor', 'Processing error.')
                    return
                data[:] = []
                for fid in intersect:
                    pfeat = next(self.player.getFeatures(featreq.setFilterFid(fid)))
                    if self.oindex in [0,1,2,3,4]:
                        data.append(float(pfeat.attribute(item.text())))
                    elif self.oindex in [5,6]:
                        data.append(str(pfeat.attribute(item.text())))
                if len(data) == 0:
                    value = None
                elif self.oindex == 0: #Find mean value of points within polygons
                    value = sum(data)/float(len(data))
                elif self.oindex == 1: #Find median value of points within polygons
                    data = sorted(data)
                    lendata = len(data)
                    if lendata % 2:
                        value = data[(lendata+1)/2-1]
                    else:
                        d1 = data[lendata/2-1]
                        d2 = data[lendata/2]
                        value = (d1 + d2)/2.0
                elif self.oindex == 2: #Find maximum value of points within polygons
                    value = max(data)
                elif self.oindex == 3: #Find minimum value of points within polygons
                    value = min(data)
                elif self.oindex == 4: #Find mean value (area-weighted) of polygons within polygons
                    value = 0.0
                    totalarea = 0.0
                    for fid in intersect:
                        pfeat = next(self.player.getFeatures(featreq.setFilterFid(fid)))
                        pgeom = pfeat.geometry()
                        isect = bgeom.intersection(pgeom)
                        parea = isect.area()
                        value+=(float(pfeat.attribute(item.text())*parea))
                        totalarea+=parea
                    value = value / totalarea
                elif self.oindex == 5: #Find largest area polygon within polygons
                    data = list(set(data))  #Get unique items in data                          
                    ddic.clear()
                    for i in data:
                        ddic.update({i : 0.0})
                    for fid in intersect:
                        pfeat = next(self.player.getFeatures(featreq.setFilterFid(fid)))
                        pgeom = pfeat.geometry()
                        isect = bgeom.intersection(pgeom)
                        parea = isect.area()
                        key = str(pfeat.attribute(item.text()))
                        parea = parea + ddic[key]
                        ddic.update({key : parea})
                    parea = -1
                    for key in list(ddic.keys()):
                        if ddic[key] > parea:
                            parea = ddic[key]
                            value = key
                elif self.oindex == 6: #Add polygon attribute to points
                    if len(data) != 1:
                        QMessageBox.warning(self, 'Vector Geoprocessor',
                                            'Point intersects more than one polygon.')
                    value = data[0]
                
                attr.update({(len2-len1+count):value})
                count+=1
            result = bprovider.changeAttributeValues({bfeat.id():attr})
            if not result:
                QMessageBox.critical(self, 'Vector Geoprocessor', 'Could not change attribute value.')
                return           
            self.ui.ProgressBar.setValue(float(b1)/float(b2) * 100.0)
            QApplication.processEvents()

        self.setCursor(Qt.ArrowCursor)
            
    @pyqtSlot()
    def on_btnExit_clicked(self):
        self.close()
    
