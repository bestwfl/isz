# -*- coding:utf8 -*-
import sys
import PyQt4
from PyQt4.QtCore import Qt, QRect, QSize
from PyQt4.QtGui import QWidget, QIcon, QApplication, QPushButton, QMessageBox, QPalette, QColor, QLabel, QPainter, \
    QPixmap, QPen, QLineEdit, QTextEdit, QGridLayout, QComboBox


class labelBtn1(QLabel):
    """
    自定义图片按钮类
    """
    def __init__(self, ID):
        super(labelBtn1, self).__init__()
        self.setMouseTracking(True)
        self.ID = ID

    def mouseReleaseEvent(self, event):  # 注:
        # 鼠标点击事件
        self.parent().btnHandle(self.ID)

class labelBtn2(QLabel):
    def __init__(self):
        super(labelBtn2, self).__init__()
        self.setMouseTracking(True)
    #拖拽
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.parent().frameGeometry().topLeft()
            event.accept()
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.parent().move(event.globalPos()- self.dragPosition)
            event.accept()

class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def btnHandle(self, ID):
        if ID == 2:
            self.close()
        elif ID == 1:
            self.hide()
            self.showMinimized()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        # painter.setRenderHint(QPainter.Antialiasing)
        # # painter.setPen(Qt.NoPen)
        # painter.drawPixmap(0, 0, 59, 51, QPixmap("C:\Users\user\Desktop\logo.png"))
        rect = QRect(0, 0, 799, 599)
        pen = QPen(QColor(30, 30, 30, 255 * 0.8), 1)#定义画笔
        painter.setPen(pen)
        painter.drawLine(580, 0, 580, 600)  #划线
        painter.drawLine(0, 60, 580, 60)  # 划线
        painter.drawRoundedRect(rect, 10, 10)
        painter.end()

    def initUI(self):

        user = QLabel(u'用户',self)
        pwd = QLabel(u'密码',self)
        userEdit = QLineEdit(self)
        pwdEdit = QLineEdit(self)
        loginB = QPushButton(u'登 录',self)
        userEdit.move(40,37)
        userEdit.setText('18815286582')
        user.move(10,40)
        pwd.move(180,40)
        pwdEdit.move(210,37)
        pwdEdit.setText('ceshi123456')
        loginB.move(500,35)
        print userEdit.size()
        userEdit.setBaseSize(QSize(100,40))

        entrustLab = QLabel(self)
        entrustLab.setText(u'委托')
        entrustLab.setFont()
        entrustLab.move(10, 65)
        rentTypeCombo = QComboBox(self)
        rentTypeCombo.addItem(u'整租')
        rentTypeCombo.addItem(u'合租')
        rentTypeCombo.move(10,90)
        apartmentTypeCombo = QComboBox(self)
        apartmentTypeCombo.addItem(u'品牌')
        apartmentTypeCombo.addItem(u'品质')
        apartmentTypeCombo.move(65,90)


        # 头部
        self.titlelab = labelBtn2()
        self.titlelab.setParent(self)
        self.titlelab.setGeometry(-1, -1, 748, 36)
        self.titlelab.setPixmap(QPixmap("C:\Users\user\Desktop\myimg\ltitle.png"))
        # logo
        self.loglab = QLabel()
        self.loglab.setParent(self)
        self.loglab.setGeometry(2, -2, 36, 36)
        self.loglab.setPixmap(QPixmap("C:\Users\user\Desktop\myimg\mlogo.png"))
        # 关闭图标
        self.closelab = labelBtn1(2)
        self.closelab.setParent(self)
        self.closelab.setGeometry(774, -2, 27, 36)
        self.closelab.setPixmap(QPixmap("C:\Users\user\Desktop\myimg\closeb.png"))
        self.closelab.setToolTip(u"关闭")
        # 最小化
        self.minlab = labelBtn1(1)
        self.minlab.setParent(self)
        self.minlab.setGeometry(746, -2, 28, 36)
        self.minlab.setPixmap(QPixmap("C:\Users\user\Desktop\myimg\minb.png"))
        self.minlab.setToolTip(u"最小化")

        palette1 = QPalette()
        palette1.setColor(self.backgroundRole(), QColor(255, 255, 255))  # 设置背景颜色
        self.setPalette(palette1)
        self.setGeometry(300, 200, 800, 600)
        self.setWindowTitle(u'爱上租')
        self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏边框
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


