# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_SimControllerDlg.ui'
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

class Ui_SimControllerDlg(object):
    def setupUi(self, SimControllerDlg):
        SimControllerDlg.setObjectName(_fromUtf8("SimControllerDlg"))
        SimControllerDlg.resize(531, 471)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SimControllerDlg.sizePolicy().hasHeightForWidth())
        SimControllerDlg.setSizePolicy(sizePolicy)
        SimControllerDlg.setMinimumSize(QtCore.QSize(531, 471))
        SimControllerDlg.setMaximumSize(QtCore.QSize(531, 471))
        self.horizontalLayoutWidget_2 = QtGui.QWidget(SimControllerDlg)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 70, 511, 41))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.ProgressBar = QtGui.QProgressBar(self.horizontalLayoutWidget_2)
        self.ProgressBar.setObjectName(_fromUtf8("ProgressBar"))
        self.horizontalLayout_3.addWidget(self.ProgressBar)
        self.cbxOnlySelected = QtGui.QCheckBox(self.horizontalLayoutWidget_2)
        self.cbxOnlySelected.setObjectName(_fromUtf8("cbxOnlySelected"))
        self.horizontalLayout_3.addWidget(self.cbxOnlySelected)
        self.btnRun = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.btnRun.setObjectName(_fromUtf8("btnRun"))
        self.horizontalLayout_3.addWidget(self.btnRun)
        self.verticalLayoutWidget_3 = QtGui.QWidget(SimControllerDlg)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(10, 10, 511, 51))
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
        self.textBrowser = QtGui.QTextBrowser(SimControllerDlg)
        self.textBrowser.setGeometry(QtCore.QRect(10, 120, 511, 311))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Consolas"))
        font.setPointSize(8)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.btnExit = QtGui.QPushButton(SimControllerDlg)
        self.btnExit.setGeometry(QtCore.QRect(447, 440, 75, 23))
        self.btnExit.setObjectName(_fromUtf8("btnExit"))

        self.retranslateUi(SimControllerDlg)
        QtCore.QMetaObject.connectSlotsByName(SimControllerDlg)

    def retranslateUi(self, SimControllerDlg):
        SimControllerDlg.setWindowTitle(QtGui.QApplication.translate("SimControllerDlg", "Simulation Controller", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxOnlySelected.setText(QtGui.QApplication.translate("SimControllerDlg", "Selected features only", None, QtGui.QApplication.UnicodeUTF8))
        self.btnRun.setText(QtGui.QApplication.translate("SimControllerDlg", "Run", None, QtGui.QApplication.UnicodeUTF8))
        self.Label3.setText(QtGui.QApplication.translate("SimControllerDlg", "Specify simulation control file:", None, QtGui.QApplication.UnicodeUTF8))
        self.tbxFile.setToolTip(QtGui.QApplication.translate("SimControllerDlg", "Give the filepath and filename of the output shapefile", None, QtGui.QApplication.UnicodeUTF8))
        self.btnBrowse.setToolTip(QtGui.QApplication.translate("SimControllerDlg", "Gives dialog box for selecting output filepath and filename.", None, QtGui.QApplication.UnicodeUTF8))
        self.btnBrowse.setText(QtGui.QApplication.translate("SimControllerDlg", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.btnExit.setText(QtGui.QApplication.translate("SimControllerDlg", "Exit", None, QtGui.QApplication.UnicodeUTF8))

