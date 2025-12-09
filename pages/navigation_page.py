from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class NavigationPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 导航页面内容
        nav_title = QLabel('导航系统')
        nav_title.setFont(QFont('Arial', 20, QFont.Bold))
        nav_title.setAlignment(Qt.AlignCenter)

        map_widget = QLabel('这里显示地图')
        map_widget.setStyleSheet("""
            background-color: #e8f4f8;
            border: 2px solid #3498db;
            border-radius: 10px;
            min-height: 300px;
        """)
        map_widget.setAlignment(Qt.AlignCenter)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('输入目的地...')
        search_btn = QPushButton('搜索')
        search_btn.clicked.connect(self.search_destination)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)

        layout.addWidget(nav_title)
        layout.addWidget(map_widget)
        layout.addLayout(search_layout)

        self.setLayout(layout)

    def search_destination(self):
        """搜索目的地"""
        destination = self.search_input.text()
        if destination:
            print(f"搜索目的地: {destination}")
            # 这里可以添加实际的搜索逻辑