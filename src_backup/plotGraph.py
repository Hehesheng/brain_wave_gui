import time
# #多线程支持
# import threading
# 开启交互式
# %matplotlib qt
# %matplotlib inline
import numpy as np
from scipy.fftpack import fft, ifft
import matplotlib.pyplot as plt
# import seaborn
# 色彩映射
from matplotlib import cm
# 3D tools
from mpl_toolkits.mplot3d import Axes3D
# 导入按键
from matplotlib.widgets import Button
# 解决字体问题
from pylab import mpl
# 数组堆叠
from numpy import newaxis

import socket
# json
import json
# 调整子图分布
from matplotlib.gridspec import GridSpec
# math
import math
# 功率谱
from scipy import signal
# 子图内插入子图
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

plt.rcParams['font.sans-serif'] = ['SimHei']  # 防止中文标签乱码，还有通过导入字体文件的方法
plt.rcParams['axes.unicode_minus'] = False

# 采样点集合
sampling_time_begin = 0
sampling_time_end = 1  # 1s的采样时间
Sampling_frequency = 512  # 采样频率为512hz，同步嵌入式设备采样频率
sampling_time = sampling_time_end - sampling_time_begin
Sampling_point = sampling_time * Sampling_frequency
x = np.linspace(sampling_time_begin, sampling_time_end,
                Sampling_point)  # 生成采样时间序列

# ax子图轴数值设置
ax_xlimt = sampling_time
ax_ylimt = Sampling_frequency/2
ax1_xlimt = 60  # 80zh
# 绘图函数区


def sin_plot_wireframe(x, y, a, rstride, cstride, ax):
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
    ax.plot_wireframe(x_plot_wireframe, y_plot_wireframe, z_plot_wireframe,
                      rstride=rstride, cstride=cstride, linewidth=0.5)

# 进行fft计算，返回频域信息和恢复的幅度信息


def start_fft(y):
    fft_out = fft(y)  # 快速傅里叶变换
    # fft_out_real = fft_out.real               # 获取实数部分
    # fft_out_imag = fft_out.imag               # 获取虚数部分
    fft_Amplitude = abs(fft_out)                    # 取模
    fft_Amplitude_half = fft_Amplitude[range(int(len(x)/2))]  # 由于对称性，只取一半区间

    y_fft_original_amplitude = (fft_Amplitude_half * 2)/Sampling_point  # 幅值恢复

    Frequency_point = np.arange(len(y))         # 频率
    x_Frequency_point_harf = Frequency_point[range(int(len(x)/2))]  # 取一半区间
    return y_fft_original_amplitude, x_Frequency_point_harf
# 在轴上绘制分类脑波的区间


def Draw3D_BW_range(y_max, linewidth, ax):
    # 标记脑波的频域区间
    xs = np.zeros(100)
    ys = np.linspace(0, y_max, 100)
    ax.plot(xs, ys, zs=0.1, zdir='y', color='g', linewidth=linewidth)
    ax.plot(xs, ys, zs=4, zdir='y', color='g', linewidth=linewidth)
    ax.plot(xs, ys, zs=8, zdir='y', color='g', linewidth=linewidth)
    ax.plot(xs, ys, zs=12, zdir='y', color='g', linewidth=linewidth)
    ax.plot(xs, ys, zs=30, zdir='y', color='g', linewidth=linewidth)


def Draw2D_BW_range(y_max, linewidth, ax):
    # 标记脑波的频域区间
    ys = np.linspace(0, y_max, 100)
    ax.plot(np.array([0.1]*100), ys, color='g', linewidth=linewidth)
    ax.text(0.1, y_max/2, "δ", color='r')
    ax.plot(np.array([4]*100), ys, color='g', linewidth=linewidth)
    ax.text(4, y_max/2, "θ", color='r')
    ax.plot(np.array([8]*100), ys, color='g', linewidth=linewidth)
    ax.text(8.5, y_max/2, "α", color='r')
    ax.plot(np.array([14]*100), ys, color='g', linewidth=linewidth)
    ax.text(24, y_max/2, "β", color='r')
    ax.plot(np.array([30]*100), ys, color='g', linewidth=linewidth)
    ax.text(50, y_max/2, "γ", color='r')


