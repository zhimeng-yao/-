import sys
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QTextEdit
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from scipy.stats import kurtosis
from scipy.stats import skew
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QPixmap


PRIMARY_COLOR = "#4CAF50"
SECONDARY_COLOR = "#2196F3"
BACKGROUND_COLOR = "#F8F8F8"
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


        # 导入部分布局
        import_box = QVBoxLayout()
        import_label = QLabel('请在下框中输入表格位置, 或将表格拖入其中。 (每个变量请以列的方式写入)')
        import_label.setStyleSheet("color: #333; font-size: 34px; font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);")
        import_box.addWidget(import_label)

        import_path_layout = QHBoxLayout()
        self.textEdit_path = QTextEdit()
        self.textEdit_path.setFixedSize(500, 100)
        self.textEdit_path.setStyleSheet(f"background-color: white; border: 2px solid {SECONDARY_COLOR}; padding: 20px; border-radius: 25px; font-size: 20px; box-shadow: 2px 2px 4px rgba(0,0,0,0.1);")
        import_path_layout.addWidget(self.textEdit_path)

        self.pushButton_in = QPushButton('导入数据')
        self.pushButton_in.setStyleSheet(f"background-color: {PRIMARY_COLOR}; color: white; padding: 18px 30px; border-radius: 25px; font-size: 20px; font-weight: bold; box-shadow: 3px 3px 6px rgba(0,0,0,0.2);")
        import_path_layout.addWidget(self.pushButton_in)
        import_box.addLayout(import_path_layout)

        # 处理部分布局
        processing_box = QVBoxLayout()
        processing_label = QLabel('数据处理')
        processing_label.setStyleSheet("color: #333; font-size: 26px; font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);")
        processing_box.addWidget(processing_label)

        processing_buttons_layout = QHBoxLayout()
        processing_buttons_layout.setSpacing(40)
        button_style = f"background-color: {SECONDARY_COLOR}; color: white; padding: 18px 30px; border-radius: 25px; font-size: 20px; font-weight: bold; box-shadow: 3px 3px 6px rgba(0,0,0,0.2);"
        self.variance_std_button = QPushButton('方差/标准差')
        self.variance_std_button.setStyleSheet(button_style)
        self.mean_extremes_button = QPushButton('均值/极值')
        self.mean_extremes_button.setStyleSheet(button_style)
        self.uncertainty_button = QPushButton('不确定度')
        self.uncertainty_button.setStyleSheet(button_style)
        self.skewness_kurtosis_button = QPushButton('偏度/峰度')
        self.skewness_kurtosis_button.setStyleSheet(button_style)
        self.formula_button = QPushButton('计算公式')
        self.formula_button.setStyleSheet(button_style)
        self.correlation_button = QPushButton('相关性分析')
        self.correlation_button.setStyleSheet(button_style)


        processing_buttons_layout.addWidget(self.variance_std_button)
        processing_buttons_layout.addWidget(self.mean_extremes_button)
        processing_buttons_layout.addWidget(self.skewness_kurtosis_button)
        processing_buttons_layout.addWidget(self.uncertainty_button)
        processing_buttons_layout.addWidget(self.correlation_button)
        processing_buttons_layout.addWidget(self.formula_button)
        processing_box.addLayout(processing_buttons_layout)





        # 绘图部分布局
        plotting_box = QVBoxLayout()
        plotting_label = QLabel('绘图')
        plotting_label.setStyleSheet("color: #333; font-size: 26px; font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);")
        plotting_box.addWidget(plotting_label)

        plotting_buttons_layout = QHBoxLayout()
        plotting_buttons_layout.setSpacing(40)
        self.scatter_button = QPushButton('散点图')
        self.scatter_button.setStyleSheet(button_style)
        self.boxplot_button = QPushButton('箱线图')
        self.boxplot_button.setStyleSheet(button_style)
        self.curve_button = QPushButton('曲线图')
        self.curve_button.setStyleSheet(button_style)
        self.linear_fit_button = QPushButton('线性拟合')
        self.linear_fit_button.setStyleSheet(button_style)
        self.quadratic_fit_button = QPushButton('二次函数拟合')
        self.quadratic_fit_button.setStyleSheet(button_style)
        self.cubic_fit_button = QPushButton('三次函数拟合')
        self.cubic_fit_button.setStyleSheet(button_style)
        self.spline_button = QPushButton('三次样条插值')
        self.spline_button.setStyleSheet(button_style)

        # Add boxplot button


        plotting_buttons_layout.addWidget(self.scatter_button)
        plotting_buttons_layout.addWidget(self.boxplot_button)
        plotting_buttons_layout.addWidget(self.curve_button)
        plotting_buttons_layout.addWidget(self.linear_fit_button)
        plotting_buttons_layout.addWidget(self.quadratic_fit_button)
        plotting_buttons_layout.addWidget(self.cubic_fit_button)
        plotting_buttons_layout.addWidget(self.spline_button)


        plotting_box.addLayout(plotting_buttons_layout)

        # Connect button signals to appropriate functions
        self.scatter_button.clicked.connect(self.plot_scatter)
        self.curve_button.clicked.connect(self.plot_curve)
        self.linear_fit_button.clicked.connect(self.linear_fit)
        self.quadratic_fit_button.clicked.connect(self.quadratic_fit)
        self.cubic_fit_button.clicked.connect(self.cubic_fit)
        self.spline_button.clicked.connect(self.cubic_spline_interpolation)
        self.boxplot_button.clicked.connect(self.plot_boxplot)

        # 退出按钮布局
        exit_box = QVBoxLayout()
        self.pushButton_exit = QPushButton('退出')
        self.pushButton_exit.setStyleSheet(f"background-color: {ACCENT_COLOR}; color: white; padding: 18px 30px; border-radius: 25px; font-size: 20px; font-weight: bold; box-shadow: 3px 3px 6px rgba(0,0,0,0.2);")
        exit_box.addWidget(self.pushButton_exit)

        # 结果显示布局
        result_box = QVBoxLayout()
        self.result_label = QLabel()
        self.result_label.setStyleSheet(f"color: #333; background-color: white; border: 2px solid #999; padding: 25px; border-radius: 25px; font-size: 22px; box-shadow: 2px 2px 4px rgba(0,0,0,0.1);")
        result_box.addWidget(self.result_label)

        self.variance_std_button.clicked.connect(self.calculate_variance_std)
        self.mean_extremes_button.clicked.connect(self.calculate_mean_extremes)
        self.uncertainty_button.clicked.connect(self.calculate_uncertainty)
        self.skewness_kurtosis_button.clicked.connect(self.calculate_skewness_kurtosis)
        self.correlation_button.clicked.connect(self.calculate_correlation)
        self.formula_button.clicked.connect(self.show_formulas)



        # 整体布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(50)
        main_layout.addLayout(import_box)
        main_layout.addLayout(processing_box)
        main_layout.addLayout(plotting_box)
        main_layout.addLayout(result_box)
        main_layout.addLayout(exit_box)

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

    def show_formulas(self):
        formula_dialog = QDialog(self)
        formula_dialog.setWindowTitle("计算公式")
        formula_dialog.resize(900, 600)  # 设置对话框大小
        formula_text = QTextEdit(formula_dialog)
        formula_text.setReadOnly(True)
        formula_text.setText("""
    方差/标准差：
        设一组数据为 x₁, x₂,..., xₙ，平均数为 μ。
        方差公式：s² = Σ((xᵢ - μ)²) / n。
        标准差公式：s = √s²。

    均值/极值：
        均值公式：μ = (x₁ + x₂ +... + xₙ) / n。
        极值公式：最大值 max(x₁, x₂,..., xₙ)，最小值 min(x₁, x₂,..., xₙ)。

    偏度/峰度：
        偏度公式（使用三阶中心矩）：Skewness = Σ((xᵢ - μ)³) / (n * s³)。
        峰度公式（使用四阶中心矩）：Kurtosis = Σ((xᵢ - μ)⁴) / (n * s⁴) - 3。

    不确定度：
        标准差公式： s = √(Σ((xᵢ - μ)²) / n)，其中 μ 是数据的均值，n 是数据个数。
        不确定度公式： uncertainties = s / 2。

    相关性分析：
        设两组数据为 X = [x₁, x₂,..., xₙ] 和 Y = [y₁, y₂,..., yₙ]。
        相关系数公式：r = Σ((xᵢ - μₓ)(yᵢ - μᵧ)) / (√Σ((xᵢ - μₓ)²) * √Σ((yᵢ - μᵧ)²))。
            """)
        layout = QVBoxLayout(formula_dialog)
        layout.addWidget(formula_text)
        formula_dialog.exec_()

    def calculate_skewness_kurtosis(self):
        if hasattr(self, 'data'):
            data = self.data

            n = data.shape[0]
            mean = np.mean(data, axis=0)
            std_dev = np.std(data, axis=0)

            third_moment_sum = np.sum([(data[:, i] - mean[i]) ** 3 for i in range(data.shape[1])], axis=1)
            skewness = np.divide(third_moment_sum.sum(axis=0), n) / std_dev ** 3

            fourth_moment_sum = np.sum([(data[:, i] - mean[i]) ** 4 for i in range(data.shape[1])], axis=1)
            kurtosis = np.divide(fourth_moment_sum.sum(axis=0), n) / std_dev ** 4 - 3

            self.result_label.setText(f"变量的偏度：\n{skewness}\n变量的峰度：\n{kurtosis}")
        else:
            self.result_label.setText("请先导入数据")
    def calculate_correlation(self):
        if hasattr(self, 'data'):
            data = self.data
            if data.shape[1] < 2:
                self.result_label.setText("数据至少需要两列才能进行相关性分析")
                return

            results = []
            column_names = [f'X{i + 1}' for i in range(data.shape[1])]
            for i in range(data.shape[1]):
                for j in range(i + 1, data.shape[1]):
                    corr, _ = pearsonr(data[:, i], data[:, j])
                    covariance = np.cov(data[:, i], data[:, j])[0, 1]
                    results.append(f'{column_names[i]} 与 {column_names[j]} 的相关系数：{corr}，协方差：{covariance}')

            self.result_label.setText("\n".join(results))
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

    def plot_boxplot(self):
        if hasattr(self, 'data'):
            # 假设数据只有一列需要绘制箱线图
            data = self.data[:, 1]
            fig = Figure()
            canvas = FigureCanvas(fig)
            ax = fig.add_subplot(111)
            ax.boxplot(data, labels=['数据'], patch_artist=True)

            min_value = np.min(data)
            max_value = np.max(data)
            q1, median, q3 = np.percentile(data, [25, 50, 75])
            info_label = QLabel(f"最小值: {min_value}\n最大值: {max_value}\nQ1(25%): {q1}\n中位数(50%): {median}\nQ3(75%): {q3}")
            ax.set_title('数据箱线图', color="#333", fontsize=16)
            toolbar = NavigationToolbar(canvas, self)
            boxplot_window = QWidget()
            boxplot_layout = QVBoxLayout()
            boxplot_layout.addWidget(canvas)
            boxplot_layout.addWidget(info_label)
            boxplot_layout.addWidget(toolbar)
            boxplot_window.setLayout(boxplot_layout)
            boxplot_window.setStyleSheet(
                f"background-color: {BACKGROUND_COLOR}; border: 2px solid {SECONDARY_COLOR}; border-radius: 10px; box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.2);")
            boxplot_window.show()
            self.plot_windows['boxplot'] = boxplot_window
        else:
            self.result_label.setText("请先导入数据")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataProcessingUI()
    window.show()
    sys.exit(app.exec_())
