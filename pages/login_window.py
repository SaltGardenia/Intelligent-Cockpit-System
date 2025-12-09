import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QHBoxLayout, QMessageBox, QCheckBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon


class LoginWindow(QWidget):
    login_successful = pyqtSignal(str)  # 登录成功信号，传递用户名

    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_user_data()

    def initUI(self):
        self.setWindowTitle('用户登录 - 智慧座舱系统')
        self.setFixedSize(700, 600)
        self.setWindowIcon(QIcon('../img/icon.png'))

        # 设置窗口样式
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }
            QLabel {
                color: white;
                font-family: Arial;
            }
            QLineEdit {
                padding: 12px;
                border: 2px solid #ddd;
                border-radius: 8px;
                font-size: 14px;
                background: white;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
            QPushButton {
                padding: 12px;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                color: white;
            }
            QPushButton#login_btn {
                background: #2ecc71;
            }
            QPushButton#login_btn:hover {
                background: #27ae60;
            }
            QPushButton#register_btn {
                background: #3498db;
            }
            QPushButton#register_btn:hover {
                background: #2980b9;
            }
        """)

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
        form_layout.setSpacing(15)

        # 用户名输入
        username_label = QLabel('用户名:')
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('请输入用户名')

        # 密码输入
        password_label = QLabel('密码:')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('请输入密码')
        self.password_input.setEchoMode(QLineEdit.Password)

        # 记住密码复选框
        self.remember_check = QCheckBox('记住密码')
        self.remember_check.setStyleSheet("color: white;")

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
        form_layout.addWidget(self.remember_check)
        form_layout.addWidget(self.login_btn)
        form_layout.addWidget(self.register_btn)

        # 添加到主布局
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch(1)
        layout.addLayout(form_layout)
        layout.addStretch(2)

        self.setLayout(layout)

    def load_user_data(self):
        """加载保存的用户数据"""
        try:
            # 这里可以从文件或数据库中加载保存的用户信息
            # 示例：从配置文件读取
            self.username_input.setText('admin')  # 示例默认用户名
        except:
            pass

    def login(self):
        """处理登录"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, '输入错误', '请输入用户名和密码！')
            return

        # 简单的验证逻辑（实际应用中应该连接数据库）
        if self.verify_credentials(username, password):
            # 登录成功
            if self.remember_check.isChecked():
                self.save_user_data(username)

            self.login_successful.emit(username)
        else:
            QMessageBox.critical(self, '登录失败', '用户名或密码错误！')

    def verify_credentials(self, username, password):
        """验证用户凭据"""
        # 简单的验证逻辑，实际应用中应该连接数据库
        # 这里使用硬编码的测试账号
        valid_users = {
            'admin': '123456',
            'user': 'password',
            'test': 'test123'
        }
        return valid_users.get(username) == password

    def save_user_data(self, username):
        """保存用户数据"""
        # 这里可以保存到文件或数据库
        print(f"保存用户数据: {username}")

    def show_register(self):
        """显示注册窗口"""
        from register_window import RegisterWindow
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.hide()