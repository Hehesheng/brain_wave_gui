#!/usr/bin/env python3
# -*- coding=utf-8 -*-

# ==============================
# @File   {main.py}
# @Date   Created on 2019/09/28
# @Author Hehesheng
# ==============================

# %%
from Combobox import ComboBox
import parameters
import onenet
from ConfigWidget import ConfigTabsWidget
from NormalView import NormalView
from AdvanceView import AdvanceView
# from NN import NN
from PyQt5.QtWidgets import (QApplication, QCheckBox, QDesktopWidget,
                             QGraphicsScene, QGridLayout, QRadioButton,
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


class MainWindow(QMainWindow):
    skin = 1
    isConfigTabsShow = False
    isServiceStart = False

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
        # self.frameLayout.addStretch()

        self.resize(1200, 600)
        self.moveToCenter()
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

    def onOnenetStartButtonPushed(self):
        title = self.configTabs.onenetDeviceIdComboBox.currentText()
        if hasattr(self, "nn") is not True:
            return
        if self.nn.isReady() is not True:
            return
        if self.configTabs.onenetModeCheckBox.isChecked() == True:
            index = self.viewTabs.addTab(
                AdvanceView(self, id=title), title)
        else:
            index = self.viewTabs.addTab(
                NormalView(self, id=title), title)
        self.viewTabs.setCurrentIndex(index)

    def onCloseRequested(self, index):
        self.viewTabs.removeTab(index)

    def initMainLayout(self):
        self.configTabs = ConfigTabsWidget(self)
        self.viewTabs = QTabWidget()
        self.viewTabs.setTabsClosable(True)
        self.viewTabs.tabCloseRequested.connect(self.onCloseRequested)

        self.mainLayout.addWidget(self.configTabs, 1)
        self.mainLayout.addWidget(self.viewTabs, 3)
        self.mainLayout.addStretch()

    # move the app to center
    def moveToCenter(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initTools(self):
        self.startBackgroundInit()
        self.startBackgroundServices()

    def startBackgroundInit(self):
        # 初始化
        task = threading.Thread(target=self.initNNThread)
        task.setDaemon(True)
        task.start()

    def startBackgroundServices(self):
        # 后台更新服务
        self.isServiceStart = True
        task = threading.Thread(target=self.backgroundNetworkService)
        task.setDaemon(True)
        task.start()

    def initNNThread(self):
        from NN import NN
        # 必须导入，原始数据
        self.trainx = np.load('./NN/TGAM/TGAM_trainx.npy')
        self.trainy = np.load('./NN/TGAM/TGAM_trainy.npy') - 1  # 标签从零开始
        self.testx = np.load('./NN/TGAM/TGAM_testx.npy')
        self.testy = np.load('./NN/TGAM/TGAM_testy.npy') - 1
        # 初始模型训练 导入原始数据
        self.nn = NN(self.trainx, self.trainy, self.testx, self.testy)

    # 后台网络服务程序 定时更新
    def backgroundNetworkService(self):
        logger.debug("Network update thread start.")
        while self.isServiceStart == True:
            currentWidget = self.viewTabs.currentWidget()
            if currentWidget is not None:
                pack = currentWidget.target()
                if pack != None:
                    currentWidget.update(pack)
            time.sleep(0.3)

        logger.debug("Network update thread exit.")

    def initEvents(self):
        self.skinButton.clicked.connect(self.skinChange)
        self.settingsButton.clicked.connect(self.settingsButtonPush)

    def settingsButtonPush(self):
        if self.isConfigTabsShow == True:
            self.isConfigTabsShow = False
            self.configTabs.hide()
        else:
            self.isConfigTabsShow = True
            self.configTabs.show()

    def skinChange(self):
        if self.skin == 1:  # light
            file = open(self.DataPath + '/assets/qss/style-dark.qss', "r")
            self.skin = 2
        else:  # elif self.skin == 2: # dark
            file = open(self.DataPath + '/assets/qss/style.qss', "r")
            self.skin = 1
        self.app.setStyleSheet(file.read().replace("$DataPath", self.DataPath))

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
