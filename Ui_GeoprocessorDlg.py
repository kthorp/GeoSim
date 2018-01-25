# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_GeoprocessorDlg.ui'
#
# Created: Mon Nov 04 09:34:04 2013
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from builtins import object
from qgis.PyQt import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_GeoprocessorDlg(object):
    def setupUi(self, GeoprocessorDlg):
        GeoprocessorDlg.setObjectName(_fromUtf8("GeoprocessorDlg"))
        GeoprocessorDlg.resize(401, 381)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GeoprocessorDlg.sizePolicy().hasHeightForWidth())
        GeoprocessorDlg.setSizePolicy(sizePolicy)
        GeoprocessorDlg.setMinimumSize(QtCore.QSize(401, 381))
        GeoprocessorDlg.setMaximumSize(QtCore.QSize(401, 381))
        self.verticalLayoutWidget = QtGui.QWidget(GeoprocessorDlg)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 130, 381, 51))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.Label1 = QtGui.QLabel(self.verticalLayoutWidget)
        self.Label1.setMinimumSize(QtCore.QSize(379, 0))
        self.Label1.setObjectName(_fromUtf8("Label1"))
        self.verticalLayout.addWidget(self.Label1)
        self.cmbProcessLayer = QtGui.QComboBox(self.verticalLayoutWidget)
        self.cmbProcessLayer.setObjectName(_fromUtf8("cmbProcessLayer"))
        self.verticalLayout.addWidget(self.cmbProcessLayer)
        self.verticalLayoutWidget_2 = QtGui.QWidget(GeoprocessorDlg)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 70, 381, 51))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.Label2 = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.Label2.setMinimumSize(QtCore.QSize(379, 0))
        self.Label2.setObjectName(_fromUtf8("Label2"))
        self.verticalLayout_2.addWidget(self.Label2)
        self.cmbBaseLayer = QtGui.QComboBox(self.verticalLayoutWidget_2)
        self.cmbBaseLayer.setObjectName(_fromUtf8("cmbBaseLayer"))
        self.verticalLayout_2.addWidget(self.cmbBaseLayer)
        self.horizontalLayoutWidget_2 = QtGui.QWidget(GeoprocessorDlg)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 330, 381, 41))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.ProgressBar = QtGui.QProgressBar(self.horizontalLayoutWidget_2)
        self.ProgressBar.setObjectName(_fromUtf8("ProgressBar"))
        self.horizontalLayout_3.addWidget(self.ProgressBar)
        self.btnRun = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.btnRun.setObjectName(_fromUtf8("btnRun"))
        self.horizontalLayout_3.addWidget(self.btnRun)
        self.btnExit = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.btnExit.setObjectName(_fromUtf8("btnExit"))
        self.horizontalLayout_3.addWidget(self.btnExit)
        self.verticalLayoutWidget_4 = QtGui.QWidget(GeoprocessorDlg)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(10, 190, 381, 131))
        self.verticalLayoutWidget_4.setObjectName(_fromUtf8("verticalLayoutWidget_4"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.Label1_2 = QtGui.QLabel(self.verticalLayoutWidget_4)
        self.Label1_2.setMinimumSize(QtCore.QSize(379, 0))
        self.Label1_2.setObjectName(_fromUtf8("Label1_2"))
        self.verticalLayout_4.addWidget(self.Label1_2)
        self.listFields = QtGui.QListWidget(self.verticalLayoutWidget_4)
        self.listFields.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.listFields.setObjectName(_fromUtf8("listFields"))
        self.verticalLayout_4.addWidget(self.listFields)
        self.verticalLayoutWidget_3 = QtGui.QWidget(GeoprocessorDlg)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(10, 10, 381, 51))
        self.verticalLayoutWidget_3.setObjectName(_fromUtf8("verticalLayoutWidget_3"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.Label3 = QtGui.QLabel(self.verticalLayoutWidget_3)
        self.Label3.setObjectName(_fromUtf8("Label3"))
        self.verticalLayout_3.addWidget(self.Label3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.cmbObjective = QtGui.QComboBox(self.verticalLayoutWidget_3)
        self.cmbObjective.setObjectName(_fromUtf8("cmbObjective"))
        self.horizontalLayout_2.addWidget(self.cmbObjective)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.retranslateUi(GeoprocessorDlg)
        QtCore.QMetaObject.connectSlotsByName(GeoprocessorDlg)

    def retranslateUi(self, GeoprocessorDlg):
        GeoprocessorDlg.setWindowTitle(QtGui.QApplication.translate("GeoprocessorDlg", "Vector Geoprocessor", None, QtGui.QApplication.UnicodeUTF8))
        self.Label1.setText(QtGui.QApplication.translate("GeoprocessorDlg", "Select Layer To Process:", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbProcessLayer.setToolTip(QtGui.QApplication.translate("GeoprocessorDlg", "Select the layer to process.", None, QtGui.QApplication.UnicodeUTF8))
        self.Label2.setText(QtGui.QApplication.translate("GeoprocessorDlg", "Select Base Layer:", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbBaseLayer.setToolTip(QtGui.QApplication.translate("GeoprocessorDlg", "Select the polygon base layer.", None, QtGui.QApplication.UnicodeUTF8))
        self.btnRun.setText(QtGui.QApplication.translate("GeoprocessorDlg", "Run", None, QtGui.QApplication.UnicodeUTF8))
        self.btnExit.setText(QtGui.QApplication.translate("GeoprocessorDlg", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.Label1_2.setText(QtGui.QApplication.translate("GeoprocessorDlg", "Select Data Fields To Process:", None, QtGui.QApplication.UnicodeUTF8))
        self.Label3.setText(QtGui.QApplication.translate("GeoprocessorDlg", "Select Processing Objective:", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbObjective.setToolTip(QtGui.QApplication.translate("GeoprocessorDlg", "Select the processing objective.", None, QtGui.QApplication.UnicodeUTF8))

