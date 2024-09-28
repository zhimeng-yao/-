import sys
import numpy as np
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QComboBox, QGridLayout, QFileDialog, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.animation import FuncAnimation
import math
from matplotlib.colors import LinearSegmentedColormap


# 表示长度的物理量单位 m
# 波长
def wavelength2Hex(waveLength):
    if 380 <= waveLength <= 440:
        attenuation = 0.3 + 0.7 * (waveLength - 380) / (440 - 380)
        r, g, b = ((-(waveLength - 440) / (440 - 380)) * attenuation) ** 0.8, 0.0, (1.0 * attenuation) ** 0.8
    elif 440 <= waveLength <= 490:
        r, g, b = 0.0, ((waveLength - 440) / (490 - 440)) ** 0.8, 1.0
    elif 490 <= waveLength <= 510:
        r, g, b = 0.0, 1.0, (-(waveLength - 510) / (510 - 490)) ** 0.8
    elif 510 <= waveLength <= 580:
        r, g, b = ((waveLength - 510) / (580 - 510)) ** 0.8, 1.0, 0.0
    elif 580 <= waveLength <= 645:
        r, g, b = 1.0, (-(waveLength - 645) / (645 - 580)) ** 0.8, 0.0
    elif 645 <= waveLength <= 780:
        attenuation = 0.3 + 0.7 * (750 - waveLength) / (750 - 645)
        r, g, b = 1.0 * attenuation, 0.0, 0.0
    else:
        r, g, b = 0.0, 0.0, 0.0
    return f'#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}'


