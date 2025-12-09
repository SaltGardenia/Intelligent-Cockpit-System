from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class PhonePage(QWidget):
    def __init__(self):
        super().__init__()
        self.phone_number = ""
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 电话页面内容
        phone_title = QLabel('电话')
        phone_title.setFont(QFont('Arial', 20, QFont.Bold))
        phone_title.setAlignment(Qt.AlignCenter)

        # 号码显示
        self.number_display = QLineEdit()
        self.number_display.setPlaceholderText('输入电话号码...')
        self.number_display.setAlignment(Qt.AlignCenter)
        self.number_display.setFont(QFont('Arial', 16))

        # 拨号盘
        dial_layout = QGridLayout()
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#']
        positions = [(i, j) for i in range(4) for j in range(3)]

        for position, number in zip(positions, numbers):
            btn = QPushButton(number)
            btn.setFixedSize(60, 60)
            btn.setFont(QFont('Arial', 16))
            btn.clicked.connect(lambda checked, num=number: self.add_number(num))
            dial_layout.addWidget(btn, *position)

        # 通话按钮
        call_layout = QHBoxLayout()
        call_btn = QPushButton('拨打')
        end_btn = QPushButton('挂断')
        clear_btn = QPushButton('清除')

        call_btn.clicked.connect(self.make_call)
        end_btn.clicked.connect(self.end_call)
        clear_btn.clicked.connect(self.clear_number)

        call_layout.addWidget(call_btn)
        call_layout.addWidget(end_btn)
        call_layout.addWidget(clear_btn)

        layout.addWidget(phone_title)
        layout.addWidget(self.number_display)
        layout.addLayout(dial_layout)
        layout.addLayout(call_layout)

        self.setLayout(layout)

    def add_number(self, number):
        """添加数字到电话号码"""
        self.phone_number += number
        self.number_display.setText(self.phone_number)

    def clear_number(self):
        """清除电话号码"""
        self.phone_number = ""
        self.number_display.clear()

    def make_call(self):
        """拨打电话"""
        if self.phone_number:
            print(f"正在呼叫: {self.phone_number}")

    def end_call(self):
        """结束通话"""
        print("通话结束")
        self.phone_number = ""
        self.number_display.clear()