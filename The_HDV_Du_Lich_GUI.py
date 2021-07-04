# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'The_HDV_Du_Lich.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Tool_The_HDV_Du_Lich(object):
    def setupUi(self, Tool_The_HDV_Du_Lich):
        Tool_The_HDV_Du_Lich.setObjectName("Tool_The_HDV_Du_Lich")
        Tool_The_HDV_Du_Lich.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(Tool_The_HDV_Du_Lich)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_2.addWidget(self.pushButton_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout.addWidget(self.comboBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setMinimumSize(QtCore.QSize(141, 91))
        self.label_2.setStyleSheet("background-color: rgb(245, 121, 0);")
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.label_show = QtWidgets.QLabel(self.centralwidget)
        self.label_show.setMinimumSize(QtCore.QSize(481, 361))
        self.label_show.setStyleSheet("background-color: rgb(115, 210, 22);")
        self.label_show.setObjectName("label_show")
        self.verticalLayout_3.addWidget(self.label_show)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        Tool_The_HDV_Du_Lich.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Tool_The_HDV_Du_Lich)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        Tool_The_HDV_Du_Lich.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Tool_The_HDV_Du_Lich)
        self.statusbar.setObjectName("statusbar")
        Tool_The_HDV_Du_Lich.setStatusBar(self.statusbar)

        self.retranslateUi(Tool_The_HDV_Du_Lich)
        QtCore.QMetaObject.connectSlotsByName(Tool_The_HDV_Du_Lich)

    def retranslateUi(self, Tool_The_HDV_Du_Lich):
        _translate = QtCore.QCoreApplication.translate
        Tool_The_HDV_Du_Lich.setWindowTitle(_translate("Tool_The_HDV_Du_Lich", "MainWindow"))
        self.pushButton_3.setText(_translate("Tool_The_HDV_Du_Lich", "Vẽ khung thẻ"))
        self.label_3.setText(_translate("Tool_The_HDV_Du_Lich", "Chọn thẻ"))
        self.label_2.setText(_translate("Tool_The_HDV_Du_Lich", "image_the"))
        self.pushButton_2.setText(_translate("Tool_The_HDV_Du_Lich", "Back"))
        self.pushButton.setText(_translate("Tool_The_HDV_Du_Lich", "Next"))
        self.label_show.setText(_translate("Tool_The_HDV_Du_Lich", "Image_Show"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Tool_The_HDV_Du_Lich = QtWidgets.QMainWindow()
    ui = Ui_Tool_The_HDV_Du_Lich()
    ui.setupUi(Tool_The_HDV_Du_Lich)
    Tool_The_HDV_Du_Lich.show()
    sys.exit(app.exec_())

