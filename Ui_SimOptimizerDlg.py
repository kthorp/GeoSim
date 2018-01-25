# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_SimOptimizerDlg.ui'
#
# Created: Mon Nov 04 09:34:05 2013
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from builtins import object
from qgis.PyQt import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SimOptimizerDlg(object):
    def setupUi(self, SimOptimizerDlg):
        SimOptimizerDlg.setObjectName(_fromUtf8("SimOptimizerDlg"))
        SimOptimizerDlg.resize(561, 471)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SimOptimizerDlg.sizePolicy().hasHeightForWidth())
        SimOptimizerDlg.setSizePolicy(sizePolicy)
        SimOptimizerDlg.setMinimumSize(QtCore.QSize(561, 471))
        SimOptimizerDlg.setMaximumSize(QtCore.QSize(561, 471))
        self.horizontalLayoutWidget_2 = QtGui.QWidget(SimOptimizerDlg)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 70, 541, 44))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.ProgressBar = QtGui.QProgressBar(self.horizontalLayoutWidget_2)
        self.ProgressBar.setObjectName(_fromUtf8("ProgressBar"))
        self.horizontalLayout_3.addWidget(self.ProgressBar)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.cbxOnlySelected = QtGui.QCheckBox(self.horizontalLayoutWidget_2)
        self.cbxOnlySelected.setObjectName(_fromUtf8("cbxOnlySelected"))
        self.verticalLayout.addWidget(self.cbxOnlySelected)
        self.cbxDoGroup = QtGui.QCheckBox(self.horizontalLayoutWidget_2)
        self.cbxDoGroup.setObjectName(_fromUtf8("cbxDoGroup"))
        self.verticalLayout.addWidget(self.cbxDoGroup)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.btnRun = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.btnRun.setObjectName(_fromUtf8("btnRun"))
        self.horizontalLayout_3.addWidget(self.btnRun)
        self.verticalLayoutWidget_3 = QtGui.QWidget(SimOptimizerDlg)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(10, 10, 541, 51))
        self.verticalLayoutWidget_3.setObjectName(_fromUtf8("verticalLayoutWidget_3"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.Label3 = QtGui.QLabel(self.verticalLayoutWidget_3)
        self.Label3.setObjectName(_fromUtf8("Label3"))
        self.verticalLayout_3.addWidget(self.Label3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.tbxFile = QtGui.QLineEdit(self.verticalLayoutWidget_3)
        self.tbxFile.setObjectName(_fromUtf8("tbxFile"))
        self.horizontalLayout_2.addWidget(self.tbxFile)
        self.btnBrowse = QtGui.QPushButton(self.verticalLayoutWidget_3)
        self.btnBrowse.setObjectName(_fromUtf8("btnBrowse"))
        self.horizontalLayout_2.addWidget(self.btnBrowse)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.textSimulation = QtGui.QTextBrowser(SimOptimizerDlg)
        self.textSimulation.setGeometry(QtCore.QRect(10, 120, 541, 151))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Consolas"))
        font.setPointSize(8)
        self.textSimulation.setFont(font)
        self.textSimulation.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.textSimulation.setObjectName(_fromUtf8("textSimulation"))
        self.btnExit = QtGui.QPushButton(SimOptimizerDlg)
        self.btnExit.setGeometry(QtCore.QRect(480, 440, 71, 23))
        self.btnExit.setObjectName(_fromUtf8("btnExit"))
        self.textOptimization = QtGui.QTextBrowser(SimOptimizerDlg)
        self.textOptimization.setGeometry(QtCore.QRect(10, 280, 541, 151))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Consolas"))
        font.setPointSize(8)
        self.textOptimization.setFont(font)
        self.textOptimization.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.textOptimization.setObjectName(_fromUtf8("textOptimization"))

        self.retranslateUi(SimOptimizerDlg)
        QtCore.QMetaObject.connectSlotsByName(SimOptimizerDlg)

    def retranslateUi(self, SimOptimizerDlg):
        SimOptimizerDlg.setWindowTitle(QtGui.QApplication.translate("SimOptimizerDlg", "Simulation Optimizer", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxOnlySelected.setText(QtGui.QApplication.translate("SimOptimizerDlg", "Selected features only", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxDoGroup.setText(QtGui.QApplication.translate("SimOptimizerDlg", "Group selected features", None, QtGui.QApplication.UnicodeUTF8))
        self.btnRun.setText(QtGui.QApplication.translate("SimOptimizerDlg", "Run", None, QtGui.QApplication.UnicodeUTF8))
        self.Label3.setText(QtGui.QApplication.translate("SimOptimizerDlg", "Specify simulation optimization file:", None, QtGui.QApplication.UnicodeUTF8))
        self.tbxFile.setToolTip(QtGui.QApplication.translate("SimOptimizerDlg", "Give the filepath and filename of the output shapefile", None, QtGui.QApplication.UnicodeUTF8))
        self.btnBrowse.setToolTip(QtGui.QApplication.translate("SimOptimizerDlg", "Gives dialog box for selecting output filepath and filename.", None, QtGui.QApplication.UnicodeUTF8))
        self.btnBrowse.setText(QtGui.QApplication.translate("SimOptimizerDlg", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.btnExit.setText(QtGui.QApplication.translate("SimOptimizerDlg", "Exit", None, QtGui.QApplication.UnicodeUTF8))

