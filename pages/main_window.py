import os
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# 导入页面类
from pages.navigation_page import NavigationPage
from pages.music_page import MusicPage
from pages.phone_page import PhonePage
from pages.home_page import HomePage


class MainWindow(QWidget):
    def __init__(self, username="用户"):
        super().__init__()
        self.username = username
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f'智慧座舱系统 - 欢迎，{self.username}')
        self.setFixedSize(1000, 800)
        self.setWindowIcon(QIcon('../data/img/icon.png'))

        # 创建主水平布局
        main_layout = QHBoxLayout()

        # 左侧按钮布局
        left_layout = self.create_left_buttons()

        # 右侧堆叠窗口
        self.stacked_widget = QStackedWidget()
        self.create_pages()

        # 将左右两部分添加到主布局
        main_layout.addLayout(left_layout, 1)
        main_layout.addWidget(self.stacked_widget, 6)

        self.setLayout(main_layout)

    def create_left_buttons(self):
        """创建左侧竖向按钮"""
        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignTop)

        # 用户信息显示
        user_label = QLabel(f'欢迎，{self.username}')
        user_label.setFont(QFont('Arial', 12, QFont.Bold))
        user_label.setAlignment(Qt.AlignCenter)
        user_label.setStyleSheet("""
            background-color: #3498db;
            color: white;
            padding: 10px;
            border-radius: 5px;
            margin: 5px;
        """)
        left_layout.addWidget(user_label)

        # 创建按钮
        btn_home = QPushButton('首页')
        btn_nav = QPushButton('导航')
        btn_music = QPushButton('音乐')
        btn_phone = QPushButton('电话')
        btn_logout = QPushButton('退出登录')

        # 设置按钮样式
        buttons = [btn_home, btn_nav, btn_music, btn_phone, btn_logout]
        for btn in buttons:
            btn.setFixedHeight(60)
            btn.setFont(QFont('Arial', 12))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #f0f0f0;
                    border: 2px solid #ccc;
                    border-radius: 5px;
                    margin: 5px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
            """)

        # 退出登录按钮特殊样式
        btn_logout.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: 2px solid #c0392b;
                border-radius: 5px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """)

        # 连接按钮信号
        btn_home.clicked.connect(lambda: self.switch_page(3))
        btn_nav.clicked.connect(lambda: self.switch_page(0))
        btn_music.clicked.connect(lambda: self.switch_page(1))
        btn_phone.clicked.connect(lambda: self.switch_page(2))
        btn_logout.clicked.connect(self.logout)

        # 添加到布局
        left_layout.addWidget(btn_home)
        left_layout.addWidget(btn_nav)
        left_layout.addWidget(btn_music)
        left_layout.addWidget(btn_phone)
        left_layout.addStretch()
        left_layout.addWidget(btn_logout)

        return left_layout

    def create_pages(self):
        """创建堆叠页面"""
        # 创建各个页面实例
        nav_page = NavigationPage()
        music_page = MusicPage()
        phone_page = PhonePage()
        home_page = HomePage(self.username)

        # 将所有页面添加到堆叠窗口
        self.stacked_widget.addWidget(nav_page)  # 索引 0
        self.stacked_widget.addWidget(music_page)  # 索引 1
        self.stacked_widget.addWidget(phone_page)  # 索引 2
        self.stacked_widget.addWidget(home_page)  # 索引 3

        # 默认显示首页
        self.stacked_widget.setCurrentIndex(3)

    def switch_page(self, index):
        """切换页面"""
        self.stacked_widget.setCurrentIndex(index)

    def logout(self):
        """退出登录"""
        reply = QMessageBox.question(self, '确认退出',
                                     '确定要退出登录吗？',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            from login_window import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()
            self.close()