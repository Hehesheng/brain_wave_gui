#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ==============================
# @File   gui.py
# @Date   Created on 2019/07/13
# @Author Hehesheng
# ==============================
#%%
from TgamPlot import MyPlot
from Combobox import ComboBox
import parameters
import onenet
from Figure_Canvas import Figure_Canvas
from NN import NN
from PyQt5.QtWidgets import (QApplication, QCheckBox, QDesktopWidget,
                             QFileDialog, QGraphicsScene, QGridLayout,
                             QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QMainWindow, QMessageBox, QPushButton,
                             QRadioButton, QSplitter, QTextEdit, QToolTip,
                             QVBoxLayout, QWidget, QGraphicsView)
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

import matplotlib
#%%
matplotlib.use("Qt5Agg")  # 声明使用QT5


logging.basicConfig(level=logging.INFO,
                    format="[%(filename)s:%(lineno)s]-%(funcName)20s()]:%(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

#%%
class MainWindow(QMainWindow):
    skin = 1
    DataPath = "./"
    isStart = False
    serverMode = str()
    address = str()
    port = 0
    origin_json = ""

    saved = {"happy": None, "sad": None, "angry": None, "scare": None}

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
        self.initTool()
        self.initEvent()

    def initWindow(self):
        # set font
        QToolTip.setFont(QFont('SansSerif', 10))

        # main layout
        frameWidget = QWidget()
        mainWidget = QSplitter(Qt.Horizontal)
        frameLayout = QVBoxLayout()

        self.settingWidget = QWidget()
        self.settingWidget.setProperty("class", "settingWidget")
        self.receiveSendWidget = QSplitter(Qt.Vertical)

        settingLayout = QVBoxLayout()
        sendReceiveLayout = QVBoxLayout()
        mainLayout = QHBoxLayout()

        self.settingWidget.setLayout(settingLayout)
        self.receiveSendWidget.setLayout(sendReceiveLayout)

        mainLayout.addWidget(self.settingWidget, 6)
        mainLayout.addWidget(self.receiveSendWidget, 6)

        menuLayout = QHBoxLayout()
        mainWidget.setLayout(mainLayout)
        frameLayout.addLayout(menuLayout)
        frameLayout.addWidget(mainWidget)
        frameWidget.setLayout(frameLayout)
        self.setCentralWidget(frameWidget)

        # option layout
        self.settingsButton = QPushButton()
        self.skinButton = QPushButton("")
        # self.waveButton = QPushButton("")
        self.aboutButton = QPushButton()
        self.functionalButton = QPushButton()

        self.settingsButton.setProperty("class", "menuItem1")
        self.skinButton.setProperty("class", "menuItem2")
        self.aboutButton.setProperty("class", "menuItem3")
        self.functionalButton.setProperty("class", "menuItem4")
        # self.waveButton.setProperty("class", "menuItem5")
        self.settingsButton.setObjectName("menuItem")
        self.skinButton.setObjectName("menuItem")
        self.aboutButton.setObjectName("menuItem")
        self.functionalButton.setObjectName("menuItem")
        # self.waveButton.setObjectName("menuItem")

        menuLayout.addWidget(self.settingsButton)
        menuLayout.addWidget(self.skinButton)
        # menuLayout.addWidget(self.waveButton)
        menuLayout.addWidget(self.aboutButton)
        menuLayout.addStretch(0)

        self.graphicView = QGraphicsView()
        self.dr = Figure_Canvas()
        # 第三步，创建一个QGraphicsScene，因为加载的图形（FigureCanvas）不能直接放到graphicview控件中，必须先放到graphicScene，然后再把graphicscene放到graphicview中
        self.graphicScene = QGraphicsScene()
        # 第四步，把图形放到QGraphicsScene中，注意：图形是作为一个QWidget放到QGraphicsScene中的
        self.graphicScene.addWidget(self.dr)
        # 第五步，把QGraphicsScene放入QGraphicsView
        self.graphicView.setScene(self.graphicScene)
        self.graphicView.show()  # 最后，调用show方法呈现图形！Voila!!
        # self.graphicView.setFixedSize(500, 300)

        # widgets receive and send area
        learnResultGroupBox = QGroupBox("Result")
        learnResultLayout = QGridLayout()
        # self.test = QVBoxLayout()
        # self.learnResultLayout.addLayout(self.test)

        self.happyResRadioButton = QRadioButton(parameters.strEmotionHappy)
        self.happyResRadioButton.toggled.connect(
            slot=self.radioButtonBeChanged)
        self.setRadioButtonStyle(self.happyResRadioButton, False)
        self.sadResRadioButton = QRadioButton(parameters.strEmotionSad)
        self.sadResRadioButton.toggled.connect(slot=self.radioButtonBeChanged)
        self.setRadioButtonStyle(self.sadResRadioButton, False)
        self.angryResRadioButton = QRadioButton(parameters.strEmotionAngry)
        self.angryResRadioButton.toggled.connect(
            slot=self.radioButtonBeChanged)
        self.setRadioButtonStyle(self.angryResRadioButton, False)
        self.scareResRadioButton = QRadioButton(parameters.strEmotionScare)
        self.scareResRadioButton.toggled.connect(
            slot=self.radioButtonBeChanged)
        self.setRadioButtonStyle(self.scareResRadioButton, False)

        self.resultText = QTextEdit()
        self.resultText.setReadOnly(True)

        learnResultLayout.addWidget(self.happyResRadioButton, 0, 0)
        learnResultLayout.addWidget(self.sadResRadioButton, 0, 1)
        # learnResultLayout.addWidget(self.relaxResRadioButton, 1, 0)
        # learnResultLayout.addWidget(self.attentionResRadioButton, 1, 1)
        learnResultLayout.addWidget(self.angryResRadioButton, 1, 0)
        learnResultLayout.addWidget(self.scareResRadioButton, 1, 1)
        learnResultLayout.addWidget(self.resultText, 0, 2, 2, 2)
        learnResultGroupBox.setLayout(learnResultLayout)

        sendReceiveLayout.addWidget(self.graphicView, 7)
        sendReceiveLayout.addWidget(learnResultGroupBox, 2)

        # socket settings
        socketSettingsGroupBox = QGroupBox(parameters.strSocketSettings)
        socketSettingsLayout = QGridLayout()

        self.socketModeComboBox = ComboBox()
        self.socketModeComboBox.addItem("OneNET")
        self.socketModeComboBox.addItem("UDP Server")
        self.socketModeComboBox.addItem("TCP Server")
        socketAddressLabel = QLabel(parameters.strSocketAddress)
        self.socketAddressLineEdit = QLineEdit()
        self.socketAddressLineEdit.setText(self.get_host_ip())
        socketPortLabel = QLabel(parameters.strSocketPort)
        self.socketPortLineEdit = QLineEdit()
        self.socketPortLineEdit.setText(parameters.strSocketDefaultPort)
        onenetDeviceIdLabel = QLabel(parameters.strOneNETDeviceId)
        self.onenetDeviceIdComboBox = ComboBox()
        for id in onenet.device_id:
            self.onenetDeviceIdComboBox.addItem(id)
        self.socketStartPushButton = QPushButton(
            parameters.strSocketButtonStart)

        socketSettingsLayout.addWidget(self.socketModeComboBox, 0, 0, 1, 2)
        socketSettingsLayout.addWidget(socketAddressLabel, 1, 0)
        socketSettingsLayout.addWidget(self.socketAddressLineEdit, 1, 1)
        socketSettingsLayout.addWidget(socketPortLabel, 2, 0)
        socketSettingsLayout.addWidget(self.socketPortLineEdit, 2, 1)
        socketSettingsLayout.addWidget(onenetDeviceIdLabel, 3, 0)
        socketSettingsLayout.addWidget(self.onenetDeviceIdComboBox, 3, 1)
        socketSettingsLayout.addWidget(self.socketStartPushButton, 4, 0, 1, 2)

        socketSettingsGroupBox.setLayout(socketSettingsLayout)

        # learning setting
        learnSettingsGroupBox = QGroupBox(parameters.strLearnSettings)
        learnSettingsLayout = QGridLayout()

        self.happyLearnRadioButton = QRadioButton(parameters.strEmotionHappy)
        self.happyLearnRadioButton.setChecked(True)
        self.sadLearnRadioButton = QRadioButton(parameters.strEmotionSad)
        # self.relaxLearnRadioButton = QRadioButton(parameters.strEmotionRelax)
        # self.attentionLearnRadioButton = QRadioButton(
        #     parameters.strEmotionAttention)
        self.angryLearnRadioButton = QRadioButton(parameters.strEmotionAngry)
        self.scareLearnRadioButton = QRadioButton(parameters.strEmotionScare)
        self.learnPushButton = QPushButton(parameters.strLearnButton)

        learnSettingsLayout.addWidget(self.happyLearnRadioButton, 0, 0)
        learnSettingsLayout.addWidget(self.sadLearnRadioButton, 0, 1)
        # learnSettingsLayout.addWidget(self.relaxLearnRadioButton, 1, 0)
        # learnSettingsLayout.addWidget(self.attentionLearnRadioButton, 1, 1)
        learnSettingsLayout.addWidget(self.angryLearnRadioButton, 1, 0)
        learnSettingsLayout.addWidget(self.scareLearnRadioButton, 1, 1)
        learnSettingsLayout.addWidget(self.learnPushButton, 2, 0, 1, 2)
        learnResultGroupBox.setLayout(learnResultLayout)

        learnSettingsGroupBox.setLayout(learnSettingsLayout)

        # algorithm setting 2
        algorithmSettingsGroupBox = QGroupBox(parameters.strAlgorithmText)
        algorithmSettingsLayout = QGridLayout()

        self.algorithmVectorLearnRadioButton = QRadioButton(
            parameters.strAlgorithmVector)
        self.algorithmNNLearnRadioButton = QRadioButton(
            parameters.strAlgorithmNN)
        self.algorithmNNLearnRadioButton.setChecked(True)
        self.realTimeCheckBox = QCheckBox(parameters.strAlgorithmRealTime)
        self.emotionCheckBox = QCheckBox(parameters.strAlgorithmEmotion)
        self.emotionCheckBox.setChecked(True)
        self.analysisPushButton = QPushButton(parameters.strAnalysisButton)

        algorithmSettingsLayout.addWidget(
            self.algorithmVectorLearnRadioButton, 0, 1)
        algorithmSettingsLayout.addWidget(
            self.algorithmNNLearnRadioButton, 0, 0)
        algorithmSettingsLayout.addWidget(self.realTimeCheckBox, 1, 0)
        algorithmSettingsLayout.addWidget(self.emotionCheckBox, 1, 1)
        algorithmSettingsLayout.addWidget(self.analysisPushButton, 2, 0, 1, 2)

        algorithmSettingsGroupBox.setLayout(algorithmSettingsLayout)

        settingLayout.addWidget(socketSettingsGroupBox, 5)
        settingLayout.addWidget(learnSettingsGroupBox, 3)
        settingLayout.addWidget(algorithmSettingsGroupBox, 3)

        # main window
        self.statusBarStauts = QLabel()
        self.statusBarStauts.setMinimumWidth(80)
        self.statusBarStauts.setText(
            "<font color=%s>%s</font>" % (parameters.strStatuBarColor, parameters.strStatuBarInit))
        self.statusBar().addWidget(self.statusBarStauts)

        self.resize(1000, 800)
        self.MoveToCenter()
        self.setWindowTitle(parameters.strTitle)

        if sys.platform == "win32":
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                "gui_template")
        self.show()

    def initNN(self):
        # 必须导入，原始数据
        self.trainx = np.load('./NN/TGAM/TGAM_trainx.npy')
        self.trainy = np.load('./NN/TGAM/TGAM_trainy.npy') - 1  # 标签从零开始
        self.testx = np.load('./NN/TGAM/TGAM_testx.npy')
        self.testy = np.load('./NN/TGAM/TGAM_testy.npy') - 1
        # 初始模型训练
        model = NN(self.trainx, self.trainy, self.testx, self.testy)  # 导入原始数据

        return model

    def initTool(self):
        # 初始化网络
        self.nn = self.initNN()
        # 线程锁
        self.lock = threading.Lock()

    def initEvent(self):
        self.skinButton.clicked.connect(self.skinChange)
        self.socketStartPushButton.clicked.connect(
            self.selectStartOrStopServer)
        self.learnPushButton.clicked.connect(self.learnEmotion)
        self.analysisPushButton.clicked.connect(self.outputAnalysiResult)

    def skinChange(self):
        if self.skin == 1:  # light
            file = open(self.DataPath + '/assets/qss/style-dark.qss', "r")
            self.skin = 2
        else:  # elif self.skin == 2: # dark
            file = open(self.DataPath + '/assets/qss/style.qss', "r")
            self.skin = 1
        self.app.setStyleSheet(file.read().replace("$DataPath", self.DataPath))

    def setRadioButtonStyle(self, radioButton, value):
        if value == True:
            radioButton.setStyleSheet(
                parameters.radioButtonSelected + parameters.radioButtonDefault)
        else:
            radioButton.setStyleSheet(parameters.radioButtonDefault)

    def radioButtonBeChanged(self, value):
        handle = self.sender()
        self.setRadioButtonStyle(handle, value)

    # move the app to center
    def MoveToCenter(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Sure To Quit?',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.isStart = False
            event.accept()
        else:
            event.ignore()

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

    def selectStartOrStopServer(self):
        if self.isStart:
            self.stopServer()
        else:
            self.startServer()

    def startServer(self):
        try:
            self.port = int(self.socketPortLineEdit.text())
        except Exception as e:
            logger.warning(e)
            QMessageBox.warning(self, "WARN", "Please enter a port.")
            return
        self.address = self.socketAddressLineEdit.text()
        if self.address == "":
            QMessageBox.warning(self, "WARN", "Please enter an ip.")
            return
        self.serverMode = self.socketModeComboBox.currentText()

        try:
            print(self.tgam)
            QMessageBox.warning(self, "WARN", "Start Fail.")
            return
        except Exception:
            self.tgam = MyPlot(self.realTimeCheckBox.isChecked())

        self.isStart = True
        if self.serverMode.find("TCP") != -1 or self.serverMode.find("UDP") != -1:
            self.serverThread = threading.Thread(
                target=self.TCPAndUDPServerThread)

        elif self.serverMode.find("OneNET") != -1:
            self.serverThread = threading.Thread(
                target=self.OneNETServerThread)

        self.serverThread.setDaemon(True)
        self.serverThread.start()

        self.socketStartPushButton.setText(parameters.strSocketButtonStop)

    def TCPAndUDPServerThread(self):
        logger.debug("TCP or UDP Running.")

        if self.serverMode.find("TCP") != -1:
            self.sock_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif self.serverMode.find("UDP") != -1:
            self.sock_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_s.bind((self.address, self.port))  # 设置监听端口
        self.sock_s.listen(2)

        self.sock, self.addr = self.sock_s.accept()  # 阻塞函数，等待连接

        while self.isStart:
            self.recv_data = self.sock.recv(1024)
            data_ascii = self.recv_data.decode('ascii')
            self.origin_json = self.origin_json + data_ascii
            try:
                if self.origin_json[-1] == '}':
                    self.tgam.update(self.origin_json)
                    self.origin_json = ""
            except Exception:
                self.stopServer()
                break

        self.sock_s.close()
        logger.debug("Exit")

    def OneNETServerThread(self):
        logger.debug("OneNET Running.")
        self.lock.acquire()
        while self.isStart:
            self.lock.release()
            # 获取 json
            self.origin_json = onenet.get_current_value(
                onenet.get_onenet_stream(parameters.strOnenetTgamName, self.onenetDeviceIdComboBox.currentText()))
            try:
                if self.tgam.update(self.origin_json) != 0:
                    logger.debug("Recv Error.")
                elif self.emotionCheckBox.isChecked():
                    self.dr.plot_bar(self.tgam.tgamPackDict)
                    self.analysisEmotion()
            except Exception as e:
                logger.debug(e)

            self.origin_json = onenet.get_current_value(
                onenet.get_onenet_stream(parameters.strOnenetAd59Name, self.onenetDeviceIdComboBox.currentText()))
            try:
                if self.tgam.update(self.origin_json) != 0:
                    logger.debug("Recv Error.")
            except Exception:
                pass
            time.sleep(0.5)
            self.lock.acquire()
        self.lock.release()

        logger.debug("Exit")

    def stopServer(self):
        self.lock.acquire()
        self.isStart = False
        self.lock.release()
        logger.debug("Stop Push!")
        # 先保证线程退出再开始删除
        while self.serverThread.is_alive():
            time.sleep(0.3)
        while self.tgam.isUpdate():
            time.sleep(0.3)
        try:
            self.dr.plot_bar(self.tgam.tgamPackDict)
        except Exception as e:
            logger.debug(e)
        # self.tgam.close()
        del self.tgam
        self.socketStartPushButton.setText(parameters.strSocketButtonStart)
        logger.debug("tgam close")

    def updateLearnData(self, dst, src):
        try:
            self.saved[dst] = np.array(src)
        except Exception:
            return -1
        return 0

    def learnEmotion(self):
        if self.algorithmVectorLearnRadioButton.isChecked():
            try:
                if self.happyLearnRadioButton.isChecked():
                    self.updateLearnData(
                        "happy", self.dr.bar_wave_data+self.dr.bar_notice_data)

                elif self.sadLearnRadioButton.isChecked():
                    self.updateLearnData(
                        "sad", self.dr.bar_wave_data+self.dr.bar_notice_data)

                elif self.angryLearnRadioButton.isChecked():
                    self.updateLearnData(
                        "angry", self.dr.bar_wave_data+self.dr.bar_notice_data)

                elif self.scareLearnRadioButton.isChecked():
                    self.updateLearnData(
                        "scare", self.dr.bar_wave_data+self.dr.bar_notice_data)

            except Exception:
                pass
        elif self.algorithmNNLearnRadioButton.isChecked():
            if self.happyLearnRadioButton.isChecked():
                tag = 0
            elif self.sadLearnRadioButton.isChecked():
                tag = 1
            elif self.angryLearnRadioButton.isChecked():
                tag = 2
            elif self.scareLearnRadioButton.isChecked():
                tag = 3
            emotion = np.array(self.dr.bar_wave_data+self.dr.bar_notice_data)
            emotion = emotion.reshape((1, 10))
            tag = np.array([tag])
            tag = tag.reshape([1, 1])
            self.nn.finetune(emotion, tag)

    def analysisEmotion(self):
        tmp = np.array(self.dr.bar_wave_data+self.dr.bar_notice_data)

        if self.algorithmVectorLearnRadioButton.isChecked():
            up = 0
            down = 0
            res = {"happy": 0, "sad": 0, "angry": 0, "scare": 0}
            try:
                up = np.sum(self.saved["happy"]*tmp)
                down = np.linalg.norm(self.saved["happy"])*np.linalg.norm(tmp)
                res["happy"] = up/down
            except Exception:
                pass
            try:
                up = np.sum(self.saved["sad"]*tmp)
                down = np.linalg.norm(self.saved["sad"])*np.linalg.norm(tmp)
                res["sad"] = up/down
            except Exception:
                pass
            try:
                up = np.sum(self.saved["angry"]*tmp)
                down = np.linalg.norm(self.saved["angry"])*np.linalg.norm(tmp)
                res["angry"] = up/down
            except Exception:
                pass
            try:
                up = np.sum(self.saved["scare"]*tmp)
                down = np.linalg.norm(self.saved["scare"])*np.linalg.norm(tmp)
                res["scare"] = up/down
            except Exception:
                pass
            emotion = sorted(res.items(), key=lambda item: item[1])
            logger.debug(emotion)

            if emotion[-1][0] == "happy":
                self.happyResRadioButton.setChecked(True)
            elif emotion[-1][0] == "sad":
                self.sadResRadioButton.setChecked(True)
            elif emotion[-1][0] == "angry":
                self.angryResRadioButton.setChecked(True)
            elif emotion[-1][0] == "scare":
                self.scareResRadioButton.setChecked(True)
        elif self.algorithmNNLearnRadioButton.isChecked():
            tmp = tmp.reshape((1, 10))
            emotion = self.nn.predict(tmp)
            """
            [None, happy, sad, angry, scare]
            """
            if emotion[0] == 0:
                self.happyResRadioButton.setChecked(True)
            elif emotion[0] == 1:
                self.sadResRadioButton.setChecked(True)
            elif emotion[0] == 2:
                self.angryResRadioButton.setChecked(True)
            elif emotion[0] == 3:
                self.scareResRadioButton.setChecked(True)

    def outputAnalysiResult(self):
        self.analysisEmotion()

        R = self.calculateRValue()
        self.resultText.clear()
        self.resultText.append("R = %f" % R)
        self.resultText.append("status: ")
        if R < 1.15:
            self.resultText.append("clear-headed")
        elif R < 1.45:
            self.resultText.append("tired")
        else:
            self.resultText.append("sleepy")

    def calculateRValue(self):
        return ((self.dr.high_alpha+self.dr.low_alpha)+self.dr.theta) / \
            (self.dr.high_beta + self.dr.low_beta)


def gui_thread():
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


if __name__ == '__main__':
    gui_thread()


#%%
