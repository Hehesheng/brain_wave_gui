#!/usr/bin/env python3
# -*- coding=utf-8 -*-

# ==============================
# @File   {main.py}
# @Date   Created on 2019/09/28
# @Author Hehesheng
# ==============================

# %%
from TgamPlot import MyPlot
from Combobox import ComboBox
import parameters
import onenet
from Figure_Canvas import Figure_Canvas
# from NN import NN
from PyQt5.QtWidgets import (QApplication, QCheckBox, QDesktopWidget,
                             QGraphicsScene, QGridLayout,
                             QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QMainWindow, QMessageBox, QPushButton,
                             QTextEdit, QToolTip, QTabWidget,
                             QVBoxLayout, QWidget, QGraphicsView, QStackedLayout)
from PyQt5.QtGui import QFont, QIcon, QPixmap, QTextCursor, QPalette
from PyQt5.QtCore import Qt, pyqtSignal
import numpy as np
import ctypes
import logging
import os
import socket
import sys
import threading
import time

logging.basicConfig(level=logging.INFO,
                    format="[%(filename)s:%(lineno)s]-%(funcName)20s()]:%(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# %%
class MainWindow(QMainWindow):
    skin = 1
    __isSettinsShow = False

    def __init__(self, app):
        super().__init__()
        self.app = app
        pathDirList = sys.argv[0].replace("\\", "/").split("/")
        pathDirList.pop()
        self.DataPath = os.path.abspath("/".join(str(i) for i in pathDirList))
        if not os.path.exists(self.DataPath):
            pathDirList.pop()
            self.DataPath = os.path.abspath(
                "/".join(str(i) for i in pathDirList))
        self.DataPath = (self.DataPath).replace("\\", "/")
        self.initWindow()
        self.initWidgets()
        self.initTools()
        self.initEvents()

    def initWindow(self):
         # set font
        QToolTip.setFont(QFont('SansSerif', 10))
        # main layout
        self.frameWidget = QWidget()
        self.setCentralWidget(self.frameWidget)
        self.frameLayout = QVBoxLayout()
        self.frameWidget.setLayout(self.frameLayout)
        # 整体界面
        self.menuBarLayout = QHBoxLayout()
        self.mainLayout = QHBoxLayout()
        self.frameLayout.addLayout(self.menuBarLayout)
        self.frameLayout.addLayout(self.mainLayout)
        self.frameLayout.addStretch()

        self.resize(800, 600)
        self.MoveToCenter()
        self.setWindowTitle(parameters.strTitle)

        self.statusBarStauts = QLabel()
        self.statusBarStauts.setMinimumWidth(80)
        self.statusBarStauts.setText(
            "<font color=%s>%s</font>" % (parameters.strStatuBarColor, parameters.strStatuBarInit))
        self.statusBar().addWidget(self.statusBarStauts)

        if sys.platform == "win32":
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                "gui_template")
        self.show()

    def initWidgets(self):
        self.initMenuBarLayout()
        self.initMainLayout()

    def initMenuBarLayout(self):
        self.settingsButton = QPushButton()
        self.skinButton = QPushButton()

        self.settingsButton.setProperty("class", "settingsItem")
        self.skinButton.setProperty("class", "skinItem")

        self.settingsButton.setObjectName("menuItem")
        self.skinButton.setObjectName("menuItem")

        self.menuBarLayout.addWidget(self.settingsButton)
        self.menuBarLayout.addWidget(self.skinButton)
        self.menuBarLayout.addStretch()

    def initMainLayout(self):
        self.initSettingsLayout()
        self.mainLayout.addStretch(1)

    def initSettingsLayout(self):
        self.settingsTabs = QTabWidget()
        self.settingsTabs.setAutoFillBackground(True)

        self.onenetTab = QWidget()
        self.networkTab = QWidget()
        self.emotionTab = QWidget()

        self.settingsTabs.addTab(self.onenetTab, "OneNET")
        self.settingsTabs.addTab(self.networkTab, "NetWork")
        self.settingsTabs.addTab(self.emotionTab, "Emotion")

        self.mainLayout.addWidget(self.settingsTabs)
        self.settingsTabs.hide()
        # OneNET Layout
        # NetWork Layout
        # Emotion Layout

    def initViewLayout(self):
        pass

    def initTools(self):
        pass

    def initEvents(self):
        self.skinButton.clicked.connect(self.skinChange)
        self.settingsButton.clicked.connect(self.settingsButtonPush)

    def settingsButtonPush(self):
        if self.__isSettinsShow == True:
            self.__isSettinsShow = False
            self.settingsTabs.hide()
        else:
            self.__isSettinsShow = True
            self.settingsTabs.show()

    def skinChange(self):
        if self.skin == 1:  # light
            file = open(self.DataPath + '/assets/qss/style-dark.qss', "r")
            self.skin = 2
        else:  # elif self.skin == 2: # dark
            file = open(self.DataPath + '/assets/qss/style.qss', "r")
            self.skin = 1
        self.app.setStyleSheet(file.read().replace("$DataPath", self.DataPath))

    # move the app to center
    def MoveToCenter(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # get ip
    def get_host_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        except Exception as e:
            logger.warning(e)
            ip = parameters.strSocketDefaultAddress
        finally:
            s.close()

        return ip

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Sure To Quit?',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.isStart = False
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow(app)
    logger.debug("data path:"+mainWindow.DataPath)

    if(mainWindow.skin == 1):  # light skin
        file = open(mainWindow.DataPath+'/assets/qss/style.qss', "r")
    else:  # elif mainWindow.skin == 2: # dark skin
        file = open(mainWindow.DataPath + '/assets/qss/style-dark.qss', "r")

    qss = file.read().replace("$DataPath", mainWindow.DataPath)
    app.setStyleSheet(qss)
    sys.exit(app.exec_())
