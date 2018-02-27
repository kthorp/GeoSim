# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_SimControllerDlg.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SimControllerDlg(object):
    def setupUi(self, SimControllerDlg):
        SimControllerDlg.setObjectName("SimControllerDlg")
        SimControllerDlg.resize(531, 471)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SimControllerDlg.sizePolicy().hasHeightForWidth())
        SimControllerDlg.setSizePolicy(sizePolicy)
        SimControllerDlg.setMinimumSize(QtCore.QSize(531, 471))
        SimControllerDlg.setMaximumSize(QtCore.QSize(531, 471))
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(SimControllerDlg)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 70, 511, 41))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.ProgressBar = QtWidgets.QProgressBar(self.horizontalLayoutWidget_2)
        self.ProgressBar.setObjectName("ProgressBar")
        self.horizontalLayout_3.addWidget(self.ProgressBar)
        self.cbxOnlySelected = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.cbxOnlySelected.setObjectName("cbxOnlySelected")
        self.horizontalLayout_3.addWidget(self.cbxOnlySelected)
        self.btnRun = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.btnRun.setObjectName("btnRun")
        self.horizontalLayout_3.addWidget(self.btnRun)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(SimControllerDlg)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(10, 10, 511, 51))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.Label3 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.Label3.setObjectName("Label3")
        self.verticalLayout_3.addWidget(self.Label3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tbxFile = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        self.tbxFile.setObjectName("tbxFile")
        self.horizontalLayout_2.addWidget(self.tbxFile)
        self.btnBrowse = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.btnBrowse.setObjectName("btnBrowse")
        self.horizontalLayout_2.addWidget(self.btnBrowse)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.textBrowser = QtWidgets.QTextBrowser(SimControllerDlg)
        self.textBrowser.setGeometry(QtCore.QRect(10, 120, 511, 311))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(8)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("textBrowser")
        self.btnExit = QtWidgets.QPushButton(SimControllerDlg)
        self.btnExit.setGeometry(QtCore.QRect(447, 440, 75, 23))
        self.btnExit.setObjectName("btnExit")

        self.retranslateUi(SimControllerDlg)
        QtCore.QMetaObject.connectSlotsByName(SimControllerDlg)

    def retranslateUi(self, SimControllerDlg):
        _translate = QtCore.QCoreApplication.translate
        SimControllerDlg.setWindowTitle(_translate("SimControllerDlg", "Simulation Controller"))
        self.cbxOnlySelected.setText(_translate("SimControllerDlg", "Selected features only"))
        self.btnRun.setText(_translate("SimControllerDlg", "Run"))
        self.Label3.setText(_translate("SimControllerDlg", "Specify simulation control file:"))
        self.tbxFile.setToolTip(_translate("SimControllerDlg", "Give the filepath and filename of the output shapefile"))
        self.btnBrowse.setToolTip(_translate("SimControllerDlg", "Gives dialog box for selecting output filepath and filename."))
        self.btnBrowse.setText(_translate("SimControllerDlg", "Browse"))
        self.btnExit.setText(_translate("SimControllerDlg", "Exit"))

