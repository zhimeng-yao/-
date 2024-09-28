import numpy as np
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QComboBox, QGridLayout, QFileDialog, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap, QFont
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from numpy import linspace, sqrt, arctan, square, cos
import math
from numpy import ceil
from numpy import squeeze
from numpy import array
from PyQt5.QtWidgets import QHeaderView, QSlider


# 常量定义
b3cde0 = "#b3cde0"
white = "#ffffff"
gray = "#7f8c8d"
blue_button = "#007bff"
red_button = "#dc3545"

class MichelsonInterferenceApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("迈克尔逊干涉仪仿真")
        self.setMinimumSize(1600, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        left_layout = QVBoxLayout()
        main_layout.addLayout(left_layout)

        # 实验目的
        objectives_label = QLabel("实验目的：")
        objectives_label.setStyleSheet(f"font-size: 20px; font-weight: bold; border: 2px solid {gray}; padding: 10px; background-color: {b3cde0}")
        left_layout.addWidget(objectives_label)
        objectives_content_label = QLabel("了解迈克尔逊干涉原理，测量入射光线波长。")
        objectives_content_label.setStyleSheet(f"font-size: 18px; border: 2px solid {gray}; padding: 10px; background-color: {white}")
        left_layout.addWidget(objectives_content_label)

        # 实验参数
        parameters_label = QLabel("实验参数：")
        parameters_label.setStyleSheet(f"font-size: 20px; font-weight: bold; border: 2px solid {gray}; padding: 10px; background-color: {b3cde0}")
        left_layout.addWidget(parameters_label)
        wavelength_label = QLabel("入射光线波长 (nm):")
        wavelength_label.setStyleSheet(f"font-size: 18px; border: 2px solid {gray}; padding: 10px; background-color: {white}")
        left_layout.addWidget(wavelength_label)
        self.wavelength_selector = QComboBox()
        self.wavelength_selector.addItems(["632.8"])
        self.wavelength_selector.setStyleSheet(f"font-size: 18px; border: 2px solid {gray}; padding: 10px; background-color: {white}")
        left_layout.addWidget(self.wavelength_selector)

        operation_layout = QGridLayout()
        left_layout.addLayout(operation_layout)

        restore_default_button = QPushButton("恢复默认")
        restore_default_button.setStyleSheet(f"font-size: 18px; background-color: {blue_button}; color: white;")
        restore_default_button.clicked.connect(self.reset_default_settings)
        operation_layout.addWidget(restore_default_button, 0, 0)

        self.ring_display_label = QLabel("环数显示")
        self.ring_display_label.setStyleSheet(f"font-size: 18px; border: 2px solid {gray}; padding: 10px; background-color: {white}")
        self.ring_display_label.mousePressEvent = self.on_ring_display_label_clicked
        operation_layout.addWidget(self.ring_display_label, 0, 1)

        help_document_button = QPushButton("帮助文档")
        help_document_button.setStyleSheet(f"font-size: 18px; background-color: {blue_button}; color: white;")
        help_document_button.clicked.connect(self.show_help_document)
        operation_layout.addWidget(help_document_button, 1, 0)

        return_main_interface_button = QPushButton("返回主界面")
        return_main_interface_button.setStyleSheet(f"font-size: 18px; background-color: {blue_button}; color: white;")
        operation_layout.addWidget(return_main_interface_button, 1, 1)

        principle_label = QLabel("实验原理图：")
        principle_label.setStyleSheet(f"font-size: 20px; font-weight: bold; border: 2px solid {gray}; padding: 10px; background-color: {b3cde0}")
        left_layout.addWidget(principle_label)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, '迈克尔逊原理图.jfif')
        pixmap = QPixmap(image_path).scaled(400, 500, Qt.KeepAspectRatio)
        self.principle_img = QLabel()
        self.principle_img.setPixmap(pixmap)
        self.principle_img.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(self.principle_img)

        middle_layout = QVBoxLayout()
        main_layout.addLayout(middle_layout)

        simulation_label = QLabel("仿真图像：等倾干涉图")
        simulation_label.setStyleSheet(f"font-size: 20px; font-weight: bold; border: 2px solid {gray}; padding: 10px; background-color: {b3cde0}")
        middle_layout.addWidget(simulation_label)

        self.figure = plt.figure(figsize=(10, 12))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        middle_layout.addWidget(self.canvas)

        self.current_ring_label = QLabel("当前环数：0")
        self.current_ring_label.setStyleSheet(f"font-size: 18px; border: 2px solid {gray}; padding: 10px; background-color: {white}")
        middle_layout.addWidget(self.current_ring_label)

        self.mirror_m2_position_label = QLabel("动镜 M2 位置：")
        self.mirror_m2_position_label.setStyleSheet(f"font-size: 18px; border: 2px solid {gray}; padding: 10px; background-color: {white}")
        middle_layout.addWidget(self.mirror_m2_position_label)
        self.mirror_m2_position_display = QLineEdit()
        middle_layout.addWidget(self.mirror_m2_position_display)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(50)
        self.slider.setStyleSheet("QSlider::groove:horizontal { background-color: #CCCCCC; height: 10px; } QSlider::handle:horizontal { background-color: #333333; width: 20px; border-radius: 5px; }")
        self.slider.valueChanged.connect(self.update_simulation)
        middle_layout.addWidget(self.slider)

        right_layout = QVBoxLayout()
        main_layout.addLayout(right_layout)

        data_label = QLabel("数据记录区：")
        data_label.setStyleSheet(f"font-size: 20px; font-weight: bold; border: 2px solid {gray}; padding: 10px; background-color: {b3cde0}")
        right_layout.addWidget(data_label)

        # 修改表格样式表，确保表头文字能够显示，并增加列宽和行高
        table_style = f"font-size: 16px; border: 1px solid {gray}; padding: 1px; background-color: {white}"
        self.data_table1 = QTableWidget(5, 2)
        self.data_table1.setHorizontalHeaderLabels(["横移条纹数 Ni", "位置 ei(mm)"])
        self.data_table1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.data_table1.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.data_table1.setStyleSheet(table_style)
        # 增加列宽
        self.data_table1.setColumnWidth(0, 200)
        self.data_table1.setColumnWidth(1, 200)
        # 增加行高
        self.data_table1.verticalHeader().setDefaultSectionSize(30)
        for row in range(5):
            if row == 0:
                item1 = QTableWidgetItem("0")
            elif row == 1:
                item1 = QTableWidgetItem("50")
            elif row == 2:
                item1 = QTableWidgetItem("100")
            elif row == 3:
                item1 = QTableWidgetItem("150")
            elif row == 4:
                item1 = QTableWidgetItem("200")
            item2 = QTableWidgetItem("")
            self.data_table1.setItem(row, 0, item1)
            self.data_table1.setItem(row, 1, item2)
        right_layout.addWidget(self.data_table1)

        self.data_table2 = QTableWidget(5, 2)
        self.data_table2.setHorizontalHeaderLabels(["横移条纹数 Ni", "位置 ei(mm)"])
        self.data_table2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.data_table2.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.data_table2.setStyleSheet(table_style)
        # 增加列宽
        self.data_table2.setColumnWidth(0, 200)
        self.data_table2.setColumnWidth(1, 200)
        # 增加行高
        self.data_table2.verticalHeader().setDefaultSectionSize(30)
        for row in range(5):
            if row == 0:
                item1 = QTableWidgetItem("250")
            elif row == 1:
                item1 = QTableWidgetItem("300")
            elif row == 2:
                item1 = QTableWidgetItem("350")
            elif row == 3:
                item1 = QTableWidgetItem("400")
            elif row == 4:
                item1 = QTableWidgetItem("450")
            item2 = QTableWidgetItem("")
            self.data_table2.setItem(row, 0, item1)
            self.data_table2.setItem(row, 1, item2)
        right_layout.addWidget(self.data_table2)

        self.data_table3 = QTableWidget(5, 2)
        self.data_table3.setHorizontalHeaderLabels(["△N=N(i+5)-Ni", "△e=e(i+5)-ei"])
        self.data_table3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.data_table3.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.data_table3.setStyleSheet(table_style)
        # 增加列宽
        self.data_table3.setColumnWidth(0, 200)
        self.data_table3.setColumnWidth(1, 200)
        # 增加行高
        self.data_table3.verticalHeader().setDefaultSectionSize(30)
        for row in range(5):
            if row == 0:
                item1 = QTableWidgetItem("250-0")
            elif row == 1:
                item1 = QTableWidgetItem("300-50")
            elif row == 2:
                item1 = QTableWidgetItem("350-100")
            elif row == 3:
                item1 = QTableWidgetItem("400-150")
            elif row == 4:
                item1 = QTableWidgetItem("450-200")
            item2 = QTableWidgetItem("")
            self.data_table3.setItem(row, 0, item1)
            self.data_table3.setItem(row, 1, item2)
        right_layout.addWidget(self.data_table3)

        data_operation_layout = QHBoxLayout()
        right_layout.addLayout(data_operation_layout)
        write_data_button = QPushButton("写入数据")
        write_data_button.setStyleSheet(f"font-size: 18px; background-color: {blue_button}; color: white;")
        write_data_button.clicked.connect(self.write_data_to_tables)
        data_operation_layout.addWidget(write_data_button)
        clear_data_button = QPushButton("清除数据")
        clear_data_button.setStyleSheet(f"font-size: 18px; background-color: {blue_button}; color: white;")
        clear_data_button.clicked.connect(self.clear_data_tables)
        data_operation_layout.addWidget(clear_data_button)
        export_data_button = QPushButton("导出数据")
        export_data_button.setStyleSheet(f"font-size: 18px; background-color: {blue_button}; color: white;")
        export_data_button.clicked.connect(self.export_data)
        data_operation_layout.addWidget(export_data_button)

        results_label = QLabel("结果展示区：")
        results_label.setStyleSheet(f"font-size: 20px; font-weight: bold; border: 2px solid {gray}; padding: 10px; background-color: {b3cde0}")
        right_layout.addWidget(results_label)
        self.result_display = QLabel()
        right_layout.addWidget(self.result_display)

        start_calculation_button = QPushButton("开始计算")
        start_calculation_button.setStyleSheet(f"font-size: 18px; background-color: {blue_button}; color: white;")
        start_calculation_button.clicked.connect(self.calculate_and_display_result)
        right_layout.addWidget(start_calculation_button)

        self.init_parameters()
        self.update_simulation()

    def init_parameters(self):
        self.N = 200
        self.X_Mmax = 10e-3
        self.Y_Mmax = self.X_Mmax
        self.N = self.N
        X_Mmin = -self.X_Mmax
        Y_Mmin = X_Mmin
        X = linspace(X_Mmin, self.X_Mmax, self.N)
        Y = X
        [x, y] = np.meshgrid(X, Y)
        r = np.square(x) + np.square(y)
        f = 0.1
        self.theta = np.arctan(np.sqrt(r) / f)
        self._translate = None
        self.maxl = 5e-4
        self.d0 = 1e-3 + 1 / 2 * self.maxl
        self.row = 0
        self.table_num = 0
        self.lamda = None
        self.location = None
        self.mainstrtemp = "url(img/100.jpg) 0 {0} 145 {1}"
        self.vicestrtemp = "url(img/100.jpg) 0 {0} 145 {1}"
        self.SongTi = QFont()

    def update_simulation(self):
        lamda = float(self.wavelength_selector.currentText()) * 1.E-9
        self.lamda = lamda
        x = self.slider.value()
        delta = self.d0 + x / self.slider.maximum() * self.maxl
        I = 2 * np.pi * delta * np.cos(self.theta) / lamda
        I = np.square(np.cos(I))
        my_cmap = self.generate_color_map(float(self.wavelength_selector.currentText()))
        num = int(abs(np.floor(2 * (delta - self.d0) / lamda)))
        self.ax.clear()
        self.ax.imshow(I, cmap=my_cmap, interpolation='bessel', origin='lower', vmin=0, vmax=1)
        self.ax.axis('off')
        self.canvas.draw()
        self.mirror_m2_position_display.setText(str(x))
        self.current_ring_label.setText(f"当前环数：{num}")

    def write_data_to_tables(self):
        if self.table_num == 0:
            self.data_table1.setItem(self.row, 1, QTableWidgetItem(self.location))
        else:
            self.data_table2.setItem(self.row, 1, QTableWidgetItem(self.location))
        self.row += 1
        if self.row >= 5:
            self.table_num += 1
            self.row = 0
        if self.table_num >= 2:
            self.table_num = 0
            self.row = 0

    def clear_data_tables(self):
        self.row = 0
        self.table_num = 0
        for table in [self.data_table1, self.data_table2, self.data_table3]:
            for i in range(5):
                j = 1
                table.setItem(i, j, QTableWidgetItem(""))

    def export_data(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "导出数据", "", "Excel Files (*.xlsx);;All Files (*)",
                                                   options=options)
        if file_name:
            pass

    def calculate_and_display_result(self):
        pass


    def show_message(self):
        QMessageBox.critical(self, "错误", "缺少数据")

    def reset_default_settings(self):
        self.wavelength_selector.setCurrentIndex(0)
        self.slider.setValue(50)
        self.clear_data_tables()
        self.update_simulation()


    def show_help_document(self):
        path = os.path.abspath('.')
        pass

    def generate_color_map(self, wavelength):
        COL = np.load("MyColorMap.npy")
        xRGB = int(ceil(abs(780 - wavelength) / 2))
        Acmx = linspace(0, COL[0][xRGB], 255)
        Acmy = linspace(0, COL[1][xRGB], 255)
        Acmz = linspace(0, COL[2][xRGB], 255)
        return ListedColormap(squeeze(array([[Acmx], [Acmy], [Acmz]])).T, "mymap")

    def on_ring_display_label_clicked(self, event):
        print("环数显示标签被点击了")


if __name__ == "__main__":
    app = QApplication([])
    window = MichelsonInterferenceApp()
    window.show()
    app.exec_()