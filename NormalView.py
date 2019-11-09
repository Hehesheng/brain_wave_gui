#!/usr/bin/env python3
# -*- coding=utf-8 -*-

# ==============================
# @File   NormalView.py
# @Date   Created on 2019/10/30
# @Author Hehesheng
# ==============================

from PyQt5.QtWidgets import (QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QMainWindow, QMessageBox, QPushButton, QProgressBar,
                             QRadioButton, QTextEdit, QToolTip, QGridLayout,
                             QVBoxLayout, QWidget, QGraphicsView, QGraphicsScene)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import logging
import matplotlib
import parameters
import onenet
import time

matplotlib.use("Qt5Agg")  # 声明使用QT5

logging.basicConfig(level=logging.INFO,
                    format="[%(filename)s:%(lineno)s]-%(funcName)20s()]:%(message)s")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class NormalView(QWidget):

    signal = pyqtSignal()
    noticeColors = ['lime', 'green']
    featuresColors = ['blue', 'lightblue', 'lightgreen',
                      'green', 'red', 'brown', 'lime', 'purple']

    def __init__(self, parent=None, canvasParent=None, id=None, width=11, height=5, dpi=100):
        # 创建一个Figure，注意：该Figure为matplotlib下的figure，不是matplotlib.pyplot下面的figure
        super().__init__()
        self.parent = parent
        self.id = id
        self.emotionRadioButtons = list()
        self.emotionProgressBars = list()
        self.emotion = [0, 0, 0, 0]
        self.lastTick = 0
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        # self.fig = Figure()
        self.signal.connect(slot=self.signalSlot)

        self.canvas = FigureCanvas(self.fig)
        FigureCanvas.__init__(self.canvas, self.fig)  # 初始化父类
        self.canvas.setParent(canvasParent)
        # self.canvas.setParent(parent)
        self.canvasParent = canvasParent

        graphicsScene = QGraphicsScene()
        graphicsScene.addWidget(self.canvas)
        graphicsView = QGraphicsView()
        graphicsView.setScene(graphicsScene)
        graphicsView.show()

        self.noticeAxes = self.fig.add_subplot(133)
        self.featuresAxes = self.fig.add_subplot(121)

        self.emotionResultLayout = QGridLayout()
        emotionResultGroupBox = QGroupBox("Result")
        emotionResultGroupBox.setLayout(self.emotionResultLayout)
        for index, emotion in enumerate(parameters.strEmotionList):
            radioButton = QRadioButton(emotion)
            progressBar = QProgressBar()
            self.emotionRadioButtons.append(radioButton)
            self.emotionProgressBars.append(progressBar)
            progressBar.setFormat("%v")
            self.emotionResultLayout.addWidget(
                radioButton, index // 2, index % 2 * 2 + 1)
            self.emotionResultLayout.addWidget(
                progressBar, index // 2, index % 2 * 2 + 2)
            radioButton.toggled.connect(self.radioButtonToggled)

        self.image = QLabel()
        self.emotionResultLayout.addWidget(self.image, 0, 0, 2, 1)

        self.resultText = QTextEdit()
        self.resultText.setReadOnly(True)
        self.emotionResultLayout.addWidget(self.resultText, 0, 5, 2, 2)

        self.viewLayout = QVBoxLayout()
        self.viewLayout.addWidget(graphicsView, 3)
        self.viewLayout.addWidget(emotionResultGroupBox, 2)

        self.setLayout(self.viewLayout)

        self.initPlotTitle()
        self.canvas.draw()
        # onenet service
        self.onenet = onenet.onenet(self.id, "tgam_pack")

    def target(self):
        return self.onenet.get_current_onenet()

    def initPlotTitle(self):
        self.noticeAxes.clear()
        self.bar_notice_labels = [u'attention', u'relax']  # 2个点
        ind = np.arange(len(self.bar_notice_labels))

        self.noticeAxes.set_title(u'注意力、放松度')
        self.noticeAxes.set_xticks(ind)
        self.noticeAxes.set_xticklabels(self.bar_notice_labels)
        self.noticeAxes.set_ylim(0, 100)

        self.featuresAxes.clear()
        self.bar_features_labels = [u'δ', u'θ', u'lowα', u'highα', u'lowβ',
                                    u'highβ', u'lowγ', u'middleγ']  # 8个点
        ind = np.arange(len(self.bar_features_labels))

        self.featuresAxes.set_xticks(ind)
        self.featuresAxes.set_xticklabels(self.bar_features_labels)
        self.featuresAxes.set_ylabel(u'特征值')

    def radioButtonToggled(self):
        for button in self.emotionRadioButtons:
            if button.isChecked() == True:
                self.image.setPixmap(
                    QPixmap("./assets/%s.png" % button.text()))
    def signalSlot(self):
        for index, progressBar in enumerate(self.emotionProgressBars):
            progressBar.setValue(self.emotion[index] * 100)

    def update(self, pack):
        if pack["type"] != "TGAM":
            logger.warning("Unknown Pack Type.")
            return -1
        try:
            if pack["tick"] == self.lastTick:
                return 0
        except:
            return -1
        try:
            self.delta = pack['pack_data']['detal']
            self.theta = pack['pack_data']['theta']
            self.low_alpha = pack['pack_data']['low_alpha']
            self.high_alpha = pack['pack_data']['high_alpha']
            self.low_beta = pack['pack_data']['low_beta']
            self.high_beta = pack['pack_data']['high_beta']
            self.low_gamma = pack['pack_data']['high_beta']
            self.middle_gamma = pack['pack_data']['middle_gamma']
            self.attention = pack['pack_data']['attention']
            self.relex = pack['pack_data']['relex']
        except Exception as identifier:
            logger.warning(identifier)
            return -1
        self.bar_feature_data = (self.delta, self.theta, self.low_alpha, self.high_alpha,
                                 self.low_beta, self.high_beta, self.low_gamma, self.middle_gamma)
        self.bar_notice_data = (self.attention, self.relex)
        self.bar_data = self.bar_feature_data + self.bar_notice_data

        self.initPlotTitle()
        ind = np.arange(len(self.bar_notice_labels))
        self.noticeAxes.bar(ind, self.bar_notice_data, color=self.noticeColors)
        ind = np.arange(len(self.bar_features_labels))
        self.featuresAxes.bar(ind, self.bar_feature_data,
                              color=self.featuresColors)

        self.canvas.draw()
        self.lastTick = pack["tick"]

        tmp = np.array(self.bar_feature_data + self.bar_notice_data)
        tmp = tmp.reshape((1, 10))
        self.emotion = self.parent.nn.predict_p(tmp)
        index = np.where(self.emotion == self.emotion.max())
        print(index)
        print(self.emotion)
        self.emotionRadioButtons[index[0][0]].setChecked(True)
        self.signal.emit()

        return 0
