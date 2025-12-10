import os
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtMultimediaWidgets import QVideoWidget


class MusicPage(QWidget):
    def __init__(self, music_folder='data/music'):
        super().__init__()
        self.music_folder = os.path.abspath(music_folder)  # 获取绝对路径
        self.current_song = None
        self.is_playing = False
        self.music_files = []  # 存储音乐文件信息

        # 初始化媒体播放器
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)

        # 连接信号
        self.player.stateChanged.connect(self.on_state_changed)
        self.player.positionChanged.connect(self.on_position_changed)
        self.player.durationChanged.connect(self.on_duration_changed)
        self.player.error.connect(self.on_player_error)

        self.initUI()
        self.load_music_files()

    def initUI(self):
        layout = QVBoxLayout()

        # 音乐页面标题
        music_title = QLabel('音乐播放器')
        music_title.setFont(QFont('Arial', 20, QFont.Bold))
        music_title.setAlignment(Qt.AlignCenter)
        music_title.setStyleSheet("color: #2c3e50; padding: 10px;")

        # 当前播放信息
        self.current_song_label = QLabel('当前未播放')
        self.current_song_label.setFont(QFont('Arial', 12))
        self.current_song_label.setAlignment(Qt.AlignCenter)
        self.current_song_label.setStyleSheet("color: #3498db; padding: 5px;")

        # 歌曲列表
        self.song_list = QListWidget()
        self.song_list.setFont(QFont('Arial', 10))
        self.song_list.setStyleSheet("""
            QListWidget {
                background-color: #ecf0f1;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #bdc3c7;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        self.song_list.itemDoubleClicked.connect(self.select_and_play_song)
        self.song_list.itemClicked.connect(self.select_song)

        # 进度条
        self.progress_slider = QSlider(Qt.Horizontal)
        self.progress_slider.setRange(0, 100)
        self.progress_slider.sliderMoved.connect(self.seek_position)
        self.progress_slider.sliderPressed.connect(self.slider_pressed)
        self.progress_slider.sliderReleased.connect(self.slider_released)

        # 时间标签
        time_layout = QHBoxLayout()
        self.current_time_label = QLabel('00:00')
        self.total_time_label = QLabel('00:00')
        self.current_time_label.setAlignment(Qt.AlignLeft)
        self.total_time_label.setAlignment(Qt.AlignRight)

        time_layout.addWidget(self.current_time_label)
        time_layout.addStretch()
        time_layout.addWidget(self.total_time_label)

        # 音量控制
        volume_layout = QHBoxLayout()
        volume_label = QLabel('音量:')
        volume_label.setFont(QFont('Arial', 10))

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(70)
        self.volume_slider.valueChanged.connect(self.set_volume)
        self.player.setVolume(70)

        self.volume_value_label = QLabel('70%')
        self.volume_value_label.setFixedWidth(40)

        volume_layout.addWidget(volume_label)
        volume_layout.addWidget(self.volume_slider)
        volume_layout.addWidget(self.volume_value_label)

        # 播放控制按钮
        control_layout = QHBoxLayout()

        # 按钮样式
        button_style = """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1c6ea4;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """

        self.prev_btn = QPushButton('⏮ 上一首')
        self.play_btn = QPushButton('▶ 播放')
        self.pause_btn = QPushButton('⏸ 暂停')
        self.next_btn = QPushButton('⏭ 下一首')
        self.stop_btn = QPushButton('⏹ 停止')

        for btn in [self.prev_btn, self.play_btn, self.pause_btn, self.next_btn, self.stop_btn]:
            btn.setStyleSheet(button_style)
            btn.setCursor(Qt.PointingHandCursor)

        self.prev_btn.clicked.connect(self.prev_song)
        self.play_btn.clicked.connect(self.play_music)
        self.pause_btn.clicked.connect(self.pause_music)
        self.next_btn.clicked.connect(self.next_song)
        self.stop_btn.clicked.connect(self.stop_music)

        # 设置按钮大小
        for btn in [self.prev_btn, self.play_btn, self.pause_btn, self.next_btn, self.stop_btn]:
            btn.setFixedHeight(35)

        # 刷新按钮
        refresh_btn = QPushButton('🔄 刷新列表')
        refresh_btn.setStyleSheet(button_style.replace('#3498db', '#27ae60'))
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.clicked.connect(self.refresh_music_list)
        refresh_btn.setFixedHeight(35)

        control_layout.addStretch()
        control_layout.addWidget(self.prev_btn)
        control_layout.addWidget(self.play_btn)
        control_layout.addWidget(self.pause_btn)
        control_layout.addWidget(self.next_btn)
        control_layout.addWidget(self.stop_btn)
        control_layout.addWidget(refresh_btn)
        control_layout.addStretch()

        # 播放模式
        mode_layout = QHBoxLayout()
        mode_label = QLabel('播放模式:')
        self.play_mode = QComboBox()
        self.play_mode.addItems(['顺序播放', '单曲循环', '随机播放'])
        self.play_mode.currentIndexChanged.connect(self.change_play_mode)

        # 文件数量显示
        self.file_count_label = QLabel('共加载 0 首歌曲')
        self.file_count_label.setStyleSheet("color: #e74c3c; font-weight: bold;")

        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.play_mode)
        mode_layout.addStretch()
        mode_layout.addWidget(self.file_count_label)

        # 添加到主布局
        layout.addWidget(music_title)
        layout.addWidget(self.current_song_label)
        layout.addWidget(self.song_list)
        layout.addLayout(time_layout)
        layout.addWidget(self.progress_slider)
        layout.addLayout(volume_layout)
        layout.addLayout(control_layout)
        layout.addLayout(mode_layout)

        self.setLayout(layout)

        # 初始状态
        self.update_button_states()

        # 用于跟踪滑块是否被拖动
        self.slider_is_dragging = False

    def load_music_files(self):
        """加载音乐文件夹中的MP3文件"""
        print(f"正在扫描文件夹: {self.music_folder}")

        # 清空现有列表
        self.song_list.clear()
        self.playlist.clear()
        self.music_files.clear()

        if not os.path.exists(self.music_folder):
            error_msg = f"错误: 音乐文件夹 '{self.music_folder}' 不存在!"
            print(error_msg)
            self.current_song_label.setText(error_msg)
            self.file_count_label.setText('文件夹不存在')
            return

        # 支持的音频格式
        supported_formats = ['.mp3', '.wav', '.ogg', '.flac', '.m4a', '.wma']

        # 扫描文件夹中的音乐文件
        for file in os.listdir(self.music_folder):
            file_path = os.path.join(self.music_folder, file)

            # 检查是否是文件并且是支持的格式
            if os.path.isfile(file_path):
                file_lower = file.lower()
                if any(file_lower.endswith(ext) for ext in supported_formats):
                    # 去除扩展名作为歌名
                    song_name = os.path.splitext(file)[0]

                    # 存储文件信息
                    self.music_files.append({
                        'name': song_name,
                        'file': file,
                        'path': file_path
                    })

        # 按文件名排序
        self.music_files.sort(key=lambda x: x['name'])

        # 添加到UI列表和播放列表
        for music_info in self.music_files:
            # 添加到UI列表
            self.song_list.addItem(music_info['name'])

            # 添加到播放列表
            url = QUrl.fromLocalFile(music_info['path'])
            self.playlist.addMedia(QMediaContent(url))

        # 更新文件数量显示
        count = len(self.music_files)
        self.file_count_label.setText(f'共加载 {count} 首歌曲')

        if count > 0:
            self.song_list.setCurrentRow(0)
            self.current_song = self.music_files[0]['name']
            self.current_song_label.setText(f"准备播放: {self.current_song}")
            print(f"成功加载 {count} 首歌曲")
        else:
            self.current_song_label.setText("文件夹中没有找到音乐文件")
            print("文件夹中没有找到音乐文件")

    def select_song(self, item):
        """选择歌曲（不立即播放）"""
        row = self.song_list.row(item)
        if 0 <= row < len(self.music_files):
            self.playlist.setCurrentIndex(row)
            self.current_song = self.music_files[row]['name']
            self.current_song_label.setText(f"已选择: {self.current_song}")
            print(f"选择歌曲: {self.current_song}")

    def select_and_play_song(self, item):
        """双击选择并播放歌曲"""
        row = self.song_list.row(item)
        if 0 <= row < len(self.music_files):
            self.playlist.setCurrentIndex(row)
            self.current_song = self.music_files[row]['name']
            self.current_song_label.setText(f"正在播放: {self.current_song}")
            print(f"播放歌曲: {self.current_song}")
            self.play_music()

    def play_music(self):
        """播放音乐"""
        if self.playlist.mediaCount() == 0:
            self.current_song_label.setText("没有可播放的歌曲")
            return

        if self.player.state() != QMediaPlayer.PlayingState:
            if self.player.state() == QMediaPlayer.StoppedState:
                # 如果没有当前索引，从第一首开始
                if self.playlist.currentIndex() == -1:
                    self.playlist.setCurrentIndex(0)
                    if self.playlist.currentIndex() >= 0:
                        self.current_song = self.music_files[self.playlist.currentIndex()]['name']
                        self.current_song_label.setText(f"正在播放: {self.current_song}")

            self.player.play()
            self.is_playing = True
            print(f"播放: {self.current_song}")

    def pause_music(self):
        """暂停音乐"""
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.is_playing = False
            self.current_song_label.setText(f"已暂停: {self.current_song}")
            print("音乐暂停")

    def stop_music(self):
        """停止音乐"""
        self.player.stop()
        self.is_playing = False
        self.progress_slider.setValue(0)
        self.current_time_label.setText('00:00')
        if self.current_song:
            self.current_song_label.setText(f"已停止: {self.current_song}")
        print("音乐停止")

    def next_song(self):
        """下一首"""
        if self.playlist.mediaCount() == 0:
            return

        current_index = self.playlist.currentIndex()
        if current_index < self.playlist.mediaCount() - 1:
            self.playlist.next()
        else:
            self.playlist.setCurrentIndex(0)  # 循环到第一首

        # 更新UI选择
        new_index = self.playlist.currentIndex()
        self.song_list.setCurrentRow(new_index)
        if 0 <= new_index < len(self.music_files):
            self.current_song = self.music_files[new_index]['name']
            self.current_song_label.setText(f"正在播放: {self.current_song}")

        # 如果当前正在播放，继续播放
        if self.is_playing:
            self.player.play()

    def prev_song(self):
        """上一首"""
        if self.playlist.mediaCount() == 0:
            return

        current_index = self.playlist.currentIndex()
        if current_index > 0:
            self.playlist.previous()
        else:
            self.playlist.setCurrentIndex(self.playlist.mediaCount() - 1)  # 循环到最后一首

        # 更新UI选择
        new_index = self.playlist.currentIndex()
        self.song_list.setCurrentRow(new_index)
        if 0 <= new_index < len(self.music_files):
            self.current_song = self.music_files[new_index]['name']
            self.current_song_label.setText(f"正在播放: {self.current_song}")

        # 如果当前正在播放，继续播放
        if self.is_playing:
            self.player.play()

    def set_volume(self, value):
        """设置音量"""
        self.player.setVolume(value)
        self.volume_value_label.setText(f'{value}%')

    def seek_position(self, position):
        """跳转到指定位置"""
        if self.player.duration() > 0:
            new_position = int((position / 100) * self.player.duration())
            self.player.setPosition(new_position)

    def slider_pressed(self):
        """滑块按下时"""
        self.slider_is_dragging = True

    def slider_released(self):
        """滑块释放时"""
        self.slider_is_dragging = False

    def on_state_changed(self, state):
        """播放状态改变时的处理"""
        self.update_button_states()

    def on_position_changed(self, position):
        """播放位置改变时的处理"""
        if self.player.duration() > 0 and not self.slider_is_dragging:
            # 更新进度条
            progress = int((position / self.player.duration()) * 100)
            self.progress_slider.setValue(progress)

            # 更新时间显示
            self.current_time_label.setText(self.format_time(position))

    def on_duration_changed(self, duration):
        """歌曲时长改变时的处理"""
        if duration > 0:
            self.total_time_label.setText(self.format_time(duration))

    def on_player_error(self, error):
        """播放器错误处理"""
        error_msg = f"播放错误: {self.player.errorString()}"
        print(error_msg)
        self.current_song_label.setText(error_msg)

    def format_time(self, milliseconds):
        """将毫秒转换为 MM:SS 格式"""
        seconds = milliseconds // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def change_play_mode(self, index):
        """改变播放模式"""
        if index == 0:  # 顺序播放
            self.playlist.setPlaybackMode(QMediaPlaylist.Sequential)
        elif index == 1:  # 单曲循环
            self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
        elif index == 2:  # 随机播放
            self.playlist.setPlaybackMode(QMediaPlaylist.Random)

    def refresh_music_list(self):
        """刷新音乐列表"""
        print("刷新音乐列表...")
        self.load_music_files()

    def update_button_states(self):
        """更新按钮状态"""
        state = self.player.state()

        self.play_btn.setEnabled(state != QMediaPlayer.PlayingState)
        self.pause_btn.setEnabled(state == QMediaPlayer.PlayingState)
        self.stop_btn.setEnabled(state != QMediaPlayer.StoppedState)
        self.prev_btn.setEnabled(self.playlist.mediaCount() > 0)
        self.next_btn.setEnabled(self.playlist.mediaCount() > 0)


# 测试代码
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    # 设置应用程序样式
    app.setStyle('Fusion')

    # 创建主窗口
    main_window = QWidget()
    main_layout = QVBoxLayout()

    # 创建音乐播放器页面
    player = MusicPage("../data/music")  # 使用当前目录下的data.music文件夹

    # 添加到主窗口
    main_layout.addWidget(player)
    main_window.setLayout(main_layout)

    # 设置窗口属性
    main_window.setWindowTitle("音乐播放器 - 自动读取MP3文件")
    main_window.setGeometry(300, 200, 800, 600)
    main_window.show()

    sys.exit(app.exec_())