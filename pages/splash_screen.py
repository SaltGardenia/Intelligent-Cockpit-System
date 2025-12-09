import os
import sys
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie, QFont


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口属性
        self.setWindowTitle('智慧座舱系统')
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 设置固定大小 1400×1000
        self.setFixedSize(700, 600)

        # 创建布局
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # 创建加载动画标签
        self.loading_label = QLabel()

        # 尝试加载GIF动画，如果失败则显示静态文本
        if os.path.exists('splash/video.gif'):
            self.movie = QMovie('splash/video.gif')
            self.loading_label.setMovie(self.movie)
            self.movie.start()
        else:
            # 如果没有视频文件，显示静态启动界面
            self.loading_label.setText('🚗 智慧座舱系统 🚗')
            self.loading_label.setFont(QFont('Arial', 24, QFont.Bold))
            self.loading_label.setStyleSheet("color: white;")
            self.loading_label.setAlignment(Qt.AlignCenter)

        self.loading_label.setFixedSize(700, 600)

        # 加载提示文字
        self.status_label = QLabel('系统启动中...')
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            color: white;
            font-size: 16px;
            font-family: Arial;
        """)

        layout.addWidget(self.loading_label)
        layout.addWidget(self.status_label)

        # 设置窗口样式
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2c3e50, stop:1 #3498db);
            }
        """)

        self.setLayout(layout)

        # 模拟加载进度
        self.loading_progress = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_loading)
        self.timer.start(100)

    def update_loading(self):
        """更新加载进度"""
        self.loading_progress += 10
        if self.loading_progress <= 100:
            self.status_label.setText(f'系统启动中... {self.loading_progress}%')
        else:
            self.timer.stop()