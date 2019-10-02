#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ==============================
# @File   Figure_Canvas.py
# @Date   Created on 2019/08/20
# @Author Hehesheng
# ==============================

from PyQt5.QtWidgets import (QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QMainWindow, QMessageBox, QPushButton,
                             QRadioButton, QSplitter, QTextEdit, QToolTip,
                             QVBoxLayout, QWidget, QGraphicsView)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import logging
import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5

logging.basicConfig(level=logging.INFO,
                    format="[%(filename)s:%(lineno)s]-%(funcName)20s()]:%(message)s")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# 通过继承FigureCanvas类，使得该类既是一个PyQt5的Qwidget，又是一个matplotlib的FigureCanvas，这是连接pyqt5与matplotlib的关键
class Figure_Canvas(FigureCanvas):

    last_data = None

    def __init__(self, parent=None, width=11, height=5, dpi=100):
        # 创建一个Figure，注意：该Figure为matplotlib下的figure，不是matplotlib.pyplot下面的figure
        fig = Figure(figsize=(width, height), dpi=100)

        FigureCanvas.__init__(self, fig)  # 初始化父类
        self.setParent(parent)

        # 调用figure下面的add_subplot方法，类似于matplotlib.pyplot下面的subplot方法
        self.noticAxes = fig.add_subplot(133)
        self.featuresAxes = fig.add_subplot(121)

    def updatePack(self, pack):
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

        self.bar_wave_data = (self.delta, self.theta, self.low_alpha, self.high_alpha,
                              self.low_beta, self.high_beta, self.low_gamma, self.middle_gamma)
        self.bar_notice_data = (self.attention, self.relex)

    def plot_bar(self, pack):
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

        self.bar_wave_data = (self.delta, self.theta, self.low_alpha, self.high_alpha,
                              self.low_beta, self.high_beta, self.low_gamma, self.middle_gamma)
        self.bar_wave_labels = [u'δ', u'θ', u'lowα', u'highα', u'lowβ',
                                u'highβ', u'lowγ', u'middleγ']  # 8个点
        colors = ['blue', 'lightblue', 'lightgreen',
                  'green', 'red', 'brown', 'lime', 'purple']
        ind = np.arange(len(self.bar_wave_labels))

        self.featuresAxes.set_xticks(ind)
        self.featuresAxes.set_xticklabels(self.bar_wave_labels)
        self.featuresAxes.set_ylabel(u'特征值')

        self.featuresAxes.bar(ind, self.bar_wave_data, color=colors)

        self.bar_notice_data = (self.attention, self.relex)
        self.bar_notice_labels = [u'attention', u'relax']  # 2个点
        colors = ['lime', 'green']
        ind = np.arange(len(self.bar_notice_data))

        self.noticAxes.set_title(u'注意力、放松度')
        self.noticAxes.set_xticks(ind)
        self.noticAxes.set_xticklabels(self.bar_notice_labels)
        self.noticAxes.set_ylim(0, 100)

        self.noticAxes.bar(ind, self.bar_notice_data, color=colors)

        self.last_data = self.bar_wave_data + self.bar_notice_data

        self.draw()
