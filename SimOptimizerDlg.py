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

from builtins import next
from builtins import str
from qgis.PyQt.QtCore import Qt, pyqtSlot
from qgis.PyQt.QtWidgets import QDialog, QFileDialog, QMessageBox, QApplication
from qgis.core import QgsFeature, QgsFeatureRequest
from .Ui_SimOptimizerDlg import Ui_SimOptimizerDlg
from . import OptimizationFile
from . import SimControllerDlg
from . import anneal
import os
import math

class SimOptimizerDlg(QDialog):
    
    def __init__(self, iface):
        QDialog.__init__(self) 
        # Set up the user interface from Designer. 
        self.ui = Ui_SimOptimizerDlg()
        self.ui.setupUi(self)
        self.iface = iface
        self.mc = iface.mapCanvas() 
        self.layers = self.mc.layers() #Only returns visible (active) layers
        
        self.ui.textSimulation.document().setMaximumBlockCount(500)
        self.ui.textOptimization.document().setMaximumBlockCount(500)
        
        self.ofilename = ''        
        
    @pyqtSlot()
    def on_btnBrowse_clicked(self):            
        f, __ = QFileDialog.getOpenFileName(self,
                                        'Specify Simulation Optimization File:',
                                        os.getcwd(),
                                        '*.gso') 
        
        if f != '':
            self.ofilename = f
            self.ui.tbxFile.setText(self.ofilename)
            os.chdir(os.path.dirname(str(f)))
        
    @pyqtSlot()
    def on_tbxFile_textEdited(self):
        self.ofilename = self.ui.tbxFile.text()  
        
    @pyqtSlot()
    def on_btnRun_clicked(self):
        
        #Open optimization file
        if not os.path.exists(self.ofilename):
            QMessageBox.critical(self,'Simulation Optimizer','File does not exist.')
            return
        else:
            self.ofile = OptimizationFile.OptimizationFile()
            ret = self.ofile.ReadFile(self.ofilename)
            if ret:
                QMessageBox.critical(self,'Simulation Optimizer','Error reading file.')
                return
            self.logfile = self.ofilename + '.log'
            f = open(self.logfile, 'w')
            f.close()
                  
        #Get base layer
        flag = 1
        for i in self.layers:
            if i.name() == self.ofile.BaseLayer:
                self.blayer = i
                self.bprovider = self.blayer.dataProvider()
                flag = 0
                break
        if flag:
            QMessageBox.critical(self,'Simulation Optimizer','Base layer not found.')
            return
        
        #Initializations
        b1 = 0
        self.ui.ProgressBar.setValue(0)
        self.setCursor(Qt.WaitCursor)
        featreq = QgsFeatureRequest()
        if self.ui.cbxOnlySelected.isChecked():
            self.selectedIDs = self.blayer.selectedFeaturesIds()
        else:
            self.selectedIDs = []
            for bfeat in self.bprovider.getFeatures():
                self.selectedIDs.append(bfeat.id())
        self.selectedIDs.sort()
        b2 = len(self.selectedIDs)
        
        #Set up optimization and run
        x0 = []
        lower = []
        upper = []
        if self.ui.cbxDoGroup.isChecked():           
            for key in sorted(self.ofile.OptAttributes.keys()):
                x0.append(float(self.ofile.OptAttributes[key][1]))
                lower.append(float(self.ofile.OptAttributes[key][2]))
                upper.append(float(self.ofile.OptAttributes[key][3]))
                         
            string = 'Optimizing grouped features\n'
            string += 'Iter Temperature  Eval  Prob  Acc  Dec   BestEval    CurEval  Parameters....'
            f = open(self.logfile, 'a')
            f.write(string + '\n')
            f.close()
            self.ui.textOptimization.append(string)
            opt = Optimize(x0,lower,upper,T0=self.ofile.T0,Tf=self.ofile.Tf,dwell=self.ofile.dwell,
                           feps=self.ofile.feps,maxeval=self.ofile.maxeval,maxiter=self.ofile.maxiter,
                           maxaccept=self.ofile.maxaccept,m=self.ofile.m,n=self.ofile.n,
                           quench=self.ofile.quench,boltzmann=self.ofile.boltzmann)            
            opt.init(self.blayer, self.bprovider, self.selectedIDs, self.ui, self.ofile, self.logfile, self.iface)
            solution = opt.run()
            self.WriteResult(solution)
            self.UpdateGIS(solution, self.selectedIDs)
            self.ui.ProgressBar.setValue(float(b2)/float(b2) * 100.0)
             
        else: #Run optimization for individual features

            for featid in self.selectedIDs:
                b1+=1
                x0[:] = []
                lower[:] = []
                upper[:] = []
                bfeat = next(self.blayer.getFeatures(featreq.setFilterFid(featid)))
                for key in sorted(self.ofile.OptAttributes.keys()):
                    x0.append(float(self.ofile.OptAttributes[key][1]))
                    lower.append(float(self.ofile.OptAttributes[key][2]))
                    upper.append(float(self.ofile.OptAttributes[key][3]))
                  
                string = 'Optimizing feature ID#: %d\n' % featid
                string += 'Iter Temperature  Eval  Prob  Acc  Dec   BestEval    CurEval  Parameters....'
                f = open(self.logfile, 'a')
                f.write(string + '\n')
                f.close()
                self.ui.textOptimization.append(string)
                opt = Optimize(x0,lower,upper,T0=self.ofile.T0,Tf=self.ofile.Tf,dwell=self.ofile.dwell,
                               feps=self.ofile.feps,maxeval=self.ofile.maxeval,maxiter=self.ofile.maxiter,
                               maxaccept=self.ofile.maxaccept,m=self.ofile.m,n=self.ofile.n,
                               quench=self.ofile.quench,boltzmann=self.ofile.boltzmann)
                opt.init(self.blayer, self.bprovider, [bfeat.id()], self.ui, self.ofile, self.logfile, self.iface)
                solution = opt.run()
                self.UpdateGIS(solution, [bfeat.id()])
                self.WriteResult(solution)
                self.ui.ProgressBar.setValue(float(b1)/float(b2) * 100.0)
            
        if self.ui.cbxOnlySelected.isChecked():
            self.blayer.setSelectedFeatures(self.selectedIDs)
        else:
            self.blayer.removeSelection()
                
        self.setCursor(Qt.ArrowCursor)
    
    def WriteResult(self, result):    
        string = '%4d ' % result[0]
        string += '%11.5f ' % result[1]
        string += '%5d ' % result[2]
        string += '%5.3f ' % result[3]
        string += '%4d ' % result[4]
        string += '%4d ' % result[5]
        string += ('%10.4f ' % result[7])
        string += '           '
        for i in result[6]:
            string += '%10.4f ' % i
        string += '\nRMSE: ' + str(result[7]) + '\n' 
        string += result[8]
        
        f = open(self.logfile, 'a')
        f.write(string + '\n\n')
        f.close()
        self.ui.textOptimization.append(string + '\n')
        
    def UpdateGIS(self, solution, bfeatids):
        
        bfeat = QgsFeature()
        featreq = QgsFeatureRequest()
        i=0 
        attr={}
        for featid in bfeatids:
            i+=1
            attr.clear()
            bfeat = next(self.blayer.getFeatures(featreq.setFilterFid(featid)))       
            for key in sorted(self.ofile.OptAttributes.keys()):
                bfindx = self.bprovider.fieldNameIndex(self.ofile.OptAttributes[key][0])
                ftype = str(self.bprovider.fields()[bfindx].typeName())
                if ftype in ['Integer']:
                    value = int(solution[6][key])
                elif ftype in ['Real', 'Double']:
                    value = float(solution[6][key])
                if int(self.ofile.OptAttributes[key][4]) in [0,i]: 
                    attr.update({bfindx:value})                    
            result = self.bprovider.changeAttributeValues({bfeat.id():attr})
            if not result:
                self.setCursor(Qt.ArrowCursor)
                QMessageBox.critical(self, 'Simulation Optimizer', 'Could not change attribute value2.')
                return 
        self.blayer.setSelectedFeatures(bfeatids)
        QApplication.processEvents()
                                       
        #Run simulations
        for featid in bfeatids:
            sim = SimControllerDlg.SimControllerDlg(self.iface)
            sim.cfilename = self.ofile.ControlFile
            sim.ui.cbxOnlySelected.setChecked(1)            
            self.blayer.setSelectedFeatures([featid])            
            sim.on_btnRun_clicked()       
            for line in sim.stdout:
                self.ui.textSimulation.append(line)
            for line in sim.stderr:
                self.ui.textSimulation.append(line)
            sim.on_btnExit_clicked()    
           
    @pyqtSlot()
    def on_btnExit_clicked(self):
        self.close()  
            
