# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_Raster2VectorDlg.ui'
#
# Created: Mon Nov 04 09:34:03 2013
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Raster2VectorDlg(object):
    def setupUi(self, Raster2VectorDlg):
        Raster2VectorDlg.setObjectName(_fromUtf8("Raster2VectorDlg"))
        Raster2VectorDlg.resize(401, 221)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Raster2VectorDlg.sizePolicy().hasHeightForWidth())
        Raster2VectorDlg.setSizePolicy(sizePolicy)
        Raster2VectorDlg.setMinimumSize(QtCore.QSize(401, 221))
        Raster2VectorDlg.setMaximumSize(QtCore.QSize(401, 221))
        self.verticalLayoutWidget = QtGui.QWidget(Raster2VectorDlg)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 381, 51))
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
        self.horizontalLayoutWidget_2 = QtGui.QWidget(Raster2VectorDlg)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 170, 381, 41))
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
        self.horizontalLayoutWidget = QtGui.QWidget(Raster2VectorDlg)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 70, 381, 31))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.rbPoints = QtGui.QRadioButton(self.horizontalLayoutWidget)
        self.rbPoints.setObjectName(_fromUtf8("rbPoints"))
        self.horizontalLayout.addWidget(self.rbPoints)
        self.rbPolygons = QtGui.QRadioButton(self.horizontalLayoutWidget)
        self.rbPolygons.setChecked(True)
        self.rbPolygons.setObjectName(_fromUtf8("rbPolygons"))
        self.horizontalLayout.addWidget(self.rbPolygons)
        self.verticalLayoutWidget_3 = QtGui.QWidget(Raster2VectorDlg)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(10, 110, 381, 51))
        self.verticalLayoutWidget_3.setObjectName(_fromUtf8("verticalLayoutWidget_3"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.Label3 = QtGui.QLabel(self.verticalLayoutWidget_3)
        self.Label3.setObjectName(_fromUtf8("Label3"))
        self.verticalLayout_3.addWidget(self.Label3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.tbxOutput = QtGui.QLineEdit(self.verticalLayoutWidget_3)
        self.tbxOutput.setObjectName(_fromUtf8("tbxOutput"))
        self.horizontalLayout_2.addWidget(self.tbxOutput)
        self.btnBrowse = QtGui.QPushButton(self.verticalLayoutWidget_3)
        self.btnBrowse.setObjectName(_fromUtf8("btnBrowse"))
        self.horizontalLayout_2.addWidget(self.btnBrowse)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Raster2VectorDlg)
        QtCore.QMetaObject.connectSlotsByName(Raster2VectorDlg)

    def retranslateUi(self, Raster2VectorDlg):
        Raster2VectorDlg.setWindowTitle(QtGui.QApplication.translate("Raster2VectorDlg", "Raster to Vector Converter", None, QtGui.QApplication.UnicodeUTF8))
        self.Label1.setText(QtGui.QApplication.translate("Raster2VectorDlg", "Select Raster Layer To Process:", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbProcessLayer.setToolTip(QtGui.QApplication.translate("Raster2VectorDlg", "Select the layer to process.", None, QtGui.QApplication.UnicodeUTF8))
        self.btnRun.setText(QtGui.QApplication.translate("Raster2VectorDlg", "Run", None, QtGui.QApplication.UnicodeUTF8))
        self.btnExit.setText(QtGui.QApplication.translate("Raster2VectorDlg", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Raster2VectorDlg", "Select Vector Layer Type:            ", None, QtGui.QApplication.UnicodeUTF8))
        self.rbPoints.setText(QtGui.QApplication.translate("Raster2VectorDlg", "Point Layer", None, QtGui.QApplication.UnicodeUTF8))
        self.rbPolygons.setText(QtGui.QApplication.translate("Raster2VectorDlg", "Polygon Layer", None, QtGui.QApplication.UnicodeUTF8))
        self.Label3.setText(QtGui.QApplication.translate("Raster2VectorDlg", "Specify output shapefile:", None, QtGui.QApplication.UnicodeUTF8))
        self.tbxOutput.setToolTip(QtGui.QApplication.translate("Raster2VectorDlg", "Give the filepath and filename of the output shapefile", None, QtGui.QApplication.UnicodeUTF8))
        self.btnBrowse.setToolTip(QtGui.QApplication.translate("Raster2VectorDlg", "Gives dialog box for selecting output filepath and filename.", None, QtGui.QApplication.UnicodeUTF8))
        self.btnBrowse.setText(QtGui.QApplication.translate("Raster2VectorDlg", "Browse", None, QtGui.QApplication.UnicodeUTF8))

