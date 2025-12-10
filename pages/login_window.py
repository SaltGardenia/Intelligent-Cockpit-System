import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QHBoxLayout, QMessageBox, QCheckBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from pages.DB_util import DButil


class LoginWindow(QWidget):
    login_successful = pyqtSignal(str)  # 登录成功信号，传递用户名

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('用户登录 - 智慧座舱系统')
        self.setFixedSize(700, 600)
        self.setWindowIcon(QIcon('../data/img/icon.png'))

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        # 标题
        title = QLabel('智慧座舱系统')
        title.setFont(QFont('Arial', 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel('用户登录')
        subtitle.setFont(QFont('Arial', 16))
        subtitle.setAlignment(Qt.AlignCenter)

        # 登录表单
        form_layout = QVBoxLayout()
        form_layout.setSpacing(35)

        # 用户名输入
        username_label = QLabel('用户名:')
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('请输入用户名')

        # 密码输入
        password_label = QLabel('密码:')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('请输入密码')
        self.password_input.setEchoMode(QLineEdit.Password)

        # 登录按钮
        self.login_btn = QPushButton('登录')
        self.login_btn.setObjectName('login_btn')
        self.login_btn.clicked.connect(self.login)

        # 注册按钮
        self.register_btn = QPushButton('注册新账号')
        self.register_btn.setObjectName('register_btn')
        self.register_btn.clicked.connect(self.show_register)

        # 添加到表单布局
        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.login_btn)
        form_layout.addWidget(self.register_btn)

        # 添加到主布局
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch(1)
        layout.addLayout(form_layout)
        layout.addStretch(2)

        self.setLayout(layout)


    def login(self):
        """处理登录"""
        db = DButil()

        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, '输入错误', '请输入用户名和密码！')
            return

        if db.user_login(username, password):
            self.login_successful.emit(username)
        else:
            QMessageBox.critical(self, '登录失败', '用户名或密码错误！')


    def show_register(self):
        """显示注册窗口"""
        from pages.register_window import RegisterWindow

        self.register_window = RegisterWindow()
        self.register_window.reg2logSignal.connect(self.reg2log)
        self.register_window.show()
        self.hide()

    def reg2log(self):
        self.register_window.hide()
        self.show()