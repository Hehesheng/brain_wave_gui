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
import json
import onenet

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

    def __init__(self, parent=None, canvasParent=None, id=None, width=12, height=10, dpi=100):
        # 创建一个Figure，注意：该Figure为matplotlib下的figure，不是matplotlib.pyplot下面的figure
        super().__init__()
        self.parent = parent
        self.id = id
        self.lastTickTgam = 0
        self.lastTickAd59 = 0
        self.count = 0
        self.__isUpdate = False
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
        # onenet service
        self.onenetTgam = onenet.onenet(self.id, "tgam_pack")
        self.onenetAd59 = onenet.onenet(self.id, "ad59_pack")

    def target(self):
        self.count = self.count + 1
        if self.count % 4 == 0:
            return self.onenetAd59.get_current_onenet()
        return self.onenetTgam.get_current_onenet()

    def plotUpdate(self):
        self.canvas.draw()

    def setUpdate(self, val):
        self.__isUpdate = val

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

    def update(self, packDict):
        self.packDict = packDict
        tp = self.getPackType()

        if tp == "TGAM":
            try:
                if self.packDict["tick"] != self.lastTickTgam:
                    self.lastTickTgam = self.packDict["tick"]
                    self.tgamPackDict = self.packDict
                else:
                    return 0
            except Exception:
                return -1

        if tp == "AD5933":
            try:
                if self.packDict["tick"] != self.lastTickAd59:
                    self.lastTickAd59 = self.packDict["tick"]
                    self.ad59PackDict = self.packDict
                else:
                    return 0
            except Exception:
                return -1

        self.setUpdate(True)
        ret = 0

        if tp == "TGAM":
            logger.debug("Rec TGAM Pack")
            ret = self.tgamUpdate(self.packDict)
        elif tp == "AD5933":
            logger.debug("Rec AD5933 Pack")
            ret = self.ad5599Update(self.packDict)
        elif tp == "CMD":
            logger.debug("Rec CMD Pack")
            ret = -1
        else:
            logger.warning("Unknown Type.")
            ret = -1
        self.setUpdate(False)
        return ret

    def getPackType(self):
        return self.packDict["type"]

    def sin_plot_wireframe(self, x, y, a, rstride, cstride):
        # 获取数据
        x_plot_wireframe = x
        x_plot_wireframe_a = x
        y_plot_wireframe = y
        a_plot_wireframe = a
        # 生成数据网格
        x_plot_wireframe_a, a_plot_wireframe = np.meshgrid(
            x_plot_wireframe_a, a_plot_wireframe)
        x_plot_wireframe, y_plot_wireframe = np.meshgrid(
            x_plot_wireframe, y_plot_wireframe)
        # 计算z
        z_plot_wireframe = a_plot_wireframe * \
            np.sin(2 * np.pi * y_plot_wireframe * x_plot_wireframe)
        # 画图
        self.fft3dAx.plot_wireframe(x_plot_wireframe, y_plot_wireframe, z_plot_wireframe,
                                    rstride=rstride, cstride=cstride, linewidth=0.5)

    def start_fft(self, y):
        # 进行fft计算，返回频域信息和恢复的幅度信息
        fft_out = fft(y)  # 快速傅里叶变换

        fft_Amplitude = abs(fft_out)                    # 取模
        fft_Amplitude_half = fft_Amplitude[range(
            int(len(self.fft3dAx_x)/2))]  # 由于对称性，只取一半区间

        y_fft_original_amplitude = (
            fft_Amplitude_half * 2)/self.Sampling_point  # 幅值恢复

        Frequency_point = np.arange(len(y))         # 频率
        x_Frequency_point_harf = Frequency_point[range(
            int(len(self.fft3dAx_x)/2))]  # 取一半区间
        return y_fft_original_amplitude, x_Frequency_point_harf

    # 在轴上绘制分类脑波的区间
    def Draw3D_BW_range(self, y_max, linewidth):
        # 标记脑波的频域区间
        xs = np.zeros(100)
        ys = np.linspace(0, y_max, 100)
        self.fft3dAx.plot(xs, ys, zs=0.1, zdir='y',
                          color='g', linewidth=linewidth)
        self.fft3dAx.plot(xs, ys, zs=4, zdir='y',
                          color='g', linewidth=linewidth)
        self.fft3dAx.plot(xs, ys, zs=8, zdir='y',
                          color='g', linewidth=linewidth)
        self.fft3dAx.plot(xs, ys, zs=12, zdir='y',
                          color='g', linewidth=linewidth)
        self.fft3dAx.plot(xs, ys, zs=30, zdir='y',
                          color='g', linewidth=linewidth)

    def Draw2D_BW_range(self, y_max, linewidth):
        # 标记脑波的频域区间
        ys = np.linspace(0, y_max, 100)
        self.freqScoreAx.plot(
            np.array([0.1]*100), ys, color='g', linewidth=linewidth)
        self.freqScoreAx.text(0.1, y_max/2, "δ", color='r')
        self.freqScoreAx.plot(
            np.array([4]*100), ys, color='g', linewidth=linewidth)
        self.freqScoreAx.text(4, y_max/2, "θ", color='r')
        self.freqScoreAx.plot(
            np.array([8]*100), ys, color='g', linewidth=linewidth)
        self.freqScoreAx.text(8.5, y_max/2, "α", color='r')
        self.freqScoreAx.plot(
            np.array([14]*100), ys, color='g', linewidth=linewidth)
        self.freqScoreAx.text(24, y_max/2, "β", color='r')
        self.freqScoreAx.plot(
            np.array([30]*100), ys, color='g', linewidth=linewidth)
        self.freqScoreAx.text(50, y_max/2, "γ", color='r')

    def visual_3D_BW_FFT(self, x, y, ax_xlimt, ax_ylimt, ax_zlimt, x_Frequency_point_harf, y_fft_original_amplitude):
        self.fft3dAx.set_title(u'3D可视化脑波')
        self.fft3dAx.set_xlim(0, ax_xlimt)
        self.fft3dAx.set_ylim(0, ax_ylimt)
        self.fft3dAx.set_zlim(-ax_zlimt, ax_zlimt)
        # x、y、z轴的名称
        self.fft3dAx.set_xlabel(u'时域')
        self.fft3dAx.set_ylabel(u'频域')
        self.fft3dAx.set_zlabel(u'电压')
        # 频谱图
        self.fft3dAx.plot(x_Frequency_point_harf, y_fft_original_amplitude,
                          zs=0, zdir='x', color='r', linewidth=3)
        # ax_xlimt/(1/N) 调整x轴绘制点数量
        sinpoint = int(ax_xlimt/(1/self.Sampling_point))
        # 绘制wireframe傅里叶展开图
        self.sin_plot_wireframe(x, x_Frequency_point_harf,
                                y_fft_original_amplitude, 10, 100)
        self.Draw3D_BW_range(ax_zlimt, 1)
        # 原信号,调制画图长度
        x_point = x[0:sinpoint]
        y_point = y[0:sinpoint]
        self.fft3dAx.plot(x_point, y_point, zs=0,
                          zdir='y', color='b', linewidth=1)

    def visual_2D_BW_FFT(self, ax_xlimt, ax_ylimt, x_Frequency_point_harf, y_fft_original_amplitude):
        self.freqScoreAx.set_title('频谱分析')
        self.freqScoreAx.set_xlim(-1, ax_xlimt)
        self.freqScoreAx.set_ylim(-1, ax_ylimt)
        # x、y、z轴的名称
        self.freqScoreAx.set_xlabel(u'频域')
        self.freqScoreAx.set_ylabel(u'电压值')
        # 频谱图
        self.freqScoreAx.plot(x_Frequency_point_harf[1:60],
                              y_fft_original_amplitude[1:60], color='r', linewidth=1)
        self.Draw2D_BW_range(ax_ylimt, 3)

    def visual_2D_HM_R_FFT(self, x_human, r_human):
        self.biologyResAx.set_title(u'生物阻抗测量')
        self.biologyResAx.plot(x_human, r_human)

    def visual_2D_PSD(self, ax_xlimt, PSD_Frequency_point, PSD):
        self.powerScoreAx.set_title(u'功率谱密度')
        # ax3子图基本设定
        self.powerScoreAx.set_xlim(0, ax_xlimt)
        # x、y、z轴的名称
        self.powerScoreAx.set_xlabel(u'频域')
        self.powerScoreAx.set_ylabel(u'PSD')
        # 绘图
        self.powerScoreAx.semilogy(PSD_Frequency_point, PSD)
        # 添加注释要素

    def visual_2D_Eigenvalues(self, delta, theta, low_alpha, high_alpha, low_beta, high_beta, low_gamma, middle_gamma):
        self.featureValueAx.set_title(u'特征值提取')
        bar_data = (delta, theta, low_alpha, high_alpha,
                    low_beta, high_beta, low_gamma, middle_gamma)
        bar_labels = [u'δ', u'θ', u'lowα', u'highα', u'lowβ',
                      u'highβ', u'lowγ', u'middleγ']  # 8个点
        ind = np.arange(len(bar_data))
        # ax4子图基本设定
        self.featureValueAx.set_xticks(ind)
        self.featureValueAx.set_xticklabels(bar_labels)
        # ax4.set_yticks(np.arange(0, max(bar_data)+100, 10))
        # x、y、z轴的名称
        self.featureValueAx.set_ylabel(u'特征值')
        # 绘图
        colors = ['blue', 'lightblue', 'lightgreen',
                  'green', 'red', 'brown', 'lime']
        self.featureValueAx.bar(ind, bar_data, color=colors)

    def visual_2D_AR(self, attention, relex):
        self.noticeRelaxAx.set_title(u'注意力、放松度')
        bar_data = (attention, relex)
        bar_labels = [u'attention', u'relax']  # 2个点
        ind = np.arange(len(bar_data))
        # ax5子图基本设定
        self.noticeRelaxAx.set_xticks(ind)
        self.noticeRelaxAx.set_xticklabels(bar_labels)
        self.noticeRelaxAx.set_ylim(0, 100)
        # 开始绘图
        colors = ['lime', 'green']
        self.noticeRelaxAx.bar(ind, bar_data, color=colors)

    def ad5599Update(self, pack):
        self.biologyResAx.clear()
        self.biologyResAx_x = np.linspace(
            pack["start"], pack["end"], pack["len"])
        self.biologyResAx_r = np.power(np.power(pack["real"], 2) +
                                       np.power(pack["image"], 2), 1/2)
        self.visual_2D_HM_R_FFT(self.biologyResAx_x, self.biologyResAx_r)

        self.fig.align_labels()  # 对齐标签
        self.plotUpdate()

        return 0

    def tgamUpdate(self, pack):
        if pack["raw_data"]["len"] < 512:
            logger.warning("pack length wrong")
            return -1
        try:
            self.packDict["raw_data"]["raw"] = pack["raw_data"]["raw"][0:512]
            sign = pack['pack_data']['sign']
            delta = pack['pack_data']['detal']
            theta = pack['pack_data']['theta']
            low_alpha = pack['pack_data']['low_alpha']
            high_alpha = pack['pack_data']['high_alpha']
            low_beta = pack['pack_data']['low_beta']
            high_beta = pack['pack_data']['high_beta']
            low_gamma = pack['pack_data']['high_beta']
            middle_gamma = pack['pack_data']['middle_gamma']
            attention = pack['pack_data']['attention']
            relex = pack['pack_data']['relex']
        except Exception as identifier:
            logger.warning(identifier)
            return -1

        self.fft3dAx.clear()
        self.freqScoreAx.clear()
        self.powerScoreAx.clear()
        self.featureValueAx.clear()
        self.noticeRelaxAx.clear()

        # 先做fft
        y_fft_original_amplitude, x_Frequency_point_harf = self.start_fft(
            self.packDict['raw_data']['raw'])
        # ！！！！！！！！！！！设置ax子图,3DFFT
        fft3dAx_zlimt = 2*(max(y_fft_original_amplitude) +
                           max(self.packDict['raw_data']['raw']))/3

        self.visual_3D_BW_FFT(self.fft3dAx_x, self.packDict['raw_data']['raw'], self.fft3dAx_xlimt, self.fft3dAx_ylimt, fft3dAx_zlimt,
                              x_Frequency_point_harf, y_fft_original_amplitude)
        # ！！！！！！！！！设置ax1子图,频谱图
        freqScoreAx_ylimt = max(y_fft_original_amplitude) + 1
        self.visual_2D_BW_FFT(self.freqScoreAx_xlimt, freqScoreAx_ylimt,
                              x_Frequency_point_harf, y_fft_original_amplitude)
        # ！！！！！！！！！设置ax3子图，显示功率谱密度
        # 使用Welch方法估算功率谱密度,
        PSD_Frequency_point, PSD = signal.welch(
            self.packDict['raw_data']['raw'], self.Sampling_frequency)
        powerScoreAx_xlimt = len(PSD_Frequency_point) + \
            10  # 每次只描述60个点的变化，也就是1min
        self.visual_2D_PSD(powerScoreAx_xlimt, PSD_Frequency_point, PSD)
        # ！！！！！！！！！设置ax4子图，显示特征值提取
        self.visual_2D_Eigenvalues(delta, theta, low_alpha,
                                   high_alpha, low_beta, high_beta, low_gamma, middle_gamma)
        # ！！！！！！！！！设置ax5子图，显示注意力与放松度
        self.visual_2D_AR(attention, relex)

        self.fig.align_labels()  # 对齐标签
        self.plotUpdate()
