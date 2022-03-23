# This Python file uses the following encoding: utf-8
# 该文件是主程序

from PyQt5 import QtWidgets
from window import Ui_Window
from PyQt5.QtWidgets import QFileDialog
import pandas as pd
import cair_al
import cv2

class Server(QtWidgets.QWidget, Ui_Window):
    def __init__(self):
        super(Server, self).__init__()
        self.setupUi(self)
        self.pushButton_3.clicked.connect(self.read_file)
        self.pushButton.clicked.connect(self.process)

    def read_file(self): #选取文件
        filename, filetype =QFileDialog.getOpenFileName(self, "选取文件", "C:/", "Jpg Files(*.jpg)")
        print(filename, filetype)
        self.lineEdit.setText(filename)

    def process(self):
        if self.comboBox.currentText() == "横向":
            which_axis = 'c'
        else:
            which_axis == 'r'
        scale = float(self.lineEdit_2.text())
        in_filename = self.lineEdit.text()
        out_filename = self.lineEdit_3.text()

        img = cv2.imread(in_filename)

        if which_axis == 'r':
            out = cair_al.crop_r(img, scale)
        elif which_axis == 'c':
            out = cair_al.crop_c(img, scale)

        cv2.imwrite(out_filename,out)
        cv2.imshow("output", out)
        cv2.waitKey(0)

if __name__=="__main__":
     import sys
     app=QtWidgets.QApplication(sys.argv)
     ui = Server()
     ui.show()
     sys.exit(app.exec_())
