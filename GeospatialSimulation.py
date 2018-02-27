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
# Import the PyQt and QGIS libraries
from builtins import object
from qgis.PyQt.QtCore import QObject, QSettings
from qgis.PyQt.QtWidgets import QAction, QMessageBox
from qgis.PyQt.QtGui import QIcon
# Initialize Qt resources from file resources.py
import os
import sys
from . import resources
# Import the code for the dialogs
from .GeoprocessorDlg import GeoprocessorDlg
from .Raster2VectorDlg import Raster2VectorDlg
from .ControlFileDlg import ControlFileDlg
from .SimControllerDlg import SimControllerDlg
from .OptimizationFileDlg import OptimizationFileDlg
from .SimOptimizerDlg import SimOptimizerDlg

class GeospatialSimulation(object): 

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'geospatialsimulation_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

    def initGui(self):  
        # Create action that will start plugin configuration
        icon = QIcon(":/plugins/geospatialsimulation/icon.png")
        self.ras2vec = QAction(icon,u"Raster to Vector Converter", self.iface.mainWindow())
        self.geoprocess = QAction(icon,u"Vector Geoprocessor", self.iface.mainWindow())
        self.controlfile = QAction(icon,u"Control File Creator", self.iface.mainWindow())
        self.simulate = QAction(icon,u"Simulation Controller", self.iface.mainWindow())
        self.optfile = QAction(icon, u"Optimization File Creator", self.iface.mainWindow())
        self.optimize = QAction(icon, u"Simulation Optimizer", self.iface.mainWindow())
        self.helpme = QAction(icon, u"Help", self.iface.mainWindow())
        
        # connect the action to a method
        self.ras2vec.triggered.connect(self.Raster2Vector)
        self.geoprocess.triggered.connect(self.Geoprocess)
        self.controlfile.triggered.connect(self.MakeControlFile)
        self.simulate.triggered.connect(self.Simulate)
        self.optfile.triggered.connect(self.MakeOptimizationFile)
        self.optimize.triggered.connect(self.Optimize)
        self.helpme.triggered.connect(self.Help)
         
        # Add toolbar button and menu item        
        self.iface.addPluginToMenu(u"&Geospatial Simulation", self.ras2vec)
        self.iface.addPluginToMenu(u"&Geospatial Simulation", self.geoprocess)
        self.iface.addPluginToMenu(u"&Geospatial Simulation", self.controlfile)
        self.iface.addPluginToMenu(u"&Geospatial Simulation", self.simulate)
        self.iface.addPluginToMenu(u"&Geospatial Simulation", self.optfile)
        self.iface.addPluginToMenu(u"&Geospatial Simulation", self.optimize)
        self.iface.addPluginToMenu(u"&Geospatial Simulation", self.helpme)
        

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&Geospatial Simulation", self.ras2vec)
        self.iface.removePluginMenu(u"&Geospatial Simulation", self.geoprocess)
        self.iface.removePluginMenu(u"&Geospatial Simulation", self.controlfile)
        self.iface.removePluginMenu(u"&Geospatial Simulation", self.simulate)
        self.iface.removePluginMenu(u"&Geospatial Simulation", self.optfile)
        self.iface.removePluginMenu(u"&Geospatial Simulation", self.optimize)
        self.iface.removePluginMenu(u"&Geospatial Simulation", self.helpme)
        
    # run methods that perform all the real work
    def Geoprocess(self): 
        # create and show the dialog 
        dlg = GeoprocessorDlg(self.iface) 
        # show the dialog
        #dlg.show() #Modeless dialog
        dlg.exec_() #Modal dialog
        
    def Raster2Vector(self):
        dlg = Raster2VectorDlg(self.iface)
        dlg.exec_()
        
    def MakeControlFile(self):
        dlg = ControlFileDlg(self.iface)
        dlg.exec_()
    
    def Simulate(self):
        dlg = SimControllerDlg(self.iface)
        dlg.exec_()
        
    def MakeOptimizationFile(self):
        dlg = OptimizationFileDlg(self.iface)
        dlg.exec_()
    
    def Optimize(self):
        dlg = SimOptimizerDlg(self.iface)
        dlg.exec_()
        
    def Help(self):
        path = os.path.dirname(sys.modules[__name__].__file__)
        if sys.platform[:-1] == 'linux':
            os.system(path+"//HTP Geoprocessor README.pdf")
        elif sys.platform == 'darwin':
            os.system(path+"//HTP Geoprocessor README.pdf")
        elif sys.platform == 'win32' or 'win64':
            os.startfile(path+"\\HTP Geoprocessor README.pdf")
        else:
            QMessageBox.critical(self.iface.mainWindow(),'Help','Error opening document. Look in plug-in install directory for PDF.')