class Optimize(anneal.Anneal):        
        
    def init(self, blayer, bprovider, bfeatids, ui, ofile, logfile, iface):
        self.blayer = blayer
        self.bprovider = bprovider
        self.bfeatids = list(bfeatids)
        self.ui = ui
        self.ofile = ofile
        self.logfile = logfile
        self.iface = iface
        self.simout = ''
        self.optout = ''
         
    def evaluate(self):
        
        #Write parameters to GIS
        bfeat = QgsFeature()
        featreq = QgsFeatureRequest()
        i=0
        attr = {}
        for featid in self.bfeatids:
            i+=1
            attr.clear()
            bfeat = next(self.blayer.getFeatures(featreq.setFilterFid(featid)))
            for key in sorted(self.ofile.OptAttributes.keys()):
                bfindx = self.bprovider.fieldNameIndex(self.ofile.OptAttributes[key][0])
                ftype = str(self.bprovider.fields()[bfindx].typeName())
                if ftype in ['Integer']:
                    value = int(self.current.x[key])
                elif ftype in ['Real', 'Double']:
                    value = float(self.current.x[key])
                if int(self.ofile.OptAttributes[key][4]) in [0,i]:                 
                    attr.update({bfindx:value})                                     
            result = self.bprovider.changeAttributeValues({bfeat.id():attr})
            if not result:
                self.setCursor(Qt.ArrowCursor)
                QMessageBox.critical(self, 'Simulation Optimizer', 'Could not change attribute value1.')
                return 
                 
        #Can't get attribute table repainting to work for all conditions.
        self.blayer.setSelectedFeatures(self.bfeatids)
        QApplication.processEvents()
        
        #Run simulations   
        for featid in self.bfeatids:
            sim = SimControllerDlg.SimControllerDlg(self.iface)
            sim.cfilename = self.ofile.ControlFile
            sim.ui.cbxOnlySelected.setChecked(1) 
            self.blayer.setSelectedFeatures([featid])          
            sim.on_btnRun_clicked()       
            for line in sim.stdout:
                self.ui.textSimulation.append(line)
            for line in sim.stderr:
                self.ui.textSimulation.append(line)
            sim.on_btnExit_clicked()
        
        #Calculate error
        sqrerr = []
        for featid in self.bfeatids:
            bfeat = next(self.blayer.getFeatures(featreq.setFilterFid(featid)))
            for key in sorted(self.ofile.ObjAttributes.keys()):
                measured = float(bfeat.attribute(self.ofile.ObjAttributes[key][0]))
                simulated = float(bfeat.attribute(self.ofile.ObjAttributes[key][1]))
                factor = float(self.ofile.ObjAttributes[key][2])
                error = (simulated - measured) * factor
                #error = (simulated - measured) / measured
                #error = (simulated - measured)
                sqrerr.append(error*error)
                
        sumsq = sum(sqrerr) / len(sqrerr)
        rmse = math.sqrt(sumsq) 
                    
        #Output
        string = '%4d ' % self.iterat
        string += '%11.5f ' % self.T
        string += '%5d ' % self.feval
        string += '%5.3f ' % self.p
        string += '%4d ' % self.accepted
        string += '%4d ' % self.declined
        if self.best.cost:
            string += ('%10.4f ' % self.best.cost)
        else:
            string += ('%10.4f ' % rmse)
        string += ('%10.4f ' % rmse)
        for i in self.best.x:
            string += '%10.4f ' % i
        for i in self.current.x:
            string += '%10.4f ' % i
        self.ui.textOptimization.append(string)
        f = open(self.logfile, 'a')
        f.write(string + '\n')
        f.close()
        
        return rmse
    
    def constrain(self):
        pass
