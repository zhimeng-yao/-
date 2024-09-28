import sys
import os
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QComboBox, QGridLayout, QFileDialog, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget  # 修复导入
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# 载入黑体字体以支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置默认字体为黑体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号 '-' 显示为方块的问题

# 常量定义
h_true = 6.626e-34  # 普朗克常量 (J·s)
e = 1.602e-19       # 电子电荷 (C)
c = 3.0e8           # 光速 (m/s)

# 金属逸出功数据 (单位: eV)
work_function_data = {"铜": 4.7, "铝": 4.2, "金": 5.1, "银": 4.26, "锌": 4.33}

class PlanckConstantSimulator(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置主窗口属性
        self.setWindowTitle("光电效应测量普朗克常量")
        self.setGeometry(100, 100, 1600, 900)

        # 创建主部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # 设置左中右各占三分之一的宽度
        left_widget = QWidget()
        middle_widget = QWidget()
        right_widget = QWidget()
        left_widget.setMaximumWidth(self.width() // 3)
        middle_widget.setMaximumWidth(self.width() // 3)
        right_widget.setMaximumWidth(self.width() // 3)

        main_layout.addWidget(left_widget)
        main_layout.addWidget(middle_widget)
        main_layout.addWidget(right_widget)

        # 左侧布局：实验目的 + 计算公式 + 原理图
        left_layout = QVBoxLayout(left_widget)
        left_layout.setSpacing(20)

        # 实验目的板块
        self.objectives_title = QLabel("实验目的")
        self.objectives_title.setAlignment(Qt.AlignCenter)
        self.objectives_title.setStyleSheet("font-size: 28px; font-weight: bold; border: 2px solid #7f8c8d; padding: 10px; background-color: #b3cde0;")
        left_layout.addWidget(self.objectives_title)

        self.objectives_display = QLabel("1. 测量普朗克常量\n2. 研究遏止电压和光频率的线性关系\n3. 探索不同材料的逸出功对实验结果的影响")
        self.objectives_display.setStyleSheet("font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")
        left_layout.addWidget(self.objectives_display)

        # 计算公式板块
        self.formula_title = QLabel("计算公式")
        self.formula_title.setAlignment(Qt.AlignCenter)
        self.formula_title.setStyleSheet("font-size: 28px; font-weight: bold; border: 2px solid #7f8c8d; padding: 10px; background-color: #b3cde0;")
        left_layout.addWidget(self.formula_title)

        self.formula_display = QLabel("E_k = hν - W\nV_0 = (hν - W)/e")
        self.formula_display.setStyleSheet("font-size: 24px; border: 2px solid #7f8c8d; padding: 10px; background-color: white;")
        left_layout.addWidget(self.formula_display)

        # 实验原理图板块
        self.principle_img_title = QLabel("实验原理图")
        self.principle_img_title.setAlignment(Qt.AlignCenter)
        self.principle_img_title.setStyleSheet("font-size: 28px; font-weight: bold; border: 2px solid #7f8c8d; padding: 10px; background-color: #b3cde0;")
        left_layout.addWidget(self.principle_img_title)

        self.principle_img = QLabel()

        # 加载示意图
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, '光电效应.png')
        pixmap = QPixmap(image_path).scaled(400, 300, Qt.KeepAspectRatio)
        self.principle_img.setPixmap(pixmap)
        self.principle_img.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(self.principle_img)

        # 原理演示按钮
        self.demo_button = QPushButton("原理演示")
        self.demo_button.setStyleSheet("font-size: 24px; background-color: #007bff; color: white;")
        self.demo_button.clicked.connect(self.play_video)  # 连接播放视频的函数
        left_layout.addWidget(self.demo_button)

        # 中间布局：实验结果可视化，仿真结果图高到与“计算公式”板块齐高
        middle_layout = QVBoxLayout(middle_widget)
        middle_layout.setSpacing(10)

        result_label = QLabel("实验结果")
        result_label.setAlignment(Qt.AlignCenter)
        result_label.setStyleSheet("font-size: 24px; font-weight: bold; border: 2px solid #7f8c8d; padding: 5px 10px; background-color: #b3cde0;")
        middle_layout.addWidget(result_label)

        # 增加仿真图高度
        self.figure, self.axs = plt.subplots(1, 1, figsize=(6, 10))  # 调整图像尺寸，使仿真结果图更高
        self.canvas = FigureCanvas(self.figure)
        middle_layout.addWidget(self.canvas)

        # 右侧布局：参数输入区 + 数据区 + 处理区
        right_layout = QVBoxLayout(right_widget)
        right_layout.setSpacing(20)

        # 参数输入区
        param_layout = QVBoxLayout()
        right_layout.addLayout(param_layout)

        param_title = QLabel("参数输入区")
        param_title.setAlignment(Qt.AlignCenter)
        param_title.setStyleSheet("font-size: 24px; font-weight: bold; border: 2px solid #7f8c8d; padding: 10px; background-color: #b3cde0;")
        param_layout.addWidget(param_title)

        grid_layout = QGridLayout()
        param_layout.addLayout(grid_layout)

        # 最低光频率输入
        self.min_freq_label = QLabel("最低光频率 (THz):")
        self.min_freq_label.setStyleSheet("font-size: 18px; padding: 10px;")
        grid_layout.addWidget(self.min_freq_label, 0, 0)
        self.min_freq_input = QLineEdit()
        self.min_freq_input.setStyleSheet("font-size: 18px; padding: 10px;")
        grid_layout.addWidget(self.min_freq_input, 0, 1)

        # 最高光频率输入
        self.max_freq_label = QLabel("最高光频率 (THz):")
        self.max_freq_label.setStyleSheet("font-size: 18px; padding: 10px;")
        grid_layout.addWidget(self.max_freq_label, 1, 0)
        self.max_freq_input = QLineEdit()
        self.max_freq_input.setStyleSheet("font-size: 18px; padding: 10px;")
        grid_layout.addWidget(self.max_freq_input, 1, 1)

        # 频率间距
        self.interval_label = QLabel("间距（点数）:")
        self.interval_label.setStyleSheet("font-size: 18px; padding: 10px;")
        grid_layout.addWidget(self.interval_label, 2, 0)
        self.interval_input = QLineEdit()
        self.interval_input.setStyleSheet("font-size: 18px; padding: 10px;")
        grid_layout.addWidget(self.interval_input, 2, 1)

        # 金属种类选择
        self.metal_label = QLabel("金属种类:")
        self.metal_label.setStyleSheet("font-size: 18px; padding: 10px;")
        grid_layout.addWidget(self.metal_label, 3, 0)
        self.metal_combo = QComboBox()
        self.metal_combo.addItems(work_function_data.keys())  # 加入金属种类
        self.metal_combo.setStyleSheet("font-size: 18px; padding: 10px;")
        grid_layout.addWidget(self.metal_combo, 3, 1)

        # 数据区：表格
        data_table_layout = QVBoxLayout()
        right_layout.addLayout(data_table_layout)

        data_table_title = QLabel("数据区")
        data_table_title.setAlignment(Qt.AlignCenter)
        data_table_title.setStyleSheet("font-size: 24px; font-weight: bold; border: 2px solid #7f8c8d; padding: 10px; background-color: #b3cde0;")
        data_table_layout.addWidget(data_table_title)

        # 初始化数据表格时不预先设置行数
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(2)
        self.data_table.setHorizontalHeaderLabels(["光频率 (THz)", "遏止电压 (V)"])
        data_table_layout.addWidget(self.data_table)

        # 处理区：计算、清除、保存按钮
        process_layout = QVBoxLayout()
        right_layout.addLayout(process_layout)

        process_title = QLabel("处理区")
        process_title.setAlignment(Qt.AlignCenter)
        process_title.setStyleSheet("font-size: 24px; font-weight: bold; border: 2px solid #7f8c8d; padding: 10px; background-color: #b3cde0;")
        process_layout.addWidget(process_title)

        self.calculate_button = QPushButton("计算结果")
        self.calculate_button.setStyleSheet("font-size: 24px; background-color: #007bff; color: white;")
        self.calculate_button.clicked.connect(self.calculate_results)
        process_layout.addWidget(self.calculate_button)

        self.clear_button = QPushButton("清除数据")
        self.clear_button.setStyleSheet("font-size: 24px; background-color: #dc3545; color: white;")
        self.clear_button.clicked.connect(self.clear_data)
        process_layout.addWidget(self.clear_button)

        self.save_img_button = QPushButton("保存图像")
        self.save_img_button.setStyleSheet("font-size: 24px; background-color: #007bff; color: white;")
        self.save_img_button.clicked.connect(self.save_image)
        process_layout.addWidget(self.save_img_button)

        # 添加保存数据按钮
        self.save_data_button = QPushButton("保存数据")
        self.save_data_button.setStyleSheet("font-size: 24px; background-color: #007bff; color: white;")
        self.save_data_button.clicked.connect(self.save_data)
        process_layout.addWidget(self.save_data_button)

        # 数据存储
        self.frequency_data = []
        self.stopping_voltage_data = []

    def calculate_results(self):
        # 获取输入的最低频率、最高频率和间距
        try:
            min_freq = float(self.min_freq_input.text())
            max_freq = float(self.max_freq_input.text())
            interval = int(self.interval_input.text())
        except ValueError:
            QMessageBox.warning(self, "输入错误", "请确保频率和间距的输入值有效！")
            return

        # 获取用户选择的金属种类
        selected_metal = self.metal_combo.currentText()
        work_function_eV = work_function_data[selected_metal]  # 根据选择的金属种类获取逸出功
        work_function_J = work_function_eV * e

        # 生成频率范围
        frequencies = np.linspace(min_freq, max_freq, interval)

        # 清空现有数据，以便新数据从第一行开始
        self.data_table.setRowCount(0)  # 确保从第一行开始

        for freq_THz in frequencies:
            frequency_Hz = freq_THz * 1e12  # 转换为 Hz

            # 计算遏止电压
            stopping_voltage = (h_true * frequency_Hz - work_function_J) / e

            # 在表格中显示结果
            row_position = self.data_table.rowCount()
            self.data_table.insertRow(row_position)
            self.data_table.setItem(row_position, 0, QTableWidgetItem(f"{freq_THz:.2f}"))
            self.data_table.setItem(row_position, 1, QTableWidgetItem(f"{stopping_voltage:.2f}"))

            # 保存数据
            self.frequency_data.append(freq_THz)
            self.stopping_voltage_data.append(stopping_voltage)

        # 更新实验结果图形
        self.update_plot()

    def update_plot(self):
        self.axs.clear()

        # 绘制频率 vs 遏止电压的关系，只保留数据点，不显示拟合曲线
        self.axs.scatter(self.frequency_data, self.stopping_voltage_data, color='b', label="实验数据")
        self.axs.set_title("频率与遏止电压的关系", fontsize=20)
        self.axs.set_xlabel("频率 (THz)", fontsize=18)
        self.axs.set_ylabel("遏止电压 (V)", fontsize=18)

        self.axs.legend()
        self.canvas.draw()

    def clear_data(self):
        self.data_table.clearContents()
        self.frequency_data.clear()
        self.stopping_voltage_data.clear()
        self.axs.clear()
        self.canvas.draw()

    def save_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "保存图像", "", "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)", options=options)
        if file_name:
            self.figure.savefig(file_name)

    # 保存数据的实现
    def save_data(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "保存数据", "", "Text Files (*.txt);;CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                file.write("光频率 (THz), 遏止电压 (V)\n")
                for freq, voltage in zip(self.frequency_data, self.stopping_voltage_data):
                    file.write(f"{freq:.2f}, {voltage:.2f}\n")

    # 播放视频的功能
    def play_video(self):
        # 创建一个新窗口用于播放视频
        self.video_window = QWidget()
        self.video_window.setWindowTitle("原理演示视频")
        self.video_window.setGeometry(300, 200, 800, 600)

        # 创建视频播放器和视频控件
        video_layout = QVBoxLayout()
        self.video_widget = QVideoWidget()
        video_layout.addWidget(self.video_widget)
        self.video_window.setLayout(video_layout)

        # 创建媒体播放器
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_widget)

        # 加载视频文件
        video_path = os.path.join(os.path.dirname(__file__), '光电效应原理动态.mp4')  # 确保路径正确
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(video_path)))

        # 显示视频窗口并播放
        self.video_window.show()
        self.media_player.play()

# 应用程序启动
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlanckConstantSimulator()
    window.show()
    sys.exit(app.exec_())