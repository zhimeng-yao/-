import sys
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QTextEdit
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar

PRIMARY_COLOR = "#4CAF50"
SECONDARY_COLOR = "#2196F3"
BACKGROUND_COLOR = "#F5F5F5"
HIGHLIGHT_COLOR = "#FFC107"
ACCENT_COLOR = "#E91E63"

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

class DataProcessingUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.plot_windows = {}
        self.setWindowTitle("实验数据处理")
    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet(f"background-color: {BACKGROUND_COLOR};")

        import_layout = QHBoxLayout()
        import_layout.setSpacing(15)
        self.textEdit_path = QTextEdit()
        self.textEdit_path.setFixedSize(300, 60)  # 设置固定大小为宽300像素，高50像素
        self.textEdit_path.setStyleSheet(f"background-color: white; border: 1px solid {SECONDARY_COLOR}; padding: 5px; border-radius: 5px;")
        self.pushButton_in = QPushButton('导入数据')
        self.pushButton_in.setStyleSheet(f"background-color: {PRIMARY_COLOR}; color: white; padding: 8px 15px; border-radius: 5px;")
        import_label = QLabel('请在下框中输入表格位置, 或将表格拖入其中。 \n       (每个变量请以列的方式写入)')
        import_label.setStyleSheet("color: #333; font-size: 24px;")
        import_layout.addWidget(import_label)
        import_layout.addWidget(self.textEdit_path)
        import_layout.addWidget(self.pushButton_in)

        processing_layout = QHBoxLayout()
        processing_layout.setSpacing(15)
        self.variance_std_button = QPushButton('方差/标准差')
        self.variance_std_button.setStyleSheet(f"background-color: {SECONDARY_COLOR}; color: white; padding: 8px 15px; border-radius: 5px;")
        self.mean_extremes_button = QPushButton('均值/极值')
        self.mean_extremes_button.setStyleSheet(f"background-color: {SECONDARY_COLOR}; color: white; padding: 8px 15px; border-radius: 5px;")
        self.uncertainty_button = QPushButton('不确定度')
        self.uncertainty_button.setStyleSheet(f"background-color: {SECONDARY_COLOR}; color: white; padding: 8px 15px; border-radius: 5px;")
        self.formula_button = QPushButton('计算公式')
        self.formula_button.setStyleSheet(f"background-color: {SECONDARY_COLOR}; color: white; padding: 8px 15px; border-radius: 5px;")
        processing_layout.addWidget(self.variance_std_button)
        processing_layout.addWidget(self.mean_extremes_button)
        processing_layout.addWidget(self.uncertainty_button)
        processing_layout.addWidget(self.formula_button)

        plotting_layout = QHBoxLayout()
        plotting_layout.setSpacing(15)
        self.scatter_button = QPushButton('散点图')
        self.scatter_button.setStyleSheet(f"background-color: {SECONDARY_COLOR}; color: white; padding: 8px 15px; border-radius: 5px;")
        self.curve_button = QPushButton('曲线图')
        self.curve_button.setStyleSheet(f"background-color: {SECONDARY_COLOR}; color: white; padding: 8px 15px; border-radius: 5px;")
        self.linear_fit_button = QPushButton('线性拟合')
        self.linear_fit_button.setStyleSheet(f"background-color: {SECONDARY_COLOR}; color: white; padding: 8px 15px; border-radius: 5px;")
        self.quadratic_fit_button = QPushButton('二次函数拟合')
        self.quadratic_fit_button.setStyleSheet(f"background-color: {SECONDARY_COLOR}; color: white; padding: 8px 15px; border-radius: 5px;")
        self.cubic_fit_button = QPushButton('三次函数拟合')
        self.cubic_fit_button.setStyleSheet(f"background-color: {SECONDARY_COLOR}; color: white; padding: 8px 15px; border-radius: 5px;")
        self.spline_button = QPushButton('三次样条插值')
        self.spline_button.setStyleSheet(f"background-color: {SECONDARY_COLOR}; color: white; padding: 8px 15px; border-radius: 5px;")
        plotting_layout.addWidget(self.scatter_button)
        plotting_layout.addWidget(self.curve_button)
        plotting_layout.addWidget(self.linear_fit_button)
        plotting_layout.addWidget(self.quadratic_fit_button)
        plotting_layout.addWidget(self.cubic_fit_button)
        plotting_layout.addWidget(self.spline_button)

        exit_layout = QHBoxLayout()
        self.pushButton_exit = QPushButton('退出')
        self.pushButton_exit.setStyleSheet(f"background-color: {ACCENT_COLOR}; color: white; padding: 8px 15px; border-radius: 5px;")
        exit_layout.addWidget(self.pushButton_exit)

        self.result_label = QLabel()
        self.result_label.setStyleSheet(f"color: #333; background-color: white; border: 1px solid #999; padding: 10px; border-radius: 5px;")

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(25)
        main_layout.addLayout(import_layout)
        main_layout.addLayout(processing_layout)
        main_layout.addLayout(plotting_layout)
        main_layout.addWidget(self.result_label)
        main_layout.addLayout(exit_layout)

        self.pushButton_in.clicked.connect(self.pushButton_in_Clicked)
        self.pushButton_exit.clicked.connect(self.pushButton_exit_Clicked)
        self.variance_std_button.clicked.connect(self.calculate_variance_std)
        self.mean_extremes_button.clicked.connect(self.calculate_mean_extremes)
        self.uncertainty_button.clicked.connect(self.calculate_uncertainty)
        self.scatter_button.clicked.connect(self.plot_scatter)
        self.curve_button.clicked.connect(self.plot_curve)
        self.linear_fit_button.clicked.connect(self.linear_fit)
        self.quadratic_fit_button.clicked.connect(self.quadratic_fit)
        self.cubic_fit_button.clicked.connect(self.cubic_fit)
        self.spline_button.clicked.connect(self.cubic_spline_interpolation)

    def pushButton_exit_Clicked(self):
        self.close()

    def pushButton_in_Clicked(self):
        path = self.textEdit_path.toPlainText()
        if path == '':
            path = "D:/data.xlsx"
        path = path.replace("file:///", "", 1)
        try:
            df = pd.read_excel(path)
            self.data = np.array(df)
            self.col_name = list(df)
            self.result_label.setText("导入数据成功")
        except Exception as e:
            self.result_label.setText(f"导入数据失败：{str(e)}")

    def calculate_variance_std(self):
        if hasattr(self, 'data'):
            data = self.data
            variances = np.var(data, axis=0)
            std_devs = np.std(data, axis=0)
            self.result_label.setText(f"变量的方差：\n{variances}\n变量的标准差：\n{std_devs}")
        else:
            self.result_label.setText("请先导入数据")

    def calculate_mean_extremes(self):
        if hasattr(self, 'data'):
            data = self.data
            means = np.mean(data, axis=0)
            mins = np.min(data, axis=0)
            maxs = np.max(data, axis=0)
            self.result_label.setText(f"变量的均值：\n{means}\n变量的极小值：\n{mins}\n变量的极大值：\n{maxs}")
        else:
            self.result_label.setText("请先导入数据")

    def calculate_uncertainty(self):
        if hasattr(self, 'data'):
            data = self.data
            std_devs = np.std(data, axis=0)
            uncertainties = std_devs / 2
            self.result_label.setText(f"变量的不确定度：\n{uncertainties}")
        else:
            self.result_label.setText("请先导入数据")

    def plot_scatter(self):
        if hasattr(self, 'data'):
            x = self.data[:, 0]
            y = self.data[:, 1]
            fig = Figure()
            canvas = FigureCanvas(fig)
            ax = fig.add_subplot(111)
            ax.scatter(x, y, label='原始数据', color="#FF9800", s=50, alpha=0.8)
            ax.set_title('原始数据散点图', color="#333", fontsize=16)
            ax.legend(fontsize=12)
            toolbar = NavigationToolbar(canvas, self)
            scatter_window = QWidget()
            scatter_layout = QVBoxLayout()
            scatter_layout.addWidget(canvas)
            scatter_layout.addWidget(toolbar)
            scatter_window.setLayout(scatter_layout)
            scatter_window.setStyleSheet(f"background-color: {BACKGROUND_COLOR}; border: 2px solid {SECONDARY_COLOR}; border-radius: 10px; box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.2);")
            scatter_window.show()
            self.plot_windows['scatter'] = scatter_window
        else:
            self.result_label.setText("请先导入数据")

    def plot_curve(self):
        if hasattr(self, 'data'):
            x = self.data[:, 0]
            y = self.data[:, 1]
            fig = Figure()
            canvas = FigureCanvas(fig)
            ax = fig.add_subplot(111)
            ax.plot(x, y, label='曲线', color="#FF9800", linewidth=2)
            ax.set_title('数据曲线图', color="#333", fontsize=16)
            ax.legend(fontsize=12)
            toolbar = NavigationToolbar(canvas, self)
            curve_window = QWidget()
            curve_layout = QVBoxLayout()
            curve_layout.addWidget(canvas)
            curve_layout.addWidget(toolbar)
            curve_window.setLayout(curve_layout)
            curve_window.setStyleSheet(f"background-color: {BACKGROUND_COLOR}; border: 2px solid {SECONDARY_COLOR}; border-radius: 10px; box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.2);")
            curve_window.show()
            self.plot_windows['curve'] = curve_window
        else:
            self.result_label.setText("请先导入数据")

    def linear_fit(self):
        if hasattr(self, 'data'):
            x = self.data[:, 0]
            y = self.data[:, 1]
            fit = np.polyfit(x, y, 1)
            fit_fn = np.poly1d(fit)
            fig = Figure()
            canvas = FigureCanvas(fig)
            ax = fig.add_subplot(111)
            ax.plot(x, y, 'o', label='原始数据', color="#FF9800")
            ax.plot(x, fit_fn(x), label='线性拟合曲线', color="#4CAF50", linewidth=2)
            ax.set_title('数据曲线与线性拟合', color="#333", fontsize=16)
            ax.legend(fontsize=12)
            function_label = QLabel(f"拟合函数：y = {np.round(fit_fn[0], 2)} + {np.round(fit_fn[1], 2)}x")
            function_label.setStyleSheet("color: #333; font-size: 24px;")
            toolbar = NavigationToolbar(canvas, self)
            linear_fit_window = QWidget()
            linear_fit_layout = QVBoxLayout()
            linear_fit_layout.addWidget(canvas)
            linear_fit_layout.addWidget(function_label)
            linear_fit_layout.addWidget(toolbar)
            linear_fit_window.setLayout(linear_fit_layout)
            linear_fit_window.setStyleSheet(f"background-color: {BACKGROUND_COLOR}; border: 2px solid {SECONDARY_COLOR}; border-radius: 10px; box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.2);")
            linear_fit_window.show()
            self.plot_windows['linear_fit'] = linear_fit_window
        else:
            self.result_label.setText("请先导入数据")

    def quadratic_fit(self):
        if hasattr(self, 'data'):
            x = self.data[:, 0]
            y = self.data[:, 1]
            fit = np.polyfit(x, y, 2)
            fit_fn = np.poly1d(fit)
            fig = Figure()
            canvas = FigureCanvas(fig)
            ax = fig.add_subplot(111)
            ax.plot(x, y, 'o', label='原始数据', color="#FF9800")
            ax.plot(x, fit_fn(x), label='二次函数拟合曲线', color="#2196F3", linewidth=2)
            ax.set_title('数据曲线与二次函数拟合', color="#333", fontsize=16)
            ax.legend(fontsize=12)
            function_label = QLabel(f"拟合函数：y = {np.round(fit_fn[0], 2)} + {np.round(fit_fn[1], 2)}x + {np.round(fit_fn[2], 2)}x^2")
            function_label.setStyleSheet("color: #333; font-size: 24px;")
            toolbar = NavigationToolbar(canvas, self)
            quadratic_fit_window = QWidget()
            quadratic_fit_layout = QVBoxLayout()
            quadratic_fit_layout.addWidget(canvas)
            quadratic_fit_layout.addWidget(function_label)
            quadratic_fit_layout.addWidget(toolbar)
            quadratic_fit_window.setLayout(quadratic_fit_layout)
            quadratic_fit_window.setStyleSheet(f"background-color: {BACKGROUND_COLOR}; border: 2px solid {SECONDARY_COLOR}; border-radius: 10px; box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.2);")
            quadratic_fit_window.show()
            self.plot_windows['quadratic_fit'] = quadratic_fit_window
        else:
            self.result_label.setText("请先导入数据")


    def cubic_fit(self):
        if hasattr(self, 'data'):
            x = self.data[:, 0]
            y = self.data[:, 1]
            fit = np.polyfit(x, y, 3)
            fit_fn = np.poly1d(fit)
            fig = Figure()
            canvas = FigureCanvas(fig)
            ax = fig.add_subplot(111)
            ax.plot(x, y, 'o', label='原始数据', color="#FF9800")
            ax.plot(x, fit_fn(x), label='三次函数拟合曲线', color="#E91E63", linewidth=2)
            ax.set_title('数据曲线与三次函数拟合', color="#333", fontsize=16)
            ax.legend(fontsize=12)
            function_label = QLabel(f"拟合函数：y = {np.round(fit_fn[0], 2)} + {np.round(fit_fn[1], 2)}x + {np.round(fit_fn[2], 2)}x^2 + {np.round(fit_fn[3], 2)}x^3")
            function_label.setStyleSheet("color: #333; font-size: 24px;")
            toolbar = NavigationToolbar(canvas, self)
            cubic_fit_window = QWidget()
            cubic_fit_layout = QVBoxLayout()
            cubic_fit_layout.addWidget(canvas)
            cubic_fit_layout.addWidget(function_label)
            cubic_fit_layout.addWidget(toolbar)
            cubic_fit_window.setLayout(cubic_fit_layout)
            cubic_fit_window.setStyleSheet(f"background-color: {BACKGROUND_COLOR}; border: 2px solid {SECONDARY_COLOR}; border-radius: 10px; box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.2);")
            cubic_fit_window.show()
            self.plot_windows['cubic_fit'] = cubic_fit_window
        else:
            self.result_label.setText("请先导入数据")

    def cubic_spline_interpolation(self):
        if hasattr(self, 'data'):
            x = self.data[:, 0]
            y = self.data[:, 1]
            from scipy.interpolate import CubicSpline
            cs = CubicSpline(x, y)
            x_interp = np.linspace(x.min(), x.max(), 100)
            y_interp = cs(x_interp)
            fig = Figure()
            canvas = FigureCanvas(fig)
            ax = fig.add_subplot(111)
            ax.plot(x, y, 'o', label='原始数据', color="#FF9800")
            ax.plot(x_interp, y_interp, label='三次样条插值曲线', color="#673AB7", linewidth=2)
            ax.set_title('数据曲线与三次样条插值', color="#333", fontsize=16)
            ax.legend(fontsize=12)
            toolbar = NavigationToolbar(canvas, self)
            spline_window = QWidget()
            spline_layout = QVBoxLayout()
            spline_layout.addWidget(canvas)
            spline_layout.addWidget(toolbar)
            spline_window.setLayout(spline_layout)
            spline_window.setStyleSheet(
                f"background-color: {BACKGROUND_COLOR}; border: 2px solid {SECONDARY_COLOR}; border-radius: 10px; box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.2);")
            spline_window.show()
            self.plot_windows['spline'] = spline_window
        else:
            self.result_label.setText("请先导入数据")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataProcessingUI()
    window.show()
    sys.exit(app.exec_())
