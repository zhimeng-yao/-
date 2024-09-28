import sys
import numpy as np
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QComboBox, QGridLayout, QFileDialog, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from numpy import linspace, sqrt, arctan, square, cos
from numpy import *

# 设置默认字体为黑体以支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def wavelength_to_map(wavelength):
    """
    根据波长生成自定义颜色映射。

    参数：
    - wavelength：波长值。

    返回：
    - ListedColormap 对象，用于特定波长的颜色映射。
    """
    COL = np.load("MyColorMap.npy")
    xRGB = int(ceil(abs(780 - wavelength) / 2))
    Acmx = linspace(0, COL[0][xRGB], 255)
    Acmy = linspace(0, COL[1][xRGB], 255)
    Acmz = linspace(0, COL[2][xRGB], 255)
    return ListedColormap(squeeze(array([[Acmx], [Acmy], [Acmz]])).T, "mymap")


class MichelsonInterferenceSimulator(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置主窗口属性
        self.setWindowTitle("迈克尔逊干涉演示实验")
        self.setGeometry(100, 100, 1600, 800)
        """设置窗口标题和初始位置及大小。"""

        # 创建主部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        """创建主部件和水平布局，用于容纳左右中三个主要部分。"""

        # 左侧布局：实验目的 + 计算公式 + 实验原理图
        left_layout = QVBoxLayout()
        left_layout.setSpacing(20)
        main_layout.addLayout(left_layout)
        """创建左侧垂直布局，设置间距，用于放置实验目的、计算公式和实验原理图相关内容。"""

        # 实验目的（标题）
        self.objectives_title = QLabel("实验目的")
        self.objectives_title.setAlignment(Qt.AlignCenter)
        self.objectives_title.setStyleSheet("font-size: 28px; font-weight: bold; border: 2px solid #7f8c8d; padding: 10px; background-color: #b3cde0;")
        """设置实验目的标题的样式，包括字体大小、加粗、居中对齐、边框和背景颜色。"""
        left_layout.addWidget(self.objectives_title)

        # 实验目的（内容）
        self.objectives_display = QLabel("实验目的:\n1. 了解迈克尔逊干涉原理\n2. 观察干涉条纹变化")
        self.objectives_display.setStyleSheet("font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")
        """设置实验目的内容的样式，包括字体大小、边框和白色背景。"""
        left_layout.addWidget(self.objectives_display)

        # 计算公式（标题）
        self.formula_title = QLabel("实验计算公式")
        self.formula_title.setAlignment(Qt.AlignCenter)
        self.formula_title.setStyleSheet("font-size: 28px; font-weight: bold; border: 2px solid #7f8c8d; padding: 10px; background-color: #b3cde0;")
        """设置计算公式标题的样式，同实验目的标题。"""
        left_layout.addWidget(self.formula_title)

        # 计算公式（内容）
        self.formula_display = QLabel("光程差 = 2d*cos(θ)")
        self.formula_display.setStyleSheet("font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")
        """设置计算公式内容的样式，同实验目的内容。"""
        left_layout.addWidget(self.formula_display)

        # 实验原理图标签设置黑体
        self.principle_img_label = QLabel("实验原理图")
        self.principle_img_label.setAlignment(Qt.AlignCenter)
        self.principle_img_label.setStyleSheet("font-size: 28px; font-weight: bold; border: 2px solid #7f8c8d; padding: 10px; background-color: #b3cde0;")
        self.principle_img_label.setFont(QFont("SimHei", 24))
        """设置实验原理图标签的样式，包括居中对齐、加粗、边框、背景颜色和黑体字体。"""
        self.principle_img = QLabel()

        # 获取图片路径并设置固定大小
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, '迈克尔逊原理图.png')
        pixmap = QPixmap(image_path).scaled(400, 500, Qt.KeepAspectRatio)
        self.principle_img.setPixmap(pixmap)
        self.principle_img.setAlignment(Qt.AlignCenter)
        """加载实验原理图图片，设置固定大小并居中显示。"""

        left_layout.addWidget(self.principle_img_label)
        left_layout.addWidget(self.principle_img)

        # 添加原理演示按钮
        self.demo_button = QPushButton("原理演示")
        self.demo_button.setStyleSheet("font-size: 24px; background-color: #007bff; color: white;")
        """设置原理演示按钮的样式，包括字体大小、背景颜色和文字颜色。"""
        left_layout.addWidget(self.demo_button)

        # 中间布局：仿真结果图
        middle_layout = QVBoxLayout()
        middle_layout.setSpacing(10)
        main_layout.addLayout(middle_layout)
        """创建中间垂直布局，设置间距，用于放置仿真结果图。"""

        # 修改子图布局：将两个图垂直排列，并调整上下之间的距离
        # 增大上半部分图的比例
        self.figure, self.axs = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 2]}, figsize=(10, 12))
        self.figure.subplots_adjust(hspace=0.5)
        self.canvas = FigureCanvas(self.figure)
        middle_layout.addWidget(self.canvas)
        """使用 matplotlib 创建两个垂直排列的子图，设置子图高度比例、图形大小和上下间距。
        然后通过 FigureCanvas 将图形嵌入到 PyQt5 的布局中，并添加到中间布局。"""

        # 给上半部分图添加标题
        self.axs[0].set_title("等倾干涉图", fontsize=20)
        """为上半部分子图设置标题和字体大小。"""

        # 右侧布局：参数设置（材料 + 计算结果）和保存区
        right_layout = QVBoxLayout()
        right_layout.setSpacing(20)
        main_layout.addLayout(right_layout)
        """创建右侧垂直布局，设置间距，用于放置参数设置和保存区相关内容。"""

        # 参数布局
        param_layout = QGridLayout()
        param_layout.setHorizontalSpacing(20)
        param_layout.setVerticalSpacing(20)
        right_layout.addLayout(param_layout)
        """创建网格布局，设置水平和垂直间距，用于放置参数输入相关的标签和输入框。"""

        # 波长输入
        wavelength_label = QLabel("波长 (nm):")
        wavelength_label.setStyleSheet("font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")
        """设置波长输入标签的样式，包括字体大小、边框和白色背景。"""
        param_layout.addWidget(wavelength_label, 0, 0)
        self.wavelength_input = QLineEdit()
        self.wavelength_input.setText(str(632.8))
        self.wavelength_input.setStyleSheet("font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")
        """创建波长输入框，设置初始值和样式。"""
        param_layout.addWidget(self.wavelength_input, 0, 1)

        # 屏宽输入
        screen_width_label = QLabel("屏宽(mm):")
        screen_width_label.setStyleSheet("font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")
        """设置屏宽输入标签的样式。"""
        param_layout.addWidget(screen_width_label, 1, 0)
        self.screen_width_input = QLineEdit()
        self.screen_width_input.setText(str(15.0))
        self.screen_width_input.setStyleSheet("font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")
        """创建屏宽输入框并设置初始值和样式。"""
        param_layout.addWidget(self.screen_width_input, 1, 1)

        # 距离输入
        distance_label = QLabel("距离(mm):")
        distance_label.setStyleSheet("font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")
        """设置距离输入标签的样式。"""
        param_layout.addWidget(distance_label, 2, 0)
        self.distance_input = QLineEdit()
        self.distance_input.setText(str(10.0))
        self.distance_input.setStyleSheet("font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")
        """创建距离输入框并设置初始值和样式。"""
        param_layout.addWidget(self.distance_input, 2, 1)

        # 折射率输入
        refractive_index_label = QLabel("折射率:")
        refractive_index_label.setStyleSheet("font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")
        """设置折射率输入标签的样式。"""
        param_layout.addWidget(refractive_index_label, 3, 0)
        self.refractive_index_input = QLineEdit()
        self.refractive_index_input.setText(str(1.00))
        self.refractive_index_input.setStyleSheet("font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")
        """创建折射率输入框并设置初始值和样式。"""
        param_layout.addWidget(self.refractive_index_input, 3, 1)

        # 像素输入
        pixel_label = QLabel("像素n:")
        pixel_label.setStyleSheet("font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")
        """设置像素输入标签的样式。"""
        param_layout.addWidget(pixel_label, 4, 0)
        self.pixel_input = QLineEdit()
        self.pixel_input.setText(str(400))
        self.pixel_input.setStyleSheet("font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")
        """创建像素输入框并设置初始值和样式。"""
        param_layout.addWidget(self.pixel_input, 4, 1)

        # 计算结果按钮
        self.calculate_button = QPushButton("计算结果")
        self.calculate_button.setStyleSheet("font-size: 24px; background-color: #007bff; color: white;")
        self.calculate_button.clicked.connect(self.calculate_results)
        """设置计算结果按钮的样式，并连接到计算结果方法。"""
        param_layout.addWidget(self.calculate_button, 5, 0, 1, 2)

        # 提前预留空间的结果显示部分
        self.result_display = QLabel("\n\n\n\n\n\n\n\n\n\n\n\n结果显示:\n干涉条纹：")
        self.result_display.setStyleSheet("font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")
        right_layout.addWidget(self.result_display)
        """创建结果显示标签，设置样式和预留的显示内容。"""

        # 保存区：保存图像和实验数据
        save_layout = QVBoxLayout()
        save_layout.setSpacing(20)
        right_layout.addLayout(save_layout)
        """创建保存区的垂直布局，设置间距。"""

        # 图像名称输入
        image_name_label = QLabel("图像名称:")
        image_name_label.setStyleSheet("font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")
        """设置图像名称输入标签的样式。"""
        save_layout.addWidget(image_name_label)
        self.image_name_input = QLineEdit()
        self.image_name_input.setStyleSheet("font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")
        """创建图像名称输入框并设置样式。"""
        save_layout.addWidget(self.image_name_input)

        # 图像格式选择
        image_format_label = QLabel("图像格式:")
        image_format_label.setStyleSheet("font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")
        """设置图像格式选择标签的样式。"""
        save_layout.addWidget(image_format_label)
        self.image_format_combo = QComboBox()
        self.image_format_combo.addItems(["jpg", "png", "bmp"])
        self.image_format_combo.setStyleSheet("font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")
        """创建图像格式选择下拉框，添加可选格式并设置样式。"""
        save_layout.addWidget(self.image_format_combo)

        self.save_img_button = QPushButton("保存干涉图像")
        self.save_img_button.setStyleSheet("font-size: 24px; background-color: #007bff; color: white;")
        self.save_img_button.clicked.connect(self.save_image)
        """设置保存干涉图像按钮的样式，并连接到保存图像方法。"""
        save_layout.addWidget(self.save_img_button)

        self.save_data_button = QPushButton("保存实验数据")
        self.save_data_button.setStyleSheet("font-size: 24px; background-color: #007bff; color: white;")
        self.save_data_button.clicked.connect(self.save_data)
        """设置保存实验数据按钮的样式，并连接到保存数据方法。"""
        save_layout.addWidget(self.save_data_button)

        # 退出按钮
        self.quit_button = QPushButton("退出")
        self.quit_button.setStyleSheet("font-size: 24px; background-color: #dc3545; color: white;")
        self.quit_button.clicked.connect(self.close)
        """设置退出按钮的样式，并连接到关闭窗口的方法。"""
        save_layout.addWidget(self.quit_button)

        #
        self.default_wavelength = 632.8
        self.default_screen_width = 15.0
        self.default_distance = 10.0
        self.default_refractive_index = 1.00
        self.default_pixel = 400
        self.default_angle_range = np.linspace(0, 2 * np.pi, 300)
        self.calculate_and_display(self.default_angle_range, self.default_wavelength, self.default_distance, self.default_refractive_index)

    def calculate_results(self):
        """
        计算结果并更新显示。

        尝试获取用户输入的波长、屏宽、距离、折射率和像素等参数，
        若参数有效，则计算干涉条纹强度，更新结果显示文本，
        并调用 animate_simulation 方法更新图形。若输入无效，则弹出错误提示框。
        """
        try:
            # 获取用户输入的波长
            selected_wavelength = float(self.wavelength_input.text())

            # 获取用户输入的参数，如果输入为空则默认为 0
            screen_width = float(self.screen_width_input.text()) if self.screen_width_input.text() else 0
            distance = float(self.distance_input.text()) if self.distance_input.text() else 0
            refractive_index = float(self.refractive_index_input.text()) if self.refractive_index_input.text() else 0
            pixel = float(self.pixel_input.text()) if self.pixel_input.text() else 0

            # 使用默认的角度范围
            self.angle_range = np.linspace(0, 2 * np.pi, 300)

            # 临时随机生成强度值（此处应该替换为实际的计算逻辑）
            self.interference_intensity = np.random.rand(len(self.angle_range))

            # 更新结果显示文本
            self.result_display.setText(
                f"结果显示:\n波长: {selected_wavelength} nm\n屏宽: {screen_width}\n距离: {distance}\n折射率: {refractive_index}\n像素: {pixel}\n干涉条纹：{self.interference_intensity[-1]:.2f}")

            # 更新图形
            self.animate_simulation(self.angle_range, self.interference_intensity, selected_wavelength, distance,
                                    refractive_index)
        except ValueError:
            # 如果输入不是有效的数字，弹出错误提示框
            QMessageBox.warning(self, "错误", "请输入有效的数字。")

    def calculate_and_display(self, angle_range, wavelength, distance, refractive_index):
        """
        计算并显示模拟结果。

        根据输入的参数计算干涉条纹强度，并绘制图像和光强分布图。

        Args:
            angle_range (numpy.ndarray): 角度范围数组。
            wavelength (float): 波长。
            distance (float): 距离。
            refractive_index (float): 折射率。
        """
        # 获取屏宽的值，如果输入为空则默认为 0
        screen_width = float(self.screen_width_input.text()) if self.screen_width_input.text() else 0

        # 新的变量替换部分
        # 将波长转换为米
        lamda = wavelength * 1e-9
        # 将距离转换为米
        d = distance * 1e-3
        # 将屏宽转换为米
        x_lim = screen_width * 1e-3
        # 设定网格点数
        N = 500
        # 生成位置数组
        x = np.linspace(-x_lim, x_lim, N)
        # 创建二维网格
        [X, Y] = np.meshgrid(x, x)
        # 计算到中心的距离
        r = np.sqrt(np.square(X) + np.square(Y))
        # 计算弧度值
        i = np.arctan(np.sqrt(np.square(r)))
        # 计算光程差
        delta = 2 * refractive_index * d * np.cos(i)
        # 计算波矢差
        k = np.pi * delta / lamda
        # 计算光强
        I0 = np.square(np.cos(k))
        # 根据波长获取颜色映射
        my_cmap = wavelength_to_map(wavelength)
        # 在第一个子图中绘制干涉条纹图像
        self.axs[0].imshow(2 * I0, cmap=my_cmap, interpolation='bessel', origin='lower', vmin=0, vmax=1)
        self.axs[0].axis('off')

        # 绘制光强分布图
        I = I0[:, int(N / 2)]
        self.axs[1].set_title("光强分布图", fontsize=20)
        self.axs[1].set_xlabel("位置", fontsize=18)
        self.axs[1].set_ylabel("光强", fontsize=18)
        # 在第二个子图中绘制光强随位置的变化曲线
        self.axs[1].plot(x, I, color=my_cmap.colors[-1], linewidth=1.5)
        labels = self.axs[1].get_xticklabels() + self.axs[1].get_yticklabels()
        [label.set_fontname('Times New Roman') for label in labels]
        self.canvas.draw()

    def animate_simulation(self, angle_range, interference_intensity, wavelength, distance, refractive_index):
        """
        调用 calculate_and_display 方法更新图形。

        Args:
            angle_range (numpy.ndarray): 角度范围数组。
            interference_intensity (numpy.ndarray): 干涉条纹强度数组。
            wavelength (float): 波长。
            distance (float): 距离。
            refractive_index (float): 折射率。
        """
        self.calculate_and_display(angle_range, wavelength, distance, refractive_index)

    # 保存图像方法
    def save_image(self):
        """
        保存图像。

        弹出文件保存对话框，获取用户指定的文件名和格式，保存图像文件。
        """
        image_name = self.image_name_input.text()
        image_format = self.image_format_combo.currentText()
        options = QFileDialog.Options()
        # 获取用户指定的文件名和格式
        file_name, _ = QFileDialog.getSaveFileName(self, "保存图像", "",
                                                   f"{image_format.upper()} Files (*.{image_format.lower()});;All Files (*)",
                                                   options=options)
        if file_name:
            # 保存图像
            self.figure.savefig(file_name)

    def save_data(self):
        """
        保存实验数据。

        弹出文件保存对话框，获取用户指定的文件名，将角度和干涉条纹强度数据保存为文本文件。
        """
        options = QFileDialog.Options()
        # 获取用户指定的文件名
        file_name, _ = QFileDialog.getSaveFileName(self, "保存实验数据", "", "Text Files (*.txt);;All Files (*)",
                                                   options=options)
        if file_name:
            with open(file_name, 'w') as file:
                # 写入文件头
                file.write("角度, 干涉条纹强度\n")
                for i in range(len(self.interference_intensity)):
                    # 写入角度和干涉条纹强度数据
                    file.write(f"{self.angle_range[i]:.2f}, {self.interference_intensity[i]:.2f}\n")


# 应用程序启动入口
if __name__ == "__main__":
    # 创建一个 QApplication 对象，sys.argv 是命令行参数列表
    app = QApplication(sys.argv)
    # 创建自定义窗口类的实例
    window = MichelsonInterferenceSimulator()
    # 显示窗口
    window.show()
    # 开始应用程序的事件循环，并在应用程序退出时返回状态码，然后退出 Python 解释器
    sys.exit(app.exec_())