def visual_3D_BW_FFT(ax, x, y, ax_xlimt, ax_ylimt, ax_zlimt, x_Frequency_point_harf, y_fft_original_amplitude):
    ax.set_title('3D可视化脑波')
    ax.set_xlim(0, ax_xlimt)
    ax.set_ylim(0, ax_ylimt)
    ax.set_zlim(-ax_zlimt, ax_zlimt)
    # x、y、z轴的名称
    ax.set_xlabel('时域')
    ax.set_ylabel('频域')
    ax.set_zlabel('电压')
    # 频谱图
    ax.plot(x_Frequency_point_harf, y_fft_original_amplitude,
            zs=0, zdir='x', color='r', linewidth=3)
    # ax_xlimt/(1/N) 调整x轴绘制点数量
    sinpoint = int(ax_xlimt/(1/Sampling_point))
    # 绘制wireframe傅里叶展开图
    sin_plot_wireframe(x, x_Frequency_point_harf,
                       y_fft_original_amplitude, 10, 100, ax)
    Draw3D_BW_range(ax_zlimt, 1, ax)
    # 原信号,调制画图长度
    x_point = x[0:sinpoint]
    y_point = y[0:sinpoint]
    ax.plot(x_point, y_point, zs=0, zdir='y', color='b', linewidth=1)
    # 视角控制
#     ax.elev = 10
#     ax.azim = -60
#     ax.dist = 10


def visual_2D_BW_FFT(ax, ax_xlimt, ax_ylimt, x_Frequency_point_harf, y_fft_original_amplitude):
    ax.set_title('频谱分析')
    ax.set_xlim(-1, ax_xlimt)
    ax.set_ylim(-1, ax_ylimt)
    # x、y、z轴的名称
    ax.set_xlabel('频域')
    ax.set_ylabel('电压值')
    # 频谱图
    ax.plot(x_Frequency_point_harf[1:60],
            y_fft_original_amplitude[1:60], color='r', linewidth=1)
    Draw2D_BW_range(ax_ylimt, 3, ax)


def visual_2D_HM_R_FFT(ax, x_human, r_human):
    ax.set_title('生物阻抗测量')
    ax.plot(x_human, r_human)


def visual_2D_PSD(ax, ax_xlimt, PSD_Frequency_point, PSD):
    ax.set_title('功率谱密度')
    # ax3子图基本设定
    ax.set_xlim(0, ax_xlimt)
    # x、y、z轴的名称
    ax.set_xlabel('频域')
    ax.set_ylabel('PSD')
    # 绘图
    ax.semilogy(PSD_Frequency_point, PSD)
    # 添加注释要素


def visual_2D_Eigenvalues(ax, delta, theta, low_alpha, high_alpha, low_beta, high_beta, low_gamma, middle_gamma):
    ax.set_title('特征值提取')
    bar_data = (delta, theta, low_alpha, high_alpha,
                low_beta, high_beta, low_gamma, middle_gamma)
    bar_labels = [u'δ', u'θ', u'lowα', u'highα', u'lowβ',
                  u'highβ', u'lowγ', u'middleγ']  # 8个点
    ind = np.arange(len(bar_data))
    # ax4子图基本设定
    ax.set_xticks(ind)
    ax.set_xticklabels(bar_labels)
    # ax4.set_yticks(np.arange(0, max(bar_data)+100, 10))
    # x、y、z轴的名称
    ax.set_ylabel('特征值')
    # 绘图
    colors = ['blue', 'lightblue', 'lightgreen',
              'green', 'red', 'brown', 'lime']
    ax.bar(ind, bar_data, color=colors)


def visual_2D_AR(ax, attention, relex):
    ax.set_title('注意力、放松度')
    bar_data = (attention, relex)
    bar_labels = [u'attention', u'relex']  # 2个点
    ind = np.arange(len(bar_data))
    # ax5子图基本设定
    ax.set_xticks(ind)
    ax.set_xticklabels(bar_labels)
    ax.set_ylim(0, 100)
    # 开始绘图
    colors = ['lime', 'green']
    ax.bar(ind, bar_data, color=colors)


def pltfigure_init():
    # 初始化绘图平台
    fig = plt.figure(constrained_layout=True)
    # 开启交互式