class SinglePhotonDoubleSlitSimulator(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置主窗口属性
        self.setWindowTitle("单光子双缝干涉实验模拟")
        self.setGeometry(100, 100, 1600, 1000)

        # 创建主部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # 左侧布局：实验目的 + 计算公式 + 实验原理图
        left_layout = QVBoxLayout()
        left_layout.setSpacing(20)


        # 设置左侧布局的固定宽度
        left_widget = QWidget()
        left_widget.setFixedWidth(600)
        left_widget.setLayout(left_layout)

        main_layout.addWidget(left_widget)

        # 实验目的（标题）
        self.objectives_title = QLabel("实验目的")
        self.objectives_title.setAlignment(Qt.AlignCenter)
        self.objectives_title.setStyleSheet(
            "font-size: 28px; font-weight: bold; border: 2px solid #7f8c8d; padding: 10px; background-color: #b3cde0;")
        left_layout.addWidget(self.objectives_title)

        # 实验目的（内容）
        self.objectives_display = QLabel(
            "实验目的:\n1. 观察单光子双缝干涉现象\n2. 研究干涉条纹与参数的关系")
        self.objectives_display.setStyleSheet(
            "font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")
        left_layout.addWidget(self.objectives_display)

        # 计算公式（标题）
        self.formula_title = QLabel("使用的计算公式")
        self.formula_title.setAlignment(Qt.AlignCenter)
        self.formula_title.setStyleSheet(
            "font-size: 28px; font-weight: bold; border: 2px solid #7f8c8d; padding: 10px; background-color: #b3cde0;")
        left_layout.addWidget(self.formula_title)

        # 计算公式（内容）
        self.formula_display = QLabel(
            "计算公式: x = nλL/d\n其中 x 是屏幕上干涉条纹到中心的距离（米）\nn 是干涉条纹的级数\nλ是光的波长（米）\nL 是双缝到屏幕的距离（米）\nd 是双缝之间的间距（米）")
        self.formula_display.setStyleSheet(
            "font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")
        left_layout.addWidget(self.formula_display)

        # 实验原理图标签设置黑体
        self.principle_img_label = QLabel("实验原理图")
        self.principle_img_label.setAlignment(Qt.AlignCenter)
        self.principle_img_label.setStyleSheet(
            "font-size: 28px; font-weight: bold; border: 2px solid #7f8c8d; padding: 10px; background-color: #b3cde0;")
        self.principle_img_label.setFont(QFont("SimHei", 24))
        self.principle_img = QLabel()

        # 获取图片路径并设置固定大小
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, '单分子双缝干涉实验.png')
        pixmap = QPixmap(image_path).scaled(400, 500, Qt.KeepAspectRatio)
        self.principle_img.setPixmap(pixmap)
        self.principle_img.setAlignment(Qt.AlignCenter)

        left_layout.addWidget(self.principle_img_label)
        left_layout.addWidget(self.principle_img)

        # 添加原理演示按钮
        self.pe_demo_button = QPushButton("原理演示")
        self.pe_demo_button.setStyleSheet("font-size: 24px; background-color: #007bff; color: white;")
        left_layout.addWidget(self.pe_demo_button)

        # 中间布局：仿真结果图
        middle_layout = QVBoxLayout()
        middle_layout.setSpacing(10)
        main_layout.addLayout(middle_layout)

        # 仿真结果（标题）
        result_label = QLabel("仿真结果")
        result_label.setAlignment(Qt.AlignCenter)
        result_label.setStyleSheet(
            "font-size: 36px; font-weight: bold; border: 2px solid #7f8c8d; padding: 5px 10px; background-color: #b3cde0;")
        middle_layout.addWidget(result_label)

        # 修改子图布局：将两个图垂直排列，并调整上下之间的距离
        self.figures = [plt.figure(), plt.figure()]
        self.canvas1 = FigureCanvas(self.figures[0])
        self.canvas2 = FigureCanvas(self.figures[1])
        middle_layout.addWidget(self.canvas1)
        middle_layout.addWidget(self.canvas2)

        # 右侧布局：参数设置和保存区
        right_layout = QVBoxLayout()
        right_layout.setSpacing(20)

        # 设置初始固定宽度
        initial_right_width = 350
        right_widget = QWidget()
        right_widget.setFixedWidth(initial_right_width)
        right_widget.setLayout(right_layout)

        main_layout.addWidget(right_widget)

        # 参数布局
        param_layout = QGridLayout()
        param_layout.setHorizontalSpacing(20)
        param_layout.setVerticalSpacing(20)
        right_layout.addLayout(param_layout)

        # 缝间距输入
        slit_spacing_label = QLabel("缝间距 d(毫米):")
        slit_spacing_label.setStyleSheet(
            "font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")
        param_layout.addWidget(slit_spacing_label, 0, 0)
        self.slit_spacing_input = QLineEdit()
        self.slit_spacing_input.setStyleSheet(
            "font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")
        # 设置默认值为 2 毫米
        self.slit_spacing_input.setText("2")
        param_layout.addWidget(self.slit_spacing_input, 0, 1)

        # 屏幕距离输入
        screen_distance_label = QLabel("屏幕距离 L(米):")
        screen_distance_label.setStyleSheet(
            "font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")
        param_layout.addWidget(screen_distance_label, 1, 0)
        self.screen_distance_input = QLineEdit()
        self.screen_distance_input.setStyleSheet(
            "font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")
        # 设置默认值为 1 米
        self.screen_distance_input.setText("1")
        param_layout.addWidget(self.screen_distance_input, 1, 1)

        # 干涉条纹级数输入
        fringe_order_label = QLabel("干涉条纹级数 n:")
        fringe_order_label.setStyleSheet(
            "font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")
        param_layout.addWidget(fringe_order_label, 2, 0)
        self.fringe_order_input = QLineEdit()
        self.fringe_order_input.setStyleSheet(
            "font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")
        # 设置默认值为 1
        self.fringe_order_input.setText("1")
        param_layout.addWidget(self.fringe_order_input, 2, 1)

        # 光波长输入
        wavelength_label = QLabel("光波长 λ(纳米):")
        wavelength_label.setStyleSheet(
            "font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")
        param_layout.addWidget(wavelength_label, 3, 0)
        self.wavelength_input = QLineEdit()
        self.wavelength_input.setStyleSheet(
            "font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")
        # 设置默认值为 450 纳米
        self.wavelength_input.setText("450")
        param_layout.addWidget(self.wavelength_input, 3, 1)

        # 计算结果按钮
        self.calculate_button = QPushButton("计算结果")
        self.calculate_button.setStyleSheet("font-size: 24px; background-color: #007bff; color: white;")
        self.calculate_button.clicked.connect(self.calculate_results)
        param_layout.addWidget(self.calculate_button, 4, 0, 1, 2)

        # 保存区：保存图像和实验数据
        save_layout = QVBoxLayout()
        save_layout.setSpacing(20)
        right_layout.addLayout(save_layout)

        self.save_img_button = QPushButton("保存图像")
        self.save_img_button.setStyleSheet("font-size: 24px; background-color: #007bff; color: white;")
        self.save_img_button.clicked.connect(self.save_image)
        save_layout.addWidget(self.save_img_button)


        # 退出按钮
        self.quit_button = QPushButton("退出")
        self.quit_button.setStyleSheet("font-size: 24px; background-color: #dc3545; color: white;")
        self.quit_button.clicked.connect(self.close)
        save_layout.addWidget(self.quit_button)

        # 持有动画对象，防止被回收
        self.ani = None



    def calculate_results(self):
        try:
            slit_spacing = float(self.slit_spacing_input.text()) if self.slit_spacing_input.text() else 0.1
            screen_distance = float(self.screen_distance_input.text()) if self.screen_distance_input.text() else 1
            fringe_order = int(self.fringe_order_input.text()) if self.fringe_order_input.text() else 0
            wavelength = float(self.wavelength_input.text()) if self.wavelength_input.text() else 500

            # 将波长从纳米转换为米
            wavelength_m = wavelength * 1e-9
            # 将狭缝宽度从毫米转换为米
            d_slit_m = slit_spacing * 1e-3

            def draw(figures, wavelength, d_slit, d_screen):
                ym = 5.0 * wavelength * d_screen / d_slit
                distance = ym / 200.0
                ys = np.arange(-ym, ym, distance)
                len_dis = len(ys)
                B = [([0.0] * len_dis) for _ in range(len_dis)]
                Br = [([0.0] * len_dis) for _ in range(len_dis)]
                N = 255.0
                for i in range(0, len_dis):
                    r1 = math.sqrt((ys[i] - d_slit / 2) ** 2 + d_screen ** 2)
                    r2 = math.sqrt((ys[i] + d_slit / 2) ** 2 + d_screen ** 2)
                    phi = 2.0 * math.pi * (r2 - r1) / wavelength
                    temp = 4.0 * math.cos(phi / 2) ** 2
                    for j in range(0, len_dis):
                        B[i][j] = temp
                        Br[i][j] = B[i][j] / 4.0 * N

                # 清除之前的图形
                figures[0].clear()
                figures[1].clear()

                fig_1 = figures[0].add_subplot(111)
                # 根据新的波长生成新的颜色映射
                cmap = LinearSegmentedColormap.from_list('custom_cmap',
                                                         [(0, '#000000'), (1, wavelength2Hex(wavelength * 10 ** 9))])
                # 设置绘图参数
                config = {
                    "font.family": 'sans-serif',
                    "font.size": 12,
                    "mathtext.fontset": 'stix',
                    "font.serif": ['Times New Roman'],
                    "font.sans-serif": ['SimSun'],
                }
                plt.rcParams.update(config)
                plt.rcParams['axes.unicode_minus'] = False

                im = fig_1.imshow(Br, extent=[-ym, ym, -ym, ym], cmap=cmap, aspect='auto')
                figures[0].colorbar(im, orientation='vertical')

                fig_1.set_xlabel('x (m)')
                fig_1.set_ylabel('y (m)')


                # 绘制光强分布曲线
                fig_2 = figures[1].add_subplot(111)
                fig_2.plot(B, ys, 'k')
                fig_2.set_xlabel('I')
                fig_2.set_ylabel('x (m)')
                for label in fig_2.get_xticklabels():
                    label.set_fontname('Times New Roman')
                    label.set_fontsize(config['font.size'])
                for label in fig_2.get_yticklabels():
                    label.set_fontname('Times New Roman')
                    label.set_fontsize(config['font.size'])

            draw(self.figures, wavelength_m, d_slit_m, screen_distance)


            # 通过 canvas 刷新图像
            self.canvas1.draw()
            self.canvas2.draw()
        except ValueError:
            # 如果输入无效，弹出提示信息
            self.show_message("输入有误，请检查输入的参数是否正确。")



    # 保存图像方法
    def save_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "保存图像", "", "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)", options=options)
        if file_name:
            self.canvas1.figure.savefig(file_name + '_fig1.png')
            self.canvas2.figure.savefig(file_name + '_fig2.png')


    def show_message(self, message):
        # 弹出提示信息框
        msg_box = QMessageBox()
        msg_box.setText(message)
        msg_box.exec_()


# 应用程序启动
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SinglePhotonDoubleSlitSimulator()
    window.show()
    sys.exit(app.exec_())