import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QHBoxLayout, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from pages.DB_util import DButil
from pages.login_window import LoginWindow


class RegisterWindow(QWidget):
    reg2logSignal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('用户注册 - 智慧座舱系统')
        self.setFixedSize(700, 600)
        self.setWindowIcon(QIcon('../img/icon.png'))

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        # 标题
        title = QLabel('用户注册')
        title.setFont(QFont('Arial', 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        # 注册表单
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)

        # 用户名输入
        username_label = QLabel('用户名:')
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('请输入用户名（3-20位字符）')

        # 密码输入
        password_label = QLabel('密码:')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('请输入密码（至少6位）')
        self.password_input.setEchoMode(QLineEdit.Password)

        # 确认密码
        confirm_label = QLabel('确认密码:')
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText('请再次输入密码')
        self.confirm_input.setEchoMode(QLineEdit.Password)

        # 按钮布局
        button_layout = QHBoxLayout()

        self.register_btn = QPushButton('注册')
        self.register_btn.setObjectName('register_btn')
        self.register_btn.clicked.connect(self.register)

        self.back_btn = QPushButton('返回登录')
        self.back_btn.setObjectName('back_btn')
        self.back_btn.clicked.connect(self.back_to_login)

        button_layout.addWidget(self.register_btn)
        button_layout.addWidget(self.back_btn)

        # 添加到表单布局
        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(confirm_label)
        form_layout.addWidget(self.confirm_input)
        form_layout.addLayout(button_layout)

        # 添加到主布局
        layout.addWidget(title)
        layout.addStretch(1)
        layout.addLayout(form_layout)
        layout.addStretch(2)

        self.setLayout(layout)

    def register(self):
        """处理注册"""
        db = DButil()

        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        confirm_password = self.confirm_input.text().strip()

        # 验证输入
        if not username or not password or not confirm_password:
            QMessageBox.warning(self, '输入错误', '请填写所有必填字段！')
            return

        if len(username) < 3 or len(username) > 20:
            QMessageBox.warning(self, '输入错误', '用户名长度应为3-20位字符！')
            return

        if len(password) < 6:
            QMessageBox.warning(self, '输入错误', '密码长度至少为6位！')
            return

        if password != confirm_password:
            QMessageBox.warning(self, '输入错误', '两次输入的密码不一致！')
            return

        if db.user_register(username, password):
            QMessageBox.information(self, '注册成功', f'用户 {username} 注册成功！\n请返回登录页面登录。')
            self.back_to_login()

    def back_to_login(self):
        """返回登录页面"""
        self.reg2logSignal.emit()