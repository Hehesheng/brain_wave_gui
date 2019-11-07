#!/usr/bin/env python3
# -*- coding=utf-8 -*-

# ==============================
# @File   AdvanceView.py
# @Date   Created on 2019/11/04
# @Author Hehesheng
# ==============================

from PyQt5.QtWidgets import (QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QMainWindow, QMessageBox, QPushButton,
                             QRadioButton, QTextEdit, QToolTip, QGridLayout,
                             QVBoxLayout, QWidget, QGraphicsView, QGraphicsScene)
from PyQt5.QtGui import QPixmap
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import logging
import matplotlib
import parameters

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.gridspec import GridSpec
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.mplot3d import Axes3D
from numpy import newaxis
from pylab import mpl
from scipy import signal
from scipy.fftpack import fft, ifft

matplotlib.use("Qt5Agg")  # 声明使用QT5

logging.basicConfig(level=logging.INFO,
                    format="[%(filename)s:%(lineno)s]-%(funcName)20s()]:%(message)s")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class AdvanceView(QWidget):
    """docstring for AdvanceView."""

    sampling_time_begin = 0
    sampling_time_end = 1  # 1s的采样时间
    Sampling_frequency = 512  # 采样频率为512hz，同步嵌入式设备采样频率
    sampling_time = sampling_time_end - sampling_time_begin
    Sampling_point = sampling_time * Sampling_frequency

    # ax子图轴数值设置
    fft3dAx_xlimt = sampling_time
    fft3dAx_ylimt = Sampling_frequency/2

    freqScoreAx_xlimt = 60  # 80zh
    # 生成采样时间序列
    fft3dAx_x = np.linspace(sampling_time_begin, sampling_time_end,
                            Sampling_point)

    def __init__(self, parent=None,canvasParent=None, width=12, height=10, dpi=100):
        # 创建一个Figure，注意：该Figure为matplotlib下的figure，不是matplotlib.pyplot下面的figure
        super().__init__()
        self.parent = parent
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        # self.fig = Figure()

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

        self.viewLayout = QVBoxLayout()
        self.viewLayout.addWidget(graphicsView)
        self.setLayout(self.viewLayout)

        self.canvas.draw()
        self.figureOpenInit()
        self.fft3dAxInit()
        self.freqScoreAxInit()
        self.biologyResAxInit()
        self.powerScoreAxInit()
        self.featureValueAxInit()
        self.noticeRelaxAxInit()

        self.fig.align_labels()  # 对齐标签

    def figureOpenInit(self):
        # figure标题
        self.fig.suptitle(u"可视化脑波分析")
        # 生成子图
        self.gs = GridSpec(3, 3, figure=self.fig)

    def fft3dAxInit(self):
        # 设置fft3dAx子图,3DFFT ax
        self.fft3dAx = self.fig.add_subplot(self.gs[:-1, :-1], projection='3d')
        self.fft3dAx.set_title(u'3D可视化脑波')
        self.fft3dAx.set_xlabel(u'时域')
        self.fft3dAx.set_ylabel(u'频域')
        self.fft3dAx.set_zlabel(u'电压')
        self.fft3dAx.set_ylim(0, 100)

    def freqScoreAxInit(self):
        # 设置freqScoreAx子图,频谱图 ax1
        self.freqScoreAx = self.fig.add_subplot(self.gs[0, -1])
        self.freqScoreAx.set_title(u'频谱分析')
        self.freqScoreAx.set_xlabel(u'频域')
        self.freqScoreAx.set_ylabel(u'电压值')

    def biologyResAxInit(self):
        # 设置biologyResAx子图，生物信息阻抗 ax2
        self.biologyResAx = self.fig.add_subplot(self.gs[1, -1])
        self.biologyResAx.set_title(u'生物阻抗测量')

    def powerScoreAxInit(self):
        # 设置powerScoreAx子图，显示功率谱密度 ax3
        self.powerScoreAx = self.fig.add_subplot(self.gs[-1, 0])
        self.powerScoreAx.set_title(u'功率谱密度')
        self.powerScoreAx.set_xlabel(u'频域')
        self.powerScoreAx.set_ylabel(u'PSD')

    def featureValueAxInit(self):
        # 设置featureValueAx子图，显示特征值提取 ax4
        self.featureValueAx = self.fig.add_subplot(self.gs[-1, 1])
        self.featureValueAx.set_title(u'特征值提取')
        self.featureValueAx.set_ylabel(u'特征值')
        bar_labels = [u'δ', u'θ', u'lowα', u'highα', u'lowβ',
                      u'highβ', u'lowγ', u'middleγ']  # 8
        ind = np.arange(8)
        self.featureValueAx.set_xticks(ind)
        self.featureValueAx.set_xticklabels(bar_labels)

    def noticeRelaxAxInit(self):
        # 设置noticeRelaxAx子图，显示注意力与放松度 ax5
        self.noticeRelaxAx = self.fig.add_subplot(self.gs[-1, -1])
        self.noticeRelaxAx.set_title(u'注意力、放松度')
        bar_labels = [u'attention', u'relex']  # 2
        ind = np.arange(2)
        self.noticeRelaxAx.set_xticks(ind)
        self.noticeRelaxAx.set_xticklabels(bar_labels)