#     plt.ion()
    # figure标题
    fig.suptitle("可视化脑波分析")
    # 生成子图
    gs = GridSpec(3, 3, figure=fig)
    ax = fig.add_subplot(gs[:-1, :-1], projection='3d')
    # 设置ax子图,3DFFT
    ax.set_title('3D可视化脑波')
    ax.set_xlabel('时域')
    ax.set_ylabel('频域')
    ax.set_zlabel('电压')

    ax1 = fig.add_subplot(gs[0, -1])
    # 设置ax1子图,频谱图
    ax1.set_title('频谱分析')
    ax1.set_xlabel('频域')
    ax1.set_ylabel('电压值')

    ax2 = fig.add_subplot(gs[1, -1])
    # 设置ax2子图，生物信息阻抗
    ax2.set_title('生物阻抗测量')

    ax3 = fig.add_subplot(gs[-1, 0])
    # 设置ax3子图，显示功率谱密度
    ax3.set_title('功率谱密度')
    ax3.set_xlabel('频域')
    ax3.set_ylabel('PSD')

    ax4 = fig.add_subplot(gs[-1, 1])
    # 设置ax4子图，显示特征值提取
    ax4.set_title('特征值提取')
    ax4.set_ylabel('特征值')
    bar_labels = [u'δ', u'θ', u'lowα', u'highα', u'lowβ',
                  u'highβ', u'lowγ', u'middleγ']  # 8
    ind = np.arange(8)
    ax4.set_xticks(ind)
    ax4.set_xticklabels(bar_labels)
    ax.set_ylim(0, 100)

    ax5 = fig.add_subplot(gs[-1, -1])
    # 设置ax5子图，显示注意力与放松度
    ax5.set_title('注意力、放松度')
    bar_labels = [u'attention', u'relex']  # 2
    ind = np.arange(2)
    ax5.set_xticks(ind)
    ax5.set_xticklabels(bar_labels)

    fig.align_labels()  # 对齐标签
    # plt.show()
    return fig, ax, ax1, ax2, ax3, ax4, ax5


