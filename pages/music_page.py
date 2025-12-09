from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class MusicPage(QWidget):
    def __init__(self):
        super().__init__()
        self.current_song = None
        self.is_playing = False
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 音乐页面内容
        music_title = QLabel('音乐播放器')
        music_title.setFont(QFont('Arial', 20, QFont.Bold))
        music_title.setAlignment(Qt.AlignCenter)

        # 歌曲列表
        self.song_list = QListWidget()
        songs = ['歌曲1 - 艺术家1', '歌曲2 - 艺术家2', '歌曲3 - 艺术家3', '歌曲4 - 艺术家4', '歌曲5 - 艺术家5']
        self.song_list.addItems(songs)
        self.song_list.itemClicked.connect(self.select_song)

        # 播放控制
        control_layout = QHBoxLayout()
        self.play_btn = QPushButton('播放')
        self.pause_btn = QPushButton('暂停')
        self.next_btn = QPushButton('下一首')
        self.prev_btn = QPushButton('上一首')

        self.play_btn.clicked.connect(self.play_music)
        self.pause_btn.clicked.connect(self.pause_music)
        self.next_btn.clicked.connect(self.next_song)
        self.prev_btn.clicked.connect(self.prev_song)

        control_layout.addWidget(self.prev_btn)
        control_layout.addWidget(self.play_btn)
        control_layout.addWidget(self.pause_btn)
        control_layout.addWidget(self.next_btn)

        layout.addWidget(music_title)
        layout.addWidget(self.song_list)
        layout.addLayout(control_layout)

        self.setLayout(layout)

    def select_song(self, item):
        """选择歌曲"""
        self.current_song = item.text()
        print(f"选择歌曲: {self.current_song}")

    def play_music(self):
        """播放音乐"""
        if self.current_song:
            self.is_playing = True
            print(f"播放: {self.current_song}")

    def pause_music(self):
        """暂停音乐"""
        if self.is_playing:
            self.is_playing = False
            print("音乐暂停")

    def next_song(self):
        """下一首"""
        current_row = self.song_list.currentRow()
        if current_row < self.song_list.count() - 1:
            self.song_list.setCurrentRow(current_row + 1)
            self.current_song = self.song_list.currentItem().text()
            print(f"切换到下一首: {self.current_song}")

    def prev_song(self):
        """上一首"""
        current_row = self.song_list.currentRow()
        if current_row > 0:
            self.song_list.setCurrentRow(current_row - 1)
            self.current_song = self.song_list.currentItem().text()
            print(f"切换到上一首: {self.current_song}")