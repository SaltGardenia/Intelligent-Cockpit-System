from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from datetime import datetime
import cv2
import os
import json
from pathlib import Path


class HomePage(QWidget):
    def __init__(self, username="用户"):
        super().__init__()
        self.username = username
        self.camera = None
        self.video_writer = None
        self.is_recording = False
        self.video_file_path = None
        self.photo_counter = 0
        self.video_counter = 0

        # 创建保存目录
        self.photos_dir = Path("data/photos")
        self.videos_dir = Path("data/videos")
        self.photos_dir.mkdir(exist_ok=True)
        self.videos_dir.mkdir(exist_ok=True)

        # 记录文件
        self.photos_list = self.load_photo_list()
        self.videos_list = self.load_video_list()

        self.initUI()
        self.initTimer()

    def initUI(self):
        layout = QVBoxLayout()

        # 首页内容
        home_title = QLabel(f'欢迎回来，{self.username}！')
        home_title.setFont(QFont('Arial', 24, QFont.Bold))
        home_title.setAlignment(Qt.AlignCenter)

        # 创建显示时间的Label
        self.time_label = QLabel()
        self.time_label.setFont(QFont('Arial', 16))
        self.time_label.setAlignment(Qt.AlignCenter)

        # 设置初始时间
        self.updateTime()

        # 创建原始的center_area (QLabel)
        self.center_area = QLabel()
        self.center_area.setFixedSize(800, 600)
        self.center_area.setAlignment(Qt.AlignCenter)

        # 将center_area包装在一个frame中，方便切换内容
        self.center_frame = QFrame()
        self.center_layout = QVBoxLayout(self.center_frame)
        self.center_layout.addWidget(self.center_area)
        self.center_layout.setContentsMargins(0, 0, 0, 0)

        # 按钮
        self.test_btn = QPushButton('座舱检测')
        self.line_btn = QPushButton('车道线检测')
        self.camera_btn = QPushButton('拍照')
        self.home_btn = QPushButton('首页')
        self.video_btn = QPushButton('视频列表')
        self.photo_btn = QPushButton('照片列表')
        self.info_btn = QPushButton('用户中心')

        self.btn_layout = QHBoxLayout()
        for btn in [self.test_btn, self.line_btn, self.camera_btn,
                    self.home_btn, self.video_btn, self.photo_btn,
                    self.info_btn]:
            self.btn_layout.addWidget(btn)

        self.test_btn.clicked.connect(self.test_btn_func)
        self.line_btn.clicked.connect(self.line_btn_func)
        self.camera_btn.clicked.connect(self.camera_btn_func)
        self.home_btn.clicked.connect(self.home_btn_func)
        self.video_btn.clicked.connect(self.video_btn_func)
        self.photo_btn.clicked.connect(self.photo_btn_func)
        self.info_btn.clicked.connect(self.info_btn_func)

        layout.addWidget(home_title)
        layout.addWidget(self.time_label)
        layout.addWidget(self.center_frame)  # 使用frame而不是直接使用label
        layout.addLayout(self.btn_layout)

        self.setLayout(layout)

        # 初始化显示欢迎信息
        self.center_area.setText("欢迎使用座舱检测系统")

    def initTimer(self):
        # 创建一个定时器，每秒更新一次时间
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(1000)  # 1000毫秒 = 1秒

        # 创建摄像头帧更新定时器
        self.camera_timer = QTimer()
        self.camera_timer.timeout.connect(self.updateCameraFrame)

    def updateTime(self):
        # 获取当前时间并格式化显示
        current_time = datetime.now()
        time_str = current_time.strftime("%Y年%m月%d日 %H:%M:%S")
        weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        weekday_str = weekdays[current_time.weekday()]
        self.time_label.setText(f"{time_str} {weekday_str}")

    def load_photo_list(self):
        """加载照片列表"""
        photos_json = self.photos_dir / "photos_list.json"
        if photos_json.exists():
            with open(photos_json, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def load_video_list(self):
        """加载视频列表"""
        videos_json = self.videos_dir / "videos_list.json"
        if videos_json.exists():
            with open(videos_json, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_photo_list(self):
        """保存照片列表"""
        photos_json = self.photos_dir / "photos_list.json"
        with open(photos_json, 'w', encoding='utf-8') as f:
            json.dump(self.photos_list, f, ensure_ascii=False, indent=2)

    def save_video_list(self):
        """保存视频列表"""
        videos_json = self.videos_dir / "videos_list.json"
        with open(videos_json, 'w', encoding='utf-8') as f:
            json.dump(self.videos_list, f, ensure_ascii=False, indent=2)

    def clearCenterArea(self):
        """清空center_area区域的内容"""
        # 清除center_layout中的所有widget
        for i in reversed(range(self.center_layout.count())):
            widget = self.center_layout.itemAt(i).widget()
            if widget and widget != self.center_area:  # 保留原始的center_area
                widget.setParent(None)
                widget.deleteLater()

        # 恢复原始的center_area
        if self.center_area not in [self.center_layout.itemAt(i).widget()
                                    for i in range(self.center_layout.count())]:
            self.center_layout.addWidget(self.center_area)

        # 重置center_area
        self.center_area.setPixmap(QPixmap())
        self.center_area.setText("")
        self.center_area.setAlignment(Qt.AlignCenter)

    def restoreOriginalCenterArea(self):
        """恢复原始的center_area显示"""
        self.clearCenterArea()
        self.center_area.setText("欢迎使用座舱检测系统")

    def test_btn_func(self):
        """座舱检测按钮功能 - 保持原有逻辑"""
        if self.camera is None:
            # 如果摄像头未打开，则打开摄像头并开始录像
            self.startCameraAndRecording()
        else:
            # 如果摄像头已打开，则停止摄像头
            self.stopCameraAndRecording()

    def startCameraAndRecording(self):
        """打开摄像头并开始录像"""
        try:
            self.camera = cv2.VideoCapture(0)

            if not self.camera.isOpened():
                QMessageBox.warning(self, "警告", "无法打开摄像头！")
                return

            # 清空center_area区域
            self.clearCenterArea()

            # 获取摄像头参数
            frame_width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(self.camera.get(cv2.CAP_PROP_FPS))
            if fps <= 0:
                fps = 30

            # 创建视频文件路径
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.video_file_path = self.videos_dir / f"video_{timestamp}.mp4"

            # 创建视频写入器
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.video_writer = cv2.VideoWriter(
                str(self.video_file_path),
                fourcc,
                fps,
                (frame_width, frame_height)
            )
            self.is_recording = True

            # 启动摄像头帧更新定时器
            self.camera_timer.start(30)  # 约30FPS

        except Exception as e:
            QMessageBox.critical(self, "错误", f"摄像头启动失败: {str(e)}")

    def stopCameraAndRecording(self):
        """停止摄像头和录像"""
        self.stopCamera()
        self.restoreOriginalCenterArea()

    def stopCamera(self):
        """关闭摄像头"""
        if self.camera_timer.isActive():
            self.camera_timer.stop()

        # 停止录像
        if self.is_recording and self.video_writer is not None:
            self.video_writer.release()
            self.is_recording = False

            # 保存视频记录
            if self.video_file_path and self.video_file_path.exists():
                timestamp = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
                video_info = {
                    "filename": self.video_file_path.name,
                    "path": str(self.video_file_path),
                    "timestamp": timestamp,
                    "size": self.video_file_path.stat().st_size
                }
                self.videos_list.append(video_info)
                self.save_video_list()

        if self.camera is not None:
            self.camera.release()
            self.camera = None

        self.center_area.setPixmap(QPixmap())  # 清空画面

    def updateCameraFrame(self):
        """更新摄像头画面"""
        if self.camera is None:
            return

        ret, frame = self.camera.read()
        if ret:
            # 录像
            if self.is_recording and self.video_writer is not None:
                self.video_writer.write(frame)

            # 将BGR格式转换为RGB格式
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # 调整图像大小以适应Label
            h, w, ch = frame_rgb.shape
            target_width = self.center_area.width()
            target_height = self.center_area.height()

            # 保持宽高比缩放
            if w > target_width or h > target_height:
                scale = min(target_width / w, target_height / h)
                new_w = int(w * scale)
                new_h = int(h * scale)
                frame_rgb = cv2.resize(frame_rgb, (new_w, new_h))
                h, w, ch = frame_rgb.shape

            # 转换为QImage
            bytes_per_line = ch * w
            q_img = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)

            # 创建QPixmap并显示
            pixmap = QPixmap.fromImage(q_img)
            self.center_area.setPixmap(pixmap)
            self.center_area.setAlignment(Qt.AlignCenter)
        else:
            self.center_area.setText("摄像头读取失败")

    def camera_btn_func(self):
        """拍照功能"""
        if self.camera is None:
            QMessageBox.warning(self, "警告", "请先打开摄像头！")
            return

        # 拍照
        ret, frame = self.camera.read()
        if ret:
            # 生成照片文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            photo_filename = f"photo_{timestamp}.jpg"
            photo_path = self.photos_dir / photo_filename

            # 保存照片
            cv2.imwrite(str(photo_path), frame)

            # 记录照片信息
            timestamp_str = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
            photo_info = {
                "filename": photo_filename,
                "path": str(photo_path),
                "timestamp": timestamp_str,
                "size": photo_path.stat().st_size
            }
            self.photos_list.append(photo_info)
            self.save_photo_list()

            QMessageBox.information(self, "成功", f"照片已保存: {photo_filename}")
        else:
            QMessageBox.warning(self, "警告", "拍照失败！")

    def home_btn_func(self):
        """回到首页"""
        # 关闭摄像头
        self.stopCamera()
        # 清空center_area，显示欢迎信息
        self.restoreOriginalCenterArea()

    def video_btn_func(self):
        """显示视频列表"""
        # 关闭摄像头
        self.stopCamera()

        # 清空center_area区域
        self.clearCenterArea()

        # 创建滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFixedSize(800, 600)

        # 创建容器widget
        container = QWidget()
        container_layout = QVBoxLayout(container)

        if not self.videos_list:
            no_videos_label = QLabel("暂无视频记录")
            no_videos_label.setAlignment(Qt.AlignCenter)
            no_videos_label.setStyleSheet("font-size: 20px; color: #666; margin-top: 100px;")
            container_layout.addWidget(no_videos_label)
        else:
            # 添加标题
            title_label = QLabel("视频列表")
            title_label.setAlignment(Qt.AlignCenter)
            title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px;")
            container_layout.addWidget(title_label)

            # 显示视频列表
            for i, video_info in enumerate(reversed(self.videos_list), 1):
                video_item = self.create_video_item(video_info, i)
                container_layout.addWidget(video_item)

        container_layout.addStretch()
        scroll.setWidget(container)

        # 移除原始的center_area，添加滚动区域
        self.center_layout.removeWidget(self.center_area)
        self.center_area.setParent(None)
        self.center_layout.addWidget(scroll)

    def create_video_item(self, video_info, index):
        """创建视频列表项"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Box)
        frame.setStyleSheet("""
            QFrame {
                border: 2px solid #ccc;
                border-radius: 10px;
                padding: 10px;
                margin: 5px;
                background-color: #f9f9f9;
            }
            QFrame:hover {
                background-color: #f0f0f0;
                border-color: #999;
            }
        """)

        layout = QHBoxLayout(frame)

        # 索引
        index_label = QLabel(f"{index}.")
        index_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        # 视频信息
        info_layout = QVBoxLayout()

        name_label = QLabel(f"文件名: {video_info['filename']}")
        name_label.setStyleSheet("font-size: 16px;")

        time_label = QLabel(f"拍摄时间: {video_info['timestamp']}")
        time_label.setStyleSheet("font-size: 14px; color: #666;")

        size_mb = video_info['size'] / (1024 * 1024)
        size_label = QLabel(f"文件大小: {size_mb:.2f} MB")
        size_label.setStyleSheet("font-size: 14px; color: #666;")

        info_layout.addWidget(name_label)
        info_layout.addWidget(time_label)
        info_layout.addWidget(size_label)

        # 按钮
        button_layout = QVBoxLayout()

        play_btn = QPushButton("播放")
        play_btn.setFixedSize(80, 30)
        play_btn.clicked.connect(lambda: self.play_video(video_info['path']))

        delete_btn = QPushButton("删除")
        delete_btn.setFixedSize(80, 30)
        delete_btn.setStyleSheet("background-color: #ff6b6b; color: white;")
        delete_btn.clicked.connect(lambda: self.delete_video(video_info, frame))

        button_layout.addWidget(play_btn)
        button_layout.addWidget(delete_btn)

        layout.addWidget(index_label)
        layout.addLayout(info_layout)
        layout.addStretch()
        layout.addLayout(button_layout)

        return frame

    def photo_btn_func(self):
        """显示照片列表"""
        # 关闭摄像头
        self.stopCamera()

        # 清空center_area区域
        self.clearCenterArea()

        # 创建滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFixedSize(800, 600)

        # 创建容器widget
        container = QWidget()
        container_layout = QVBoxLayout(container)

        if not self.photos_list:
            no_photos_label = QLabel("暂无照片记录")
            no_photos_label.setAlignment(Qt.AlignCenter)
            no_photos_label.setStyleSheet("font-size: 20px; color: #666; margin-top: 100px;")
            container_layout.addWidget(no_photos_label)
        else:
            # 添加标题
            title_label = QLabel("照片列表")
            title_label.setAlignment(Qt.AlignCenter)
            title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px;")
            container_layout.addWidget(title_label)

            # 使用QScrollArea包装网格布局，以支持滚动
            grid_scroll = QScrollArea()
            grid_scroll.setWidgetResizable(True)
            grid_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

            grid_container = QWidget()
            grid_layout = QGridLayout(grid_container)

            row, col = 0, 0
            max_cols = 3  # 每行显示3张照片

            for i, photo_info in enumerate(reversed(self.photos_list), 1):
                photo_item = self.create_photo_item(photo_info, i)
                grid_layout.addWidget(photo_item, row, col)
                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1

            grid_scroll.setWidget(grid_container)
            container_layout.addWidget(grid_scroll)

        scroll.setWidget(container)

        # 移除原始的center_area，添加滚动区域
        self.center_layout.removeWidget(self.center_area)
        self.center_area.setParent(None)
        self.center_layout.addWidget(scroll)

    def create_photo_item(self, photo_info, index):
        """创建照片列表项"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Box)
        frame.setFixedSize(250, 300)
        frame.setStyleSheet("""
            QFrame {
                border: 2px solid #ccc;
                border-radius: 10px;
                padding: 10px;
                margin: 5px;
                background-color: #f9f9f9;
            }
            QFrame:hover {
                background-color: #f0f0f0;
                border-color: #999;
            }
        """)

        layout = QVBoxLayout(frame)

        # 显示缩略图
        try:
            pixmap = QPixmap(photo_info['path'])
            if not pixmap.isNull():
                # 调整缩略图大小
                pixmap = pixmap.scaled(200, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                thumbnail_label = QLabel()
                thumbnail_label.setPixmap(pixmap)
                thumbnail_label.setAlignment(Qt.AlignCenter)
                layout.addWidget(thumbnail_label)
        except Exception as e:
            print(f"加载图片失败: {e}")
            error_label = QLabel("图片加载失败")
            error_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(error_label)

        # 照片信息
        name_label = QLabel(f"照片 {index}")
        name_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        name_label.setAlignment(Qt.AlignCenter)

        time_label = QLabel(f"时间: {photo_info['timestamp']}")
        time_label.setStyleSheet("font-size: 12px; color: #666;")
        time_label.setAlignment(Qt.AlignCenter)

        # 按钮
        button_layout = QHBoxLayout()

        view_btn = QPushButton("查看")
        view_btn.setFixedSize(80, 25)
        view_btn.clicked.connect(lambda: self.view_photo(photo_info['path']))

        delete_btn = QPushButton("删除")
        delete_btn.setFixedSize(80, 25)
        delete_btn.setStyleSheet("background-color: #ff6b6b; color: white;")
        delete_btn.clicked.connect(lambda: self.delete_photo(photo_info, frame))

        button_layout.addWidget(view_btn)
        button_layout.addWidget(delete_btn)

        layout.addWidget(name_label)
        layout.addWidget(time_label)
        layout.addLayout(button_layout)

        return frame

    def play_video(self, video_path):
        """播放视频"""
        try:
            os.startfile(video_path)
        except:
            QMessageBox.warning(self, "警告", "无法播放视频，请检查播放器")

    def view_photo(self, photo_path):
        """查看照片"""
        dialog = QDialog(self)
        dialog.setWindowTitle("查看照片")
        dialog.setFixedSize(800, 600)

        layout = QVBoxLayout(dialog)

        pixmap = QPixmap(photo_path)
        if not pixmap.isNull():
            label = QLabel()
            label.setPixmap(pixmap.scaled(780, 550, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)

        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn, alignment=Qt.AlignCenter)

        dialog.exec_()

    def delete_video(self, video_info, frame):
        """删除视频"""
        reply = QMessageBox.question(
            self,
            "确认删除",
            f"确定要删除视频 {video_info['filename']} 吗？",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                # 删除文件
                Path(video_info['path']).unlink()
                # 从列表中移除
                self.videos_list = [v for v in self.videos_list if v['path'] != video_info['path']]
                self.save_video_list()
                # 移除界面中的项目
                frame.setParent(None)
                frame.deleteLater()

                # 刷新视频列表显示
                self.video_btn_func()

                QMessageBox.information(self, "成功", "视频已删除")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"删除失败: {str(e)}")

    def delete_photo(self, photo_info, frame):
        """删除照片"""
        reply = QMessageBox.question(
            self,
            "确认删除",
            f"确定要删除照片 {photo_info['filename']} 吗？",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                # 删除文件
                Path(photo_info['path']).unlink()
                # 从列表中移除
                self.photos_list = [p for p in self.photos_list if p['path'] != photo_info['path']]
                self.save_photo_list()
                # 移除界面中的项目
                frame.setParent(None)
                frame.deleteLater()

                # 刷新照片列表显示
                self.photo_btn_func()

                QMessageBox.information(self, "成功", "照片已删除")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"删除失败: {str(e)}")

    def line_btn_func(self):
        """车道线检测功能"""
        # 关闭摄像头
        self.stopCamera()
        # 清空center_area，显示车道线检测相关内容
        self.clearCenterArea()
        self.center_area.setText("车道线检测功能开发中...")
        self.center_area.setStyleSheet("font-size: 20px; color: #666;")

    def info_btn_func(self):
        """用户中心功能"""
        # 关闭摄像头
        self.stopCamera()
        # 清空center_area，显示用户中心相关内容
        self.clearCenterArea()
        self.center_area.setText(f"用户中心\n\n用户名: {self.username}\n\n功能开发中...")
        self.center_area.setStyleSheet("font-size: 20px; color: #666;")
        self.center_area.setAlignment(Qt.AlignCenter)