import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QComboBox, QGridLayout, QSlider, QFrame, QColorDialog, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QColor
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# 常量定义
c = 3.0e8  # 光速 (m/s)

# 晶体折射率数据 (示例数据)
crystal_data = {
    "石英": {"no": 1.544, "ne": 1.553},
    "方解石": {"no": 1.658, "ne": 1.486},
    
}

class BirefringenceExperiment(QMainWindow):
    def __init__(self):
        super().__init__()
        # 设置主窗口属性
        self.setWindowTitle("单轴晶体双折射仿真实验")
        self.setGeometry(100, 100, 1600, 900)
        # 设置主颜色主题
        self.setStyleSheet("background-color: #f0f0f0; color: #333333;")
        # 创建主部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # 左侧布局：实验目的 + 计算公式 + 实验原理图
        left_layout = QVBoxLayout()
        main_layout.addLayout(left_layout)

        # 设置统一的框架样式
        self.setup_frame_style = lambda frame: frame.setStyleSheet("border: 1px solid black; background-color: #ffffff;")

        # 实验目的框架
        self.objectives_frame = QFrame()
        self.setup_frame_style(self.objectives_frame)
        objectives_layout = QVBoxLayout(self.objectives_frame)
        left_layout.addWidget(self.objectives_frame)

        # 实验目的标题
        self.objectives_title = QLabel("实验目的")
        self.objectives_title.setAlignment(Qt.AlignCenter)
        self.objectives_title.setStyleSheet("font-size: 22px; font-weight: bold; background-color: #d0e0f0; padding: 10px;")
        objectives_layout.addWidget(self.objectives_title)

        # 实验目的内容
        self.objectives_display = QLabel("1. 观察晶体双折射现象\n2. o光和e光的折射角度变化\n3. 不同光轴和入射角下的双折射现象")
        self.objectives_display.setStyleSheet("font-size: 18px; padding: 10px;")
        objectives_layout.addWidget(self.objectives_display)

        # 计算公式框架
        self.formula_frame = QFrame()
        self.setup_frame_style(self.formula_frame)
        left_layout.addWidget(self.formula_frame)
        formula_layout = QVBoxLayout(self.formula_frame)

        # 计算公式标题
        self.formula_title = QLabel("计算公式")
        self.formula_title.setAlignment(Qt.AlignCenter)
        self.formula_title.setStyleSheet("font-size: 22px; font-weight: bold; background-color: #d0e0f0; padding: 10px;")
        formula_layout.addWidget(self.formula_title)

        # 计算公式内容
        self.formula_display = QLabel("Snell's Law for o光: n * sin(θ) = constant\n非常光: 折射率随光轴变化")
        self.formula_display.setStyleSheet("font-size: 18px; padding: 10px;")
        formula_layout.addWidget(self.formula_display)

        # 实验原理和原理图框架
        self.principle_frame = QFrame()
        self.setup_frame_style(self.principle_frame)
        left_layout.addWidget(self.principle_frame)
        principle_layout = QVBoxLayout(self.principle_frame)

        # 实验原理标题
        self.principle_img_label = QLabel("实验原理")
        self.principle_img_label.setAlignment(Qt.AlignCenter)
        self.principle_img_label.setStyleSheet("font-size: 22px; font-weight: bold; background-color: #d0e0f0; padding: 10px;")
        principle_layout.addWidget(self.principle_img_label)

        # 设置图片路径并加载图片
        self.principle_img = QLabel()
        image_path = "晶体双折射.jpg"  # 替换为正确的图片路径
        pixmap = QPixmap(image_path).scaled(500, 350, Qt.KeepAspectRatio)
        self.principle_img.setPixmap(pixmap)
        self.principle_img.setAlignment(Qt.AlignCenter)
        principle_layout.addWidget(self.principle_img)

        # 添加原理演示旋钮
        self.demo_button = QPushButton("原理演示")
        self.demo_button.setStyleSheet("font-size: 18px; padding: 8px;")
        self.demo_button.clicked.connect(self.change_principle_image_color)
        principle_layout.addWidget(self.demo_button)

        # 中间布局：仿真结果图
        middle_layout = QVBoxLayout()
        middle_layout.setSpacing(20)
        main_layout.addLayout(middle_layout, 2)

        # 仿真结果框架
        self.simulation_frame = QFrame()
        self.setup_frame_style(self.simulation_frame)
        middle_layout.addWidget(self.simulation_frame)

        # 仿真结果标题
        simulation_layout = QVBoxLayout(self.simulation_frame)
        self.simulation_title = QLabel("仿真结果")
        self.simulation_title.setAlignment(Qt.AlignCenter)
        self.simulation_title.setStyleSheet("font-size: 16px; font-weight: bold; background-color: #d0e0f0; padding: 10px;")
        simulation_layout.addWidget(self.simulation_title)

        # 仿真图像
        self.figure, self.ax = plt.subplots(figsize=(12, 10))  # 调大图像尺寸
        self.canvas = FigureCanvas(self.figure)
        simulation_layout.addWidget(self.canvas)

        # 右侧布局：参数设置和操作区
        right_layout = QVBoxLayout()
        right_layout.setSpacing(30)
        main_layout.addLayout(right_layout, 1)

        # 参数设置框架
        self.param_frame = QFrame()
        self.setup_frame_style(self.param_frame)
        right_layout.addWidget(self.param_frame)
        param_layout = QGridLayout(self.param_frame)

        # 晶体材料选择
        material_label = QLabel("晶体材料:")
        material_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #003366;")
        param_layout.addWidget(material_label, 0, 0)
        self.material_combo = QComboBox()
        self.material_combo.addItems(crystal_data.keys())
        self.material_combo.setStyleSheet("font-size: 20px;")
        param_layout.addWidget(self.material_combo, 0, 1)

        # 入射角动态调整
        incidence_angle_label = QLabel("入射角 (度):")
        incidence_angle_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #003366;")
        param_layout.addWidget(incidence_angle_label, 1, 0)
        self.incidence_angle_slider = QSlider(Qt.Horizontal)
        self.incidence_angle_slider.setMinimum(0)
        self.incidence_angle_slider.setMaximum(90)
        self.incidence_angle_slider.setValue(30)
        self.incidence_angle_slider.valueChanged.connect(self.update_label)
        param_layout.addWidget(self.incidence_angle_slider, 1, 1)
        self.incidence_angle_display = QLabel(f"{self.incidence_angle_slider.value()}°")
        self.incidence_angle_display.setStyleSheet("font-size: 20px; font-weight: bold; color: #003366;")
        param_layout.addWidget(self.incidence_angle_display, 1, 2)

        # 光轴方向动态调整
        axis_angle_label = QLabel("光轴方向 (度):")
        axis_angle_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #003366;")
        param_layout.addWidget(axis_angle_label, 2, 0)
        self.axis_angle_slider = QSlider(Qt.Horizontal)
        self.axis_angle_slider.setMinimum(0)
        self.axis_angle_slider.setMaximum(90)
        self.axis_angle_slider.setValue(0)
        self.axis_angle_slider.valueChanged.connect(self.update_label)
        param_layout.addWidget(self.axis_angle_slider, 2, 1)
        self.axis_angle_display = QLabel(f"{self.axis_angle_slider.value()}°")
        self.axis_angle_display.setStyleSheet("font-size: 20px; font-weight: bold; color: #003366;")
        param_layout.addWidget(self.axis_angle_display, 2, 2)

        # 计算结果按钮
        self.calculate_button = QPushButton("开始实验")
        self.calculate_button.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px; background-color: #003366; color: #ffffff; border-radius: 8px;")
        self.calculate_button.clicked.connect(self.calculate_results)
        param_layout.addWidget(self.calculate_button, 4, 0, 1, 3)

        # 计算结果显示框架
        self.result_frame = QFrame()
        self.setup_frame_style(self.result_frame)
        right_layout.addWidget(self.result_frame)
        result_layout = QVBoxLayout(self.result_frame)
        self.result_display = QLabel("结果显示:\n折射角o光: \n折射角e光:")
        self.result_display.setStyleSheet("font-size: 20px; font-weight: bold; color: #003366; padding: 10px;")
        result_layout.addWidget(self.result_display)

        # 保存图片和退出按钮
        save_exit_layout = QHBoxLayout()
        right_layout.addLayout(save_exit_layout)
        self.save_button = QPushButton("保存图片")
        self.save_button.setStyleSheet("font-size: 20px; font-weight: bold; padding: 8px; background-color: #0055cc; color: #ffffff;")
        self.save_button.clicked.connect(self.save_image)
        save_exit_layout.addWidget(self.save_button)

        self.exit_button = QPushButton("退出")
        self.exit_button.setStyleSheet("font-size: 20px; font-weight: bold; padding: 8px; background-color: #cc0000; color: #ffffff;")
        self.exit_button.clicked.connect(self.close)
        save_exit_layout.addWidget(self.exit_button)

    def update_label(self):
        # 更新入射角和光轴角的显示值
        self.incidence_angle_display.setText(f"{self.incidence_angle_slider.value()}°")
        self.axis_angle_display.setText(f"{self.axis_angle_slider.value()}°")

    def calculate_results(self):
        material = self.material_combo.currentText()
        # 获取折射率数据
        no = crystal_data[material]["no"]
        ne = crystal_data[material]["ne"]
        # 获取入射角和光轴角
        incidence_angle_deg = self.incidence_angle_slider.value()
        incidence_angle = np.radians(incidence_angle_deg)
        axis_angle_deg = self.axis_angle_slider.value()
        axis_angle = np.radians(axis_angle_deg)
        # **o光**：遵循斯涅尔定律
        o_angle = np.arcsin(np.sin(incidence_angle) / no)
        # **e光**：折射率根据光轴角度变化
        ne_effective = ne / np.sqrt(1 + (np.tan(axis_angle) ** 2))  # 简化模型
        e_angle = np.arcsin(np.sin(incidence_angle) / ne_effective)
        # 更新结果显示
        self.result_display.setText(f"结果显示:\n折射角o光: {np.degrees(o_angle):.2f}°\n折射角e光: {np.degrees(e_angle):.2f}°\n光轴方向: {axis_angle_deg}°")
        # 更新仿真图形
        self.update_simulation(incidence_angle, o_angle, e_angle)

    def update_simulation(self, incidence_angle, o_angle, e_angle):
        self.ax.clear()
        
        # 绘制入射光源，入射光角度应随入射角度变化
        self.ax.plot([-2 * np.cos(incidence_angle), 0], [2 * np.sin(incidence_angle), 0], label="入射光", color='#003366', linewidth=3)
        self.ax.scatter([-2 * np.cos(incidence_angle)], [2 * np.sin(incidence_angle)], color='#003366', s=200, label="光源")

        # 绘制晶体
        crystal = Rectangle((0, -1), 1, 2, fill=False, edgecolor='black', linewidth=2, label="晶体")
        self.ax.add_patch(crystal)

        # 绘制o光和e光的折射路径
        self.ax.plot([0, 1 * np.cos(o_angle)], [0, 1 * np.sin(o_angle)], label="o光", color='#0066cc', linewidth=2)
        self.ax.scatter([1 * np.cos(o_angle)], [1 * np.sin(o_angle)], color='#0066cc', s=100)

        self.ax.plot([0, 1 * np.cos(e_angle)], [0, 1 * np.sin(e_angle)], label="e光", color='#ff9900', linewidth=2)
        self.ax.scatter([1 * np.cos(e_angle)], [1 * np.sin(e_angle)], color='#ff9900', s=100)

        # 绘制出射光线
        self.ax.plot([1 * np.cos(o_angle), 2 * np.cos(o_angle)], [1 * np.sin(o_angle), 2 * np.sin(o_angle)], color='#0066cc', linestyle='--', linewidth=2, label="出射光 (o光)")
        self.ax.plot([1 * np.cos(e_angle), 2 * np.cos(e_angle)], [1 * np.sin(e_angle), 2 * np.sin(e_angle)], color='#ff9900', linestyle='--', linewidth=2, label="出射光 (e光)")

        # 添加图例
        self.ax.legend()

        # 设置图形界限和标签
        self.ax.set_xlim(-2.5, 2)
        self.ax.set_ylim(-2, 2)
        self.ax.set_xlabel("X轴", fontsize=16)
        self.ax.set_ylabel("Y轴", fontsize=16)
        self.ax.set_title("晶体双折射现象", fontsize=20, color='#003366')

        # 显示光的折射情况
        self.canvas.draw()

    # 改变原理图颜色
    def change_principle_image_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.principle_img.setStyleSheet(f"background-color: {color.name()};")

    # 保存图片功能
    def save_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "保存图片", "", "PNG Files (*.png);;JPEG Files (*.jpg)", options=options)
        if file_name:
            self.figure.savefig(file_name)

# 应用程序启动
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BirefringenceExperiment()
    window.show()
    sys.exit(app.exec_())