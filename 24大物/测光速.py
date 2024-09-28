
import sys
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
                             QLabel, QPushButton, QComboBox, QLineEdit, QSlider, QTableWidget,
                             QTableWidgetItem, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtWidgets import QHeaderView
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.colors import ListedColormap

class MichelsonInterferenceApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("迈克尔逊干涉仪光速测量仿真")
        self.setMinimumSize(1600, 900)

        # 设置中央Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 设置背景图样式
        self.set_background_image()

        # 添加板块1：实验步骤说明
        self.add_experiment_steps(main_layout)

        # 实验参数、图像与结果部分
        experiment_layout = QHBoxLayout()
        main_layout.addLayout(experiment_layout)

        # 左侧布局
        left_layout = QVBoxLayout()
        experiment_layout.addLayout(left_layout)

        # 实验目的与实验参数
        self.add_experiment_purpose(left_layout)

        # 中间布局：显示仿真图像和光速公式
        middle_layout = QVBoxLayout()
        experiment_layout.addLayout(middle_layout)

        self.add_simulation_area(middle_layout)
        self.add_formula_section(middle_layout)  # 添加光速计算公式

        # 右侧布局：实验结果展示
        right_layout = QVBoxLayout()
        experiment_layout.addLayout(right_layout)

        self.add_experiment_result_section(right_layout)

        # 实验总结与数据导出板块
        self.add_experiment_summary(main_layout)

        self.init_parameters()
        self.update_simulation()

    def set_background_image(self):
        # 设置背景图片
        palette = QPalette()
        pixmap = QPixmap("仿真平台.jpg")  # 替换为你的图片路径
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.setPalette(palette)

    def add_experiment_steps(self, layout):
        steps_label = QLabel("实验步骤：")
        steps_label.setStyleSheet("font-size: 22px; font-weight: bold; padding: 10px; color: white; background-color: #1E90FF; border-radius: 5px;")
        layout.addWidget(steps_label)

        steps_content = QLabel("1. 选择入射光波长。\n2. 设置光程差和镜子移动距离。\n3. 点击更新仿真并计算光速。\n4. 导出实验结果并分析。")
        steps_content.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px; background-color: rgba(255, 255, 255, 0.9); color: black; border-radius: 5px;")
        layout.addWidget(steps_content)

    def add_experiment_purpose(self, layout):
        objectives_label = QLabel("实验目的：")
        objectives_label.setStyleSheet("font-size: 20px; font-weight: bold; border: 2px solid #1E90FF; padding: 10px; background-color: #4682B4; border-radius: 5px; color: white;")
        layout.addWidget(objectives_label)
        objectives_content_label = QLabel("通过迈克尔逊干涉仪测量光速。")
        objectives_content_label.setStyleSheet("font-size: 18px; font-weight: bold; border: 2px solid #1E90FF; padding: 10px; background-color: rgba(255, 255, 255, 0.9); color: black; border-radius: 5px;")
        layout.addWidget(objectives_content_label)

        parameters_label = QLabel("实验参数：")
        parameters_label.setStyleSheet("font-size: 20px; font-weight: bold; border: 2px solid #1E90FF; padding: 10px; background-color: #4682B4; border-radius: 5px; color: white;")
        layout.addWidget(parameters_label)

        wavelength_label = QLabel("入射光线波长 (nm):")
        wavelength_label.setStyleSheet("font-size: 18px; font-weight: bold; border: 2px solid #1E90FF; padding: 10px; background-color: rgba(255, 255, 255, 0.9); color: black; border-radius: 5px;")
        layout.addWidget(wavelength_label)
        self.wavelength_selector = QComboBox()
        self.wavelength_selector.addItems(["632.8", "532", "488"])
        self.wavelength_selector.setStyleSheet("font-size: 18px; font-weight: bold; border: 2px solid #1E90FF; padding: 10px; background-color: rgba(255, 255, 255, 0.9); color: black; border-radius: 5px;")
        layout.addWidget(self.wavelength_selector)

        distance_label = QLabel("光程差 (mm):")
        distance_label.setStyleSheet("font-size: 18px; font-weight: bold; border: 2px solid #1E90FF; padding: 10px; background-color: rgba(255, 255, 255, 0.9); color: black; border-radius: 5px;")
        layout.addWidget(distance_label)
        self.distance_input = QLineEdit()
        self.distance_input.setText("10")  # 默认光程差
        self.distance_input.setStyleSheet("font-size: 18px; font-weight: bold; border: 2px solid #1E90FF; padding: 10px; background-color: rgba(255, 255, 255, 0.9); color: black; border-radius: 5px;")
        layout.addWidget(self.distance_input)

        mirror_label = QLabel("镜子移动距离 (μm):")
        mirror_label.setStyleSheet("font-size: 18px; font-weight: bold; border: 2px solid #1E90FF; padding: 10px; background-color: rgba(255, 255, 255, 0.9); color: black; border-radius: 5px;")
        layout.addWidget(mirror_label)
        self.mirror_input = QLineEdit()
        self.mirror_input.setText("5")  # 默认镜子移动距离
        self.mirror_input.setStyleSheet("font-size: 18px; font-weight: bold; border: 2px solid #1E90FF; padding: 10px; background-color: rgba(255, 255, 255, 0.9); color: black; border-radius: 5px;")
        layout.addWidget(self.mirror_input)

    def add_simulation_area(self, layout):
        simulation_label = QLabel("仿真图像：")
        simulation_label.setStyleSheet("font-size: 20px; font-weight: bold; border: 2px solid #1E90FF; padding: 10px; background-color: #4682B4; border-radius: 5px; color: white;")
        layout.addWidget(simulation_label)

        self.figure = plt.figure(figsize=(12, 12))  # 调整图像显示区域的大小
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.current_ring_label = QLabel("当前环数：0")
        self.current_ring_label.setStyleSheet("font-size: 18px; font-weight: bold; border: 2px solid #1E90FF; padding: 10px; background-color: rgba(255, 255, 255, 0.9); color: black; border-radius: 5px;")
        layout.addWidget(self.current_ring_label)

        self.mirror_m2_position_label = QLabel("动镜 M2 位置：")
        self.mirror_m2_position_label.setStyleSheet("font-size: 18px; font-weight: bold; border: 2px solid #1E90FF; padding: 10px; background-color: rgba(255, 255, 255, 0.9); color: black; border-radius: 5px;")
        layout.addWidget(self.mirror_m2_position_label)
        self.mirror_m2_position_display = QLineEdit()
        layout.addWidget(self.mirror_m2_position_display)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(50)
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal { background-color: #CCCCCC; height: 10px; }
            QSlider::handle:horizontal { background-color: #2980b9; width: 20px; border-radius: 5px; }
            QSlider::handle:hover { background-color: #1abc9c; }
        """)
        self.slider.valueChanged.connect(self.update_simulation)
        layout.addWidget(self.slider)

    def add_formula_section(self, layout):
        formula_label = QLabel("光速计算公式：")
        formula_label.setStyleSheet("font-size: 20px; font-weight: bold; border: 2px solid #1E90FF; padding: 10px; background-color: #4682B4; border-radius: 5px; color: white;")
        layout.addWidget(formula_label)

        formula_content = QLabel("光速 c = 2 * d / t\n其中：\n d = 光程差 (m)\n t = 光经过距离的时间 (s)")
        formula_content.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px; background-color: rgba(255, 255, 255, 0.9); color: black; border-radius: 5px;")
        layout.addWidget(formula_content)

    def add_experiment_result_section(self, layout):
        results_label = QLabel("实验记录和光速：")
        results_label.setStyleSheet("font-size: 20px; font-weight: bold; border: 2px solid #1E90FF; padding: 10px; background-color: #4682B4; border-radius: 5px; color: white;")
        layout.addWidget(results_label)

        # 设置实验记录表格，调整列宽，使所有数据都能显示在视图中
        self.data_table = QTableWidget(20, 3)
        self.data_table.setHorizontalHeaderLabels(["光程差 (mm)", "条纹数 N", "光速 (m/s)"])
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)  # 自动调整列宽
        self.data_table.setStyleSheet("font-size: 16px; font-weight: bold; border-radius: 5px;")
        layout.addWidget(self.data_table)

        update_data_button = QPushButton("更新实验数据并计算光速")
        update_data_button.setStyleSheet("""
            QPushButton {
                font-size: 18px; font-weight: bold; background-color: #2980b9; color: white; padding: 10px; border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1abc9c;
            }
        """)
        update_data_button.clicked.connect(self.calculate_and_display_result)
        layout.addWidget(update_data_button)

    def add_experiment_summary(self, layout):
        summary_label = QLabel("实验总结：")
        summary_label.setStyleSheet("font-size: 20px; font-weight: bold; border: 2px solid #1E90FF; padding: 10px; background-color: #4682B4; border-radius: 5px; color: white;")
        layout.addWidget(summary_label)

        self.summary_text = QLabel("当前实验无总结数据。")
        self.summary_text.setStyleSheet("font-size: 18px; font-weight: bold; border: 2px solid #1E90FF; padding: 10px; background-color: rgba(255, 255, 255, 0.9); color: black; border-radius: 5px;")
        layout.addWidget(self.summary_text)

        export_data_button = QPushButton("导出实验数据")
        export_data_button.setStyleSheet("""
            QPushButton {
                font-size: 18px; font-weight: bold; background-color: #27ae60; color: white; padding: 10px; border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        export_data_button.clicked.connect(self.export_data)
        layout.addWidget(export_data_button)

    def export_data(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "保存实验数据", "", "CSV Files (*.csv);;All Files (*)")
        if file_name:
            with open(file_name, 'w') as f:
                f.write("光程差 (mm), 条纹数 N, 光速 (m/s)\n")
                for row in range(self.row):  # 只导出已生成的数据行
                    distance = self.data_table.item(row, 0).text() if self.data_table.item(row, 0) else ""
                    fringe_number = self.data_table.item(row, 1).text() if self.data_table.item(row, 1) else ""
                    light_speed = self.data_table.item(row, 2).text() if self.data_table.item(row, 2) else ""
                    f.write(f"{distance}, {fringe_number}, {light_speed}\n")
            QMessageBox.information(self, "成功", "实验数据已导出。")

    def init_parameters(self):
        self.row = 0  # 用于跟踪输出的数据行

    def update_simulation(self):
        lamda = float(self.wavelength_selector.currentText()) * 1.E-9
        x = self.slider.value()
        delta = (float(self.distance_input.text()) + x / self.slider.maximum() * 5e-4)  # 修改光程差
        I = 2 * np.pi * delta * np.cos(np.pi / 4) / lamda
        I = np.square(np.cos(I))

        # **修改点：生成二维干涉图像数据**
        X = np.linspace(-5, 5, 100)
        Y = np.linspace(-5, 5, 100)
        X, Y = np.meshgrid(X, Y)
        Z = np.sin(2 * np.pi * np.sqrt(X**2 + Y**2) / lamda) + I  # 使用干涉公式生成二维图像

        # 创建一个自定义的颜色映射，透明化白色区域
        cmap = plt.get_cmap('viridis')
        new_cmap = cmap(np.arange(cmap.N))
        new_cmap[:, -1] = np.where(np.all(new_cmap[:, :-1] == 1, axis=-1), 0, 1)  # 将白色区域的alpha设为0
        transparent_cmap = ListedColormap(new_cmap)

        # 使用彩色图像并设置白色部分透明
        self.ax.clear()
        self.ax.imshow(Z, cmap=transparent_cmap, interpolation='bessel', origin='lower', aspect='equal')
        self.ax.axis('off')
        self.canvas.draw()

        self.mirror_m2_position_display.setText(str(x))
        num = int(abs(np.floor(2 * (delta - float(self.distance_input.text())) / lamda)))
        self.current_ring_label.setText(f"当前环数：{num}")

    def calculate_and_display_result(self):
        lamda = float(self.wavelength_selector.currentText()) * 1.E-9
        distance = float(self.distance_input.text())  # 读取光程差
        mirror_move = float(self.mirror_input.text())  # 读取镜子移动距离

        # 计算条纹数
        fringe_number = 2 * mirror_move / lamda
        # 加入模拟误差
        light_speed = 299792458 + np.random.normal(0, 1e5)  # 固定光速值加随机误差

        # 将数据添加到表格中
        self.data_table.setItem(self.row, 0, QTableWidgetItem(f"{distance:.2f}"))
        self.data_table.setItem(self.row, 1, QTableWidgetItem(f"{fringe_number:.2f}"))
        self.data_table.setItem(self.row, 2, QTableWidgetItem(f"{light_speed:.3e}"))

        # 更新行数
        self.row += 1

        # 更新实验总结
        avg_light_speed = np.mean([float(self.data_table.item(row, 2).text()) for row in range(self.row)])
        self.summary_text.setText(f"已输出 {self.row} 个数据点。\n当前平均光速为 {avg_light_speed:.3e} m/s。")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MichelsonInterferenceApp()
    window.show()
    sys.exit(app.exec_())