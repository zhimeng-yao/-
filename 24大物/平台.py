import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

# 导入实验模块
from 光电效应 import PhotoelectricEffectSimulator
from 晶体双折射 import BirefringenceExperiment
from 单分子双缝干涉实验 import SinglePhotonDoubleSlitSimulator
from 迈克尔逊干涉演示 import MichelsonInterferenceSimulator
from 光电效应测普朗克常量 import PlanckConstantSimulator
from 迈克尔逊干涉测量波长 import MichelsonInterferenceApp
from 实验数据处理 import DataProcessingUI
from 测光速 import MichelsonInterferenceApp as SpeedOfLightExperiment
from 测折射率 import MichelsonInterferenceApp as RefractiveIndexExperiment

class MainPlatform(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口属性
        self.setWindowTitle('基于Python的光学仿真实验平台')
        self.setGeometry(100, 100, 1200, 700)

        # 设置背景图片
        self.background_label = QLabel(self)
        pixmap = QPixmap("仿真平台.jpg")  # 替换为背景图片的路径
        self.background_label.setPixmap(pixmap)
        self.background_label.setScaledContents(True)
        self.background_label.setGeometry(0, 0, 1200, 700)

        # 主窗口部件和布局
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 顶部大标题
        title_label = QLabel('基于PYTHON的光学仿真实验平台')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: blue;
            padding: 20px;
            background-color: rgba(245, 245, 245, 0.8);
            border: 2px solid #a3c2c2;
            border-radius: 10px;
        """)
        main_layout.addWidget(title_label)

        # 水平布局：左侧功能按钮区 + 右侧简介和功能按钮
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)

        # 左侧功能按钮区（包括实验按钮的布局）
        left_layout = QVBoxLayout()
        content_layout.addLayout(left_layout)

        # 左侧主功能按钮
        self.vertical_buttons = {
            '演示实验': QPushButton('演示实验'),
            '仿真实验': QPushButton('仿真实验'),
            '数据处理': QPushButton('数据处理')
        }

        for name, btn in self.vertical_buttons.items():
            btn.setStyleSheet("""
                font-size: 22px;
                font-weight: bold;
                padding: 20px;
                background-color: rgba(200, 230, 255, 0.8);
                border: 3px solid #a3c2c2;
                border-radius: 12px;
            """)
            left_layout.addWidget(btn)

        # 实验按钮的动态显示区域
        self.experiment_button_layout = QVBoxLayout()
        left_layout.addLayout(self.experiment_button_layout)

        # 连接按钮点击事件
        self.vertical_buttons['演示实验'].clicked.connect(self.show_demo_experiment)
        self.vertical_buttons['仿真实验'].clicked.connect(self.show_simulation_experiment)
        self.vertical_buttons['数据处理'].clicked.connect(self.show_data_processing)

        # 右侧功能区布局（简介和功能按钮）
        self.right_function_layout = QVBoxLayout()
        content_layout.addLayout(self.right_function_layout)

        # 平台简介标题
        info_title = QLabel('平台简介')
        info_title.setAlignment(Qt.AlignCenter)
        info_title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #333;
            padding: 10px;
            background-color: rgba(245, 245, 245, 0.8);
            border: 2px solid #a3c2c2;
            border-radius: 10px;
        """)
        self.right_function_layout.addWidget(info_title)

        # 平台介绍详细内容
        intro_text = QTextEdit()

        # 详细的介绍内容
        platform_intro_text = """
基于Python的光学仿真实验平台提供了一个虚拟的实验环境，旨在帮助学生深入理解光学实验的基本原理和现象。平台结合了多个开源库的优势，实现了实验结果的可视化和数据处理能力。
在光学实验中，很多实验由于精度要求高、设备昂贵，常常无法大规模开展。为解决这些问题，我们设计了这个平台，学生能够在虚拟环境中完成各种复杂的实验。

主要功能模块：
1. 演示实验模块：
    该模块集成了经典的光学实验，如光电效应、迈克尔逊干涉等，用户可以通过调节实验参数，动态观察光学现象。通过动画和图像展示，学生可以更直观地理解复杂的光学现象。
    演示实验不仅提供了图形界面的可视化展示，还详细介绍了实验原理和公式推导，帮助学生从理论和实践两方面加深理解。

2. 仿真实验模块：
    仿真实验模块允许用户进行更复杂的实验操作，包括光电效应测普朗克常量、迈克尔逊干涉测光源相干长度等。通过调节实验条件，用户可以模拟不同的实验环境，并且记录数据。
    学生可以根据实验结果进行数据分析，平台提供了数据的导出功能，方便进行后续处理。

3. 数据处理模块：
    该模块为学生提供了分析实验数据的工具。用户可以导入实验数据，平台会自动生成相关图表，帮助学生进一步分析实验现象和结果。

平台的优势：
1. 免费开源：
    平台基于Python语言开发，所有代码均开源，用户可以自由下载、修改和扩展。相比于商业软件如Matlab和Zemax，平台不仅免费，还具有更强的定制能力。
  
2. 高度可扩展性：
    平台具有良好的扩展能力。由于其基于Python的开源特性，开发者可以轻松增加新的实验模块，进一步提升平台的功能。用户甚至可以根据教学需求修改代码，定制实验内容。

3. 跨平台支持：
    平台支持在不同操作系统上运行（Windows, MacOS, Linux）。Python的跨平台性使得该平台可以在各种设备上无缝运行，方便不同环境下的教学需求。

4. 虚拟实验的创新性：
    平台通过虚拟实验的方式，帮助学生通过互动式操作和参数调节更好地理解实验原理和过程。所有实验结果都通过图形化展示，帮助学生更直观地分析数据。
    此外，虚拟实验还可以避免实验设备的维护成本和使用的限制，让更多学生参与到实验中。

5. 全球共享与合作：
    本平台的开源代码已上传至GitHub，供全球开发者和教育工作者免费下载和使用。用户可以根据自身需求扩展功能，也可以共享自己的扩展成果，推动光学实验虚拟仿真的全球合作与进步。

展望：
    随着平台的不断发展，未来我们将增加更多复杂的实验模块，例如非线性光学、量子光学等。我们还计划增加测验功能，通过平台帮助学生进行知识评估。
    我们期待更多的科研人员、教育工作者参与到平台的开发中，共同推动虚拟实验技术在教育中的应用。
"""

        # 将详细介绍内容展示在界面中
        intro_text.setText(platform_intro_text)
        intro_text.setReadOnly(True)
        intro_text.setStyleSheet("""
            font-size: 24px;
            background-color: rgba(255, 255, 255, 0.9);
            border: 24px solid #a3c2c2;
            padding: 24px;
            border-radius: 24px;
        """)
        self.right_function_layout.addWidget(intro_text)

        # 添加 "进入实验" 和 "阅读原理" 按钮
        button_layout = QHBoxLayout()
        self.right_function_layout.addLayout(button_layout)

        # 进入实验按钮
        enter_button = QPushButton('进入实验')
        enter_button.setStyleSheet("""
            font-size: 22px;
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border-radius: 10px;
        """)
        button_layout.addWidget(enter_button)

        # 阅读原理按钮
        read_button = QPushButton('阅读原理')
        read_button.setStyleSheet("""
            font-size: 22px;
            padding: 10px 20px;
            background-color: #28a745;
            color: white;
            border-radius: 10px;
        """)
        button_layout.addWidget(read_button)

        # 初始化显示默认的演示实验
        self.show_demo_experiment()

    # 显示演示实验按钮的实验列表
    def show_demo_experiment(self):
        self.clear_experiment_buttons()
        # 高亮显示当前按钮
        for name, btn in self.vertical_buttons.items():
            btn.setStyleSheet("""
                font-size: 22px;
                font-weight: bold;
                padding: 20px;
                background-color: rgba(200, 230, 255, 0.8);
                border: 3px solid #a3c2c2;
                border-radius: 12px;
            """)
        self.vertical_buttons['演示实验'].setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            padding: 20px;
            background-color: rgba(100, 150, 255, 0.8);  # 高亮显示
            border: 3px solid #a3c2c2;
            border-radius: 12px;
        """)

        # 添加演示实验的实验按钮
        buttons = [
            ('单光子干涉实验', self.run_double_slit_experiment),
            ('光电效应', self.run_photoelectric_effect_experiment),
            ('晶体双折射实验', self.run_birefringence_experiment),
            ('迈克尔逊干涉实验', self.run_michelson_demo_experiment)
        ]
        for name, func in buttons:
            btn = QPushButton(name)
            btn.setStyleSheet("""
                font-size: 20px;
                padding: 15px;
                background-color: rgba(230, 242, 255, 0.8);
                border: 2px solid #a3c2c2;
                border-radius: 10px;
            """)
            btn.clicked.connect(func)
            self.experiment_button_layout.addWidget(btn)

    # 显示仿真实验按钮的实验列表，并添加两个新实验
    def show_simulation_experiment(self):
        self.clear_experiment_buttons()
        # 高亮显示当前按钮
        for name, btn in self.vertical_buttons.items():
            btn.setStyleSheet("""
                font-size: 22px;
                font-weight: bold;
                padding: 20px;
                background-color: rgba(200, 230, 255, 0.8);
                border: 3px solid #a3c2c2;
                border-radius: 12px;
            """)
        self.vertical_buttons['仿真实验'].setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            padding: 20px;
            background-color: rgba(100, 150, 255, 0.8);  # 高亮显示
            border: 3px solid #a3c2c2;
            border-radius: 12px;
        """)

        # 添加仿真实验的实验按钮
        buttons = [
            ('迈克尔逊测光的相干长度', self.run_michelson_measure_experiment),
            ('光电效应测普朗克常量', self.run_planck_experiment),
            ('基于迈克尔逊测量光速', self.run_speed_of_light_experiment),  # 新增测光速实验按钮
            ('基于迈克尔逊测量折射率', self.run_refractive_index_experiment)  # 新增测折射率实验按钮
        ]
        for name, func in buttons:
            btn = QPushButton(name)
            btn.setStyleSheet("""
                font-size: 20px;
                padding: 15px;
                background-color: rgba(230, 242, 255, 0.8);
                border: 2px solid #a3c2c2;
                border-radius: 10px;
            """)
            btn.clicked.connect(func)
            self.experiment_button_layout.addWidget(btn)

    # 显示数据处理实验按钮
    def show_data_processing(self):
        self.clear_experiment_buttons()
        # 高亮显示当前按钮
        for name, btn in self.vertical_buttons.items():
            btn.setStyleSheet("""
                font-size: 22px;
                font-weight: bold;
                padding: 20px;
                background-color: rgba(200, 230, 255, 0.8);
                border: 3px solid #a3c2c2;
                border-radius: 12px;
            """)
        self.vertical_buttons['数据处理'].setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            padding: 20px;
            background-color: rgba(100, 150, 255, 0.8);
            border: 3px solid #a3c2c2;
            border-radius: 12px;
        """)

        # 添加数据处理的实验按钮
        btn = QPushButton('处理平台')
        btn.setStyleSheet("""
            font-size: 20px;
            padding: 15px;
            background-color: rgba(230, 242, 255, 0.8);
            border: 2px solid #a3c2c2;
            border-radius: 10px;
        """)
        btn.clicked.connect(self.run_data_processing_experiment)
        self.experiment_button_layout.addWidget(btn)

    # 清空实验按钮区
    def clear_experiment_buttons(self):
        while self.experiment_button_layout.count() > 0:
            widget = self.experiment_button_layout.takeAt(0).widget()
            if widget:
                widget.setParent(None)

    # 运行单光子双缝实验
    def run_double_slit_experiment(self):
        self.experiment_window = SinglePhotonDoubleSlitSimulator()
        self.experiment_window.show()

    # 运行光电效应实验
    def run_photoelectric_effect_experiment(self):
        self.experiment_window = PhotoelectricEffectSimulator()
        self.experiment_window.show()

    # 运行晶体双折射实验
    def run_birefringence_experiment(self):
        self.experiment_window = BirefringenceExperiment()
        self.experiment_window.show()

    # 运行迈克尔逊干涉实验
    def run_michelson_demo_experiment(self):
        self.experiment_window = MichelsonInterferenceSimulator()
        self.experiment_window.show()

    # 运行光电效应测普朗克常量实验
    def run_planck_experiment(self):
        self.experiment_window = PlanckConstantSimulator()
        self.experiment_window.show()

    # 运行测光的相干长度实验
    def run_michelson_measure_experiment(self):
        self.experiment_window = MichelsonInterferenceApp()
        self.experiment_window.show()

    # 新增：运行测光速实验
    def run_speed_of_light_experiment(self):
        self.experiment_window = SpeedOfLightExperiment()
        self.experiment_window.show()

    # 新增：运行测折射率实验
    def run_refractive_index_experiment(self):
        self.experiment_window = RefractiveIndexExperiment()
        self.experiment_window.show()

    # 运行数据处理平台
    def run_data_processing_experiment(self):
        self.experiment_window = DataProcessingUI()
        self.experiment_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainPlatform()
    main_window.show()
    sys.exit(app.exec_())