def main():
    re_success = -1
    # 绘图平台初始化
    fig, ax, ax1, ax2, ax3, ax4, ax5 = pltfigure_init()

    j = ''
    # 建立一个ipv4，tcp的socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 9999))  # 设置监听端口
    s.listen(1)  # 同时只能有一个连接
    print('Waiting for connection...')
    sock, addr = s.accept()  # 阻塞函数，等待连接
    print('addr', addr)  # 连接成功，进入循环
    # plt.ion()
    plt.show(block=False)
    plt.pause(0.01)

    while True:  # 循环更新数据
        data = sock.recv(1024)
        data_ascii = data.decode('ascii')
        if data_ascii == 'ending':  # 如果发送了ending，就结束连接
            s.close()
        j = j + data_ascii  # 字符串拼接，这说明json包满意完整的接受到
        # 解析
        if j[-1] == '}':  # 完整的接收到了一个json包
            print(j)
            try:
                re_data_py = json.loads(j)
                print('json OK')
                j = ''
            except Exception as e:
                print('json error')
                j = ''
                continue
            tp = re_data_py['type']
            if tp == 'TGAM':
                l = re_data_py['raw_data']['len']  # 提取数据
                y = re_data_py['raw_data']['raw']  # 提取数据
                sign = re_data_py['pack_data']['sign']
                delta = re_data_py['pack_data']['detal']
                theta = re_data_py['pack_data']['theta']
                low_alpha = re_data_py['pack_data']['low_alpha']
                high_alpha = re_data_py['pack_data']['high_alpha']
                low_beta = re_data_py['pack_data']['low_beta']
                high_beta = re_data_py['pack_data']['high_beta']
                low_gamma = re_data_py['pack_data']['high_beta']
                middle_gamma = re_data_py['pack_data']['middle_gamma']
                attention = re_data_py['pack_data']['attention']
                relex = re_data_py['pack_data']['relex']
                if l == 512:
                    re_success = 1
                    print("TGMAdata is coming")

            elif tp == 'AD5933':
                stsrt_f = re_data_py['start']
                end_f = re_data_py['end']
                len_AD5933 = re_data_py['len']
                rel_AD5933 = re_data_py['real']
                img_AD5933 = re_data_py['image']
                print("AD5933data is coming")
                re_success = 2
        # 更新
        if re_success == 1:
            ax.clear()
            ax1.clear()
            ax3.clear()
            ax4.clear()
            ax5.clear()
            # 先做fft
            y_fft_original_amplitude, x_Frequency_point_harf = start_fft(y)
            # 使用Welch方法估算功率谱密度,
            PSD_Frequency_point, PSD = signal.welch(y, Sampling_frequency)
            # ！！！！！！！！！！！设置ax子图,3DFFT
            ax_zlimt = 2*(max(y_fft_original_amplitude) + max(y))/3
            visual_3D_BW_FFT(ax, x, y, ax_xlimt, ax_ylimt, ax_zlimt,
                             x_Frequency_point_harf, y_fft_original_amplitude)
            # ！！！！！！！！！设置ax1子图,频谱图
            ax1_ylimt = max(y_fft_original_amplitude) + 1
            visual_2D_BW_FFT(ax1, ax1_xlimt, ax1_ylimt,
                             x_Frequency_point_harf, y_fft_original_amplitude)
            # ！！！！！！！！！设置ax3子图，显示功率谱密度
            ax3_xlimt = len(PSD_Frequency_point)+10  # 每次只描述60个点的变化，也就是1min
            visual_2D_PSD(ax3, ax3_xlimt, PSD_Frequency_point, PSD)
            # ！！！！！！！！！设置ax4子图，显示特征值提取
            visual_2D_Eigenvalues(ax4, delta, theta, low_alpha,
                                  high_alpha, low_beta, high_beta, low_gamma, middle_gamma)
            # ！！！！！！！！！设置ax5子图，显示注意力与放松度
            visual_2D_AR(ax5, attention, relex)
            fig.align_labels()  # 对齐标签
            # plt.draw()  # 刷新
            plt.pause(0.01)  # 设置暂停
            print("TGAM ending")
            re_success = 0

        if re_success == 2:
            ax2.clear()
            # ！！！！！！！！设置ax2子图，生物信息阻抗
            x_human = np.linspace(stsrt_f, end_f, len_AD5933)
            r_human = np.power(np.power(rel_AD5933, 2) +
                               np.power(img_AD5933, 2), 1/2)
            visual_2D_HM_R_FFT(ax2, x_human, r_human)
            fig.align_labels()  # 对齐标签
            # plt.draw()  # 刷新
            plt.pause(0.01)  # 设置暂停
            print("AD9953 ending")
            re_success = 0


#     plt.ioff()       # 关闭画图的窗口，即关闭交互模式
#     plt.show()       # 显示图片，防止闪退

if __name__ == '__main__':
    # 开启主进程
    main()


# 暂时不用
# def PSD_extract_DE(PSD, Sampling_frequency):  # 计算各个频段的PSD、DE,提取特征
#     PSD_delta = np.sum(PSD[0:4])/((4/Sampling_frequency) -
#                                   (0.1/Sampling_frequency)+1)  # 0.1-4hz
#     DE_delta = math.log2(PSD_detal)  # 微分熵
#     PSD_theta = np.sum(PSD[4:8])/((8/Sampling_frequency) -
#                                   (4/Sampling_frequency)+1)  # 4-8hz
#     DE_theta = math.log2(PSD_theta)  # 微分熵
#     PSD_alpha = np.sum(PSD[8:12])/((12/Sampling_frequency) -
#                                    (8/Sampling_frequency)+1)  # 8-12hz
#     DE_alpha = math.log2(PSD_alpha)  # 微分熵
#     PSD_beta = np.sum(PSD[12:30])/((30/Sampling_frequency) -
#                                    (0.1/Sampling_frequency)+1)  # 12-30hz
#     DE_beta = math.log2(PSD_beta)  # 微分熵
#     PSD_gamma = np.sum(PSD[30:])/((256/Sampling_frequency) -
#                                   (30/Sampling_frequency)+1)  # 30hz
#     DE_gamma = math.log2(PSD_gamma)  # 微分熵
#     # attention
#     # relex
#     return DE_delta, DE_theta, DE_alpha, DE_beta, DE_gamma
