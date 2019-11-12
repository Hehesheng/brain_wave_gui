#!/usr/bin/env python3
# -*- coding=utf-8 -*-

# ==============================
# @File   ConfigWidget.py
# @Date   Created on 2019/11/12
# @Author Hehesheng
# ==============================

# %%
from Combobox import ComboBox
import parameters
import onenet
from NormalView import NormalView
from PyQt5.QtWidgets import (QApplication, QCheckBox, QDesktopWidget,
                             QGraphicsScene, QGridLayout, QRadioButton,
                             QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QMainWindow, QMessageBox, QPushButton,
                             QTextEdit, QToolTip, QTabWidget,
                             QVBoxLayout, QWidget, QGraphicsView, QStackedLayout)
from PyQt5.QtGui import QFont, QIcon, QPixmap, QTextCursor, QPalette
from PyQt5.QtCore import Qt
import socket
import ctypes
import logging

logging.basicConfig(level=logging.INFO,
                    format="[%(filename)s:%(lineno)s]-%(funcName)20s()]:%(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# %%


class ConfigTabsWidget(QTabWidget):
    """docstring for ConfigTabsWidget."""

    def __init__(self, parent=None):
        super(ConfigTabsWidget, self).__init__()
        self.parent = parent

        self.emotionRadioButtons = list()

        self.setAutoFillBackground(True)
        self.onenetTab = QWidget()
        self.networkTab = QWidget()
        self.emotionTab = QWidget()

        self.addTab(self.onenetTab, "OneNET")
        self.addTab(self.networkTab, "NetWork")
        self.addTab(self.emotionTab, "Emotion")

        self.initOnenetTab()
        self.initOnenetTabEvents()

        self.initNetworkTab()

        self.initEmotionTab()
        self.initEmotionTabEvents()

        self.hide()

    def initOnenetTab(self):
        onenetTabLayout = QVBoxLayout()
        self.onenetTab.setLayout(onenetTabLayout)

        onenetConfigLayout = QGridLayout()
        onenetGroupBox = QGroupBox(parameters.strOnenetGroupBox)
        onenetGroupBox.setLayout(onenetConfigLayout)

        onenetDeviceIdLabel = QLabel(parameters.strOneNETDeviceId)
        self.onenetDeviceIdComboBox = ComboBox()
        for info in onenet.info:
            self.onenetDeviceIdComboBox.addItem(info["id"])
        self.onenetStartButton = QPushButton(parameters.strStart)
        self.onenetModeCheckBox = QCheckBox(parameters.strAdvance)

        onenetConfigLayout.addWidget(onenetDeviceIdLabel, 0, 0)
        onenetConfigLayout.addWidget(self.onenetDeviceIdComboBox, 0, 1, 1, 2)
        onenetConfigLayout.addWidget(self.onenetModeCheckBox, 1, 0, 1, 3)
        onenetConfigLayout.addWidget(self.onenetStartButton, 2, 0, 1, 3)

        onenetTabLayout.addWidget(onenetGroupBox)
        onenetTabLayout.addStretch(1)

    def initOnenetTabEvents(self):
        self.onenetStartButton.clicked.connect(
            self.parent.onOnenetStartButtonPushed)

    def initNetworkTab(self):
        networkTabLayout = QVBoxLayout()
        self.networkTab.setLayout(networkTabLayout)

        networkConfigLayout = QGridLayout()
        networkGroupBox = QGroupBox(parameters.strNetworkGroupBox)
        networkGroupBox.setLayout(networkConfigLayout)

        self.networkModeComboBox = ComboBox()
        self.networkModeComboBox.addItem("TCP Server")
        self.networkModeComboBox.addItem("UDP Server")
        addressLabel = QLabel(parameters.strAddress)
        self.networkAddressLineEdit = QLineEdit()
        self.networkAddressLineEdit.setText(self.get_host_ip())
        portLabel = QLabel(parameters.strPort)
        self.networkPortLineEdit = QLineEdit()
        self.networkPortLineEdit.setText(parameters.strDefaultPort)
        self.networkStartButton = QPushButton(parameters.strStart)

        networkConfigLayout.addWidget(self.networkModeComboBox, 0, 0, 1, 3)
        networkConfigLayout.addWidget(addressLabel, 1, 0)
        networkConfigLayout.addWidget(self.networkAddressLineEdit, 1, 1, 1, 2)
        networkConfigLayout.addWidget(portLabel, 2, 0)
        networkConfigLayout.addWidget(self.networkPortLineEdit, 2, 1, 1, 2)
        networkConfigLayout.addWidget(self.networkStartButton, 3, 0, 1, 3)

        networkTabLayout.addWidget(networkGroupBox)
        networkTabLayout.addStretch(1)

    def initEmotionTab(self):
        emotionTabLayout = QVBoxLayout()
        self.emotionTab.setLayout(emotionTabLayout)

        emotionConfigLayout = QGridLayout()
        emotionGroupBox = QGroupBox(parameters.strEmotionGroupBox)
        emotionGroupBox.setLayout(emotionConfigLayout)

        self.happyRadioButton = QRadioButton(parameters.strEmotionHappy)
        self.sadRadioButton = QRadioButton(parameters.strEmotionSad)
        self.angryRadioButton = QRadioButton(parameters.strEmotionAngry)
        self.scareRadioButton = QRadioButton(parameters.strEmotionScare)

        self.emotionStartButton = QPushButton(parameters.strStart)

        for index, emotion in enumerate(parameters.strEmotionList):
            radioButton = QRadioButton(emotion)
            self.emotionRadioButtons.append(radioButton)
            emotionConfigLayout.addWidget(
                radioButton, index // 2, index % 2)

        emotionConfigLayout.addWidget(self.emotionStartButton, 2, 0, 1, 2)

        emotionTabLayout.addWidget(emotionGroupBox)
        emotionTabLayout.addStretch(1)

    def initEmotionTabEvents(self):
        self.emotionStartButton.clicked.connect(
            self.onEmotionStartButtonPushed)

    def onEmotionStartButtonPushed(self):
        selected = False
        index = 0
        for i, radioButton in enumerate(self.emotionRadioButtons):
            if radioButton.isChecked() == True:
                selected= True
                index = i
                break
        if selected == False:
            return
        NormalView.finetuneEmotion = index
        if NormalView.enableFinetune == False:
            NormalView.enableFinetune = True
            self.emotionStartButton.setText(parameters.strStop)
        elif NormalView.enableFinetune == True:
            NormalView.enableFinetune = False
            self.emotionStartButton.setText(parameters.strStart)

    # get ip
    def get_host_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        except Exception as e:
            logger.warning(e)
            ip = parameters.strDefaultAddress
        finally:
            s.close()

        return ip