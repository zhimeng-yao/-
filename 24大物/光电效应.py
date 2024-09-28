import sys
import numpy as np
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QComboBox, QGridLayout, QFileDialog, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.animation import FuncAnimation

# 载入黑体字体以支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置默认字体为黑体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号 '-' 显示为方块的问题

# 常量定义
h = 6.626e-34  # 普朗克常数 (J·s)
e = 1.602e-19  # 电子电荷 (C)
c = 3.0e8      # 光速 (m/s)
m = 9.109e-31  # 电子质量 (kg)

# 金属逸出功数据
work_function_data = {"铜": 4.7, "铝": 4.2, "金": 5.1, "银": 4.26, "锌": 4.33}

class PhotoelectricEffectSimulator(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置主窗口属性
        self.setWindowTitle("光电效应模拟仿真")
        self.setGeometry(100, 100, 1400, 800)

        # 创建主部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)  # 主布局为水平布局，分为三栏

        # 左侧布局：实验目的 + 计算公式 + 实验原理图
        left_layout = QVBoxLayout()
        left_layout.setSpacing(20)  # 设置组件之间的间距
        main_layout.addLayout(left_layout)

        # 实验目的（标题）
        self.objectives_title = QLabel("实验目的")
        self.objectives_title.setAlignment(Qt.AlignCenter)
        self.objectives_title.setStyleSheet("font-size: 28px; font-weight: bold; border: 2px solid #7f8c8d; padding: 10px; background-color: #b3cde0;")
        left_layout.addWidget(self.objectives_title)

        # 实验目的（内容）
        self.objectives_display = QLabel("1. 了解光电效应的过程\n2. 研究最大初动能和波长的关系\n3. 探索电流与光强的关系")
        self.objectives_display.setStyleSheet("font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")  # 添加白色底色
        left_layout.addWidget(self.objectives_display)

        # 计算公式（标题）
        self.formula_title = QLabel("使用的计算公式")
        self.formula_title.setAlignment(Qt.AlignCenter)
        self.formula_title.setStyleSheet("font-size: 28px; font-weight: bold; border: 2px solid #7f8c8d; padding: 10px; background-color: #b3cde0;")
        left_layout.addWidget(self.formula_title)

        # 计算公式（内容）
        self.formula_display = QLabel("hv = 1/2 mv^2 + W\nI = e · n · A · 光强")
        self.formula_display.setStyleSheet("font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")  # 添加白色底色
        left_layout.addWidget(self.formula_display)

        # 实验原理图标签设置黑体
        self.principle_img_label = QLabel("实验原理图")
        self.principle_img_label.setAlignment(Qt.AlignCenter)
        self.principle_img_label.setStyleSheet("font-size: 28px; font-weight: bold; border: 2px solid #7f8c8d; padding: 10px; background-color: #b3cde0;")
        self.principle_img_label.setFont(QFont("SimHei", 18))  # 设置黑体字体
        self.principle_img = QLabel()

        # 获取图片路径并设置固定大小
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, '光电效应.png')
        pixmap = QPixmap(image_path).scaled(400, 500, Qt.KeepAspectRatio)  # 设置图片大小
        self.principle_img.setPixmap(pixmap)
        self.principle_img.setAlignment(Qt.AlignCenter)

        left_layout.addWidget(self.principle_img_label)
        left_layout.addWidget(self.principle_img)

        # 添加原理演示按钮
        self.demo_button = QPushButton("原理演示")
        self.demo_button.setStyleSheet("font-size: 24px; background-color: #007bff; color: white;")  # 设置按钮样式
        left_layout.addWidget(self.demo_button)

        # 中间布局：仿真结果图
        middle_layout = QVBoxLayout()
        middle_layout.setSpacing(10)  # 减少“仿真结果”与图形之间的间距
        main_layout.addLayout(middle_layout)

        # 仿真结果（标题）
        result_label = QLabel("仿真结果")
        result_label.setAlignment(Qt.AlignCenter)
        result_label.setStyleSheet("font-size: 24px; font-weight: bold; border: 2px solid #7f8c8d; padding: 5px 10px; background-color: #b3cde0;")
        middle_layout.addWidget(result_label)

        # 修改子图布局：增加图形高度，使其与左侧的“使用的计算公式”框框匹配
        self.figure, self.axs = plt.subplots(2, 1, figsize=(10, 12))  # 2 行 1 列的布局，并将高度调整为12
        self.figure.subplots_adjust(hspace=0.5)  # 调整上下图之间的距离（hspace参数设置图形的上下间距）
        self.canvas = FigureCanvas(self.figure)
        middle_layout.addWidget(self.canvas)

        # 右侧布局：参数设置（材料 + 计算结果）和保存区
        right_layout = QVBoxLayout()
        right_layout.setSpacing(20)  # 增加间距使界面更整齐
        main_layout.addLayout(right_layout)

        # 参数布局
        param_layout = QGridLayout()
        param_layout.setHorizontalSpacing(20)  # 设置横向间距
        param_layout.setVerticalSpacing(20)    # 设置纵向间距
        right_layout.addLayout(param_layout)

        # 金属材料选择
        material_label = QLabel("金属材料:")
        material_label.setStyleSheet("font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")  # 添加白色背景框
        param_layout.addWidget(material_label, 0, 0)
        self.material_combo = QComboBox()
        self.material_combo.addItems(work_function_data.keys())
        self.material_combo.setStyleSheet("font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")  # 添加白色背景框
        param_layout.addWidget(self.material_combo, 0, 1)

        # 光电子数输入
        photon_number_label = QLabel("光电子数 (n):")
        photon_number_label.setStyleSheet("font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")  # 添加白色背景框
        param_layout.addWidget(photon_number_label, 1, 0)
        self.photon_number_input = QLineEdit()
        self.photon_number_input.setStyleSheet("font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")  # 添加白色背景框
        param_layout.addWidget(self.photon_number_input, 1, 1)

        # 照射面积输入
        area_label = QLabel("照射面积 (m^2):")
        area_label.setStyleSheet("font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")  # 添加白色背景框
        param_layout.addWidget(area_label, 2, 0)
        self.area_input = QLineEdit()
        self.area_input.setStyleSheet("font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")  # 添加白色背景框
        param_layout.addWidget(self.area_input, 2, 1)

        # 计算结果按钮
        self.calculate_button = QPushButton("计算结果")
        self.calculate_button.setStyleSheet("font-size: 24px; background-color: #007bff; color: white;")  # 设置按钮颜色
        self.calculate_button.clicked.connect(self.calculate_results)
        param_layout.addWidget(self.calculate_button, 3, 0, 1, 2)

        # 计算结果显示
        self.result_display = QLabel("结果显示:\n最大动能：\n电流：")
        self.result_display.setStyleSheet("font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")  # 添加白色背景框
        right_layout.addWidget(self.result_display)

        # 保存区：保存图像和实验数据
        save_layout = QVBoxLayout()
        save_layout.setSpacing(20)
        right_layout.addLayout(save_layout)

        self.save_img_button = QPushButton("保存图像")
        self.save_img_button.setStyleSheet("font-size: 24px; background-color: #007bff; color: white;")  # 设置按钮颜色
        self.save_img_button.clicked.connect(self.save_image)
        save_layout.addWidget(self.save_img_button)

        self.save_data_button = QPushButton("保存实验数据")
        self.save_data_button.setStyleSheet("font-size: 24px; background-color: #007bff; color: white;")  # 设置按钮颜色
        self.save_data_button.clicked.connect(self.save_data)
        save_layout.addWidget(self.save_data_button)

        # 退出按钮
        self.quit_button = QPushButton("退出")
        self.quit_button.setStyleSheet("font-size: 24px; background-color: #dc3545; color: white;")  # 设置按钮颜色
        self.quit_button.clicked.connect(self.close)  # 连接到关闭窗口的方法
        save_layout.addWidget(self.quit_button)  # 将退出按钮添加到保存布局下方

        # 持有动画对象，防止被回收
        self.ani = None

    def calculate_results(self):
        material = self.material_combo.currentText()

        work_function = work_function_data.get(material, 4.7)
        work_function_J = work_function * e

        # 获取用户输入的光电子数和照射面积
        photon_number = float(self.photon_number_input.text()) if self.photon_number_input.text() else 0
        area = float(self.area_input.text()) if self.area_input.text() else 0

        # 使用默认的频率范围
        self.frequency_range = np.linspace(1e15, 10e15, 300)  # 调整频率范围
        photon_energy = h * self.frequency_range

        # 使用光强的范围
        self.light_intensity_range = np.linspace(1, 10000, 50)  # 光强从1到100
        self.current = e * photon_number * area * self.light_intensity_range  # 根据新的公式计算电流

        # 计算最大初动能
        self.kinetic_energy_max = np.maximum(photon_energy - work_function_J, 0)

        # 更新结果显示
        self.result_display.setText(f"结果显示:\n光电子数: {photon_number}\n照射面积: {area} m^2\n最大动能：{self.kinetic_energy_max[-1]:.2e} J\n电流：{self.current[-1]:.2e} A")

        # 更新图形
        self.animate_simulation(self.frequency_range, self.kinetic_energy_max, self.light_intensity_range, self.current)

    def animate_simulation(self, frequency_range, kinetic_energy_max, light_intensity_range, current):
        self.axs[0].clear()
        self.axs[1].clear()

        # 动态更新函数
        def update(frame):
            # 最大初动能与频率的关系
            self.axs[0].set_title("最大初动能与频率的关系", fontsize=20)  # 放大图形上的文字
            self.axs[0].set_xlabel("频率 (Hz)", fontsize=18)  # 放大文字
            self.axs[0].set_ylabel("最大初动能 (J)", fontsize=18)  # 放大文字
            self.axs[0].plot(frequency_range[:frame], kinetic_energy_max[:frame], color='b')

            # 电流与光强的关系
            self.axs[1].set_title("电流与光强的关系", fontsize=20)  # 放大图形上的文字
            self.axs[1].set_xlabel("光强", fontsize=18)  # 放大文字
            self.axs[1].set_ylabel("电流 (A)", fontsize=18)  # 放大文字
            self.axs[1].plot(light_intensity_range[:frame], current[:frame], 'r')

            # 通过 canvas 刷新图像
            self.canvas.draw()

        # 创建动画并保持引用
        self.ani = FuncAnimation(self.figure, update, frames=len(frequency_range), interval=50, repeat=False)

        # 确保动画显示
        self.canvas.draw()

    # 保存图像方法
    def save_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "保存图像", "", "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)", options=options)
        if file_name:
            self.figure.savefig(file_name)

    # 保存实验数据方法
    def save_data(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "保存实验数据", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                file.write("频率(Hz), 最大初动能(J), 光强, 电流(A)\n")
                for i in range(len(self.kinetic_energy_max)):
                    file.write(f"{self.frequency_range[i]:.2e}, {self.kinetic_energy_max[i]:.2e}, {self.light_intensity_range[i]:.2e}, {self.current[i]:.2e}\n")


# 应用程序启动
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PhotoelectricEffectSimulator()
    window.show()
    sys.exit(app.exec_())