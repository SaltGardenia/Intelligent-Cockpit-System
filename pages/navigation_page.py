from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
import urllib.parse
import sys


class NavigationPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 请替换为你的百度AK（在百度地图开放平台申请）
        self.baidu_ak = "mqWyl1vC6D8nbs2ofTtOC7WDlXzlIdFa"  # 你的百度AK
        self.current_lat = 39.9042  # 北京纬度
        self.current_lon = 116.4074  # 北京经度
        self.current_zoom = 12
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 导航标题
        nav_title = QLabel('导航系统')
        nav_title.setFont(QFont('Arial', 20, QFont.Bold))
        nav_title.setAlignment(Qt.AlignCenter)
        nav_title.setStyleSheet("""
            color: white;
            padding: 15px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #3498db, stop:1 #2ecc71);
            border-radius: 8px;
            margin-bottom: 10px;
        """)

        # 地图控件
        self.map_view = QWebEngineView()
        self.map_view.setMinimumSize(700, 500)  # 调整为适合在页面中显示

        # 调试：连接加载完成信号
        self.map_view.loadFinished.connect(self.on_map_loaded)

        # 加载地图
        self.load_simplified_map()

        # 地图容器
        map_container = QWidget()
        map_layout = QVBoxLayout(map_container)
        map_layout.addWidget(self.map_view)
        map_container.setStyleSheet("""
            QWidget {
                border: 2px solid #3498db;
                border-radius: 10px;
                background-color: white;
            }
        """)

        # 控制区域
        control_container = QWidget()
        control_container.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 10px;
            }
        """)

        # 主控制布局
        main_control_layout = QHBoxLayout(control_container)

        # 搜索区域
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('输入目的地（如：北京天安门）...')
        self.search_input.setMinimumWidth(300)
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                font-size: 14px;
                border: 2px solid #ddd;
                border-radius: 6px 0 0 6px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: #f0f8ff;
            }
        """)
        self.search_input.returnPressed.connect(self.search_destination)

        search_btn = QPushButton('搜索')
        search_btn.setFixedWidth(80)
        search_btn.setStyleSheet("""
            QPushButton {
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
                color: white;
                background-color: #3498db;
                border: none;
                border-radius: 0 6px 6px 0;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1c6ea4;
            }
        """)
        search_btn.clicked.connect(self.search_destination)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)

        # 地图控制按钮
        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(10, 0, 0, 0)

        zoom_in_btn = QPushButton('+')
        zoom_out_btn = QPushButton('-')
        reset_btn = QPushButton('重置')
        locate_btn = QPushButton('定位')

        # 设置按钮大小
        zoom_in_btn.setFixedSize(40, 40)
        zoom_out_btn.setFixedSize(40, 40)
        reset_btn.setFixedHeight(40)
        locate_btn.setFixedHeight(40)

        for btn, action in [(zoom_in_btn, self.zoom_in),
                            (zoom_out_btn, self.zoom_out),
                            (reset_btn, self.reset_map),
                            (locate_btn, self.locate_current)]:
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 14px;
                    font-weight: bold;
                    color: white;
                    background-color: #2ecc71;
                    border: none;
                    border-radius: 4px;
                    margin-left: 5px;
                }
                QPushButton:hover {
                    background-color: #27ae60;
                }
                QPushButton:pressed {
                    background-color: #219653;
                }
            """)
            btn.clicked.connect(action)
            btn_layout.addWidget(btn)

        # 缩放按钮特殊样式
        zoom_in_btn.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                font-weight: bold;
                color: white;
                background-color: #e74c3c;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)

        zoom_out_btn.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                font-weight: bold;
                color: white;
                background-color: #e67e22;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
        """)

        # 将搜索和按钮添加到主控制布局
        main_control_layout.addWidget(search_container)
        main_control_layout.addWidget(btn_container)

        # 状态栏
        self.status_label = QLabel('地图加载中...')
        self.status_label.setStyleSheet("""
            QLabel {
                padding: 8px;
                color: #666;
                font-size: 13px;
                background-color: #f1f8ff;
                border-radius: 4px;
                border: 1px solid #d1e7ff;
            }
        """)

        # 添加到主布局
        layout.addWidget(nav_title)
        layout.addWidget(map_container, 1)  # 地图占据大部分空间
        layout.addWidget(control_container)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def load_simplified_map(self):
        """加载简化的百度地图HTML - 修复版本"""
        html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>百度地图</title>
            <style>
                body, html {{
                    margin: 0;
                    padding: 0;
                    width: 100%;
                    height: 100%;
                    overflow: hidden;
                }}
                #map {{
                    width: 100%;
                    height: 100%;
                }}
                .error {{
                    color: red;
                    padding: 20px;
                    text-align: center;
                    font-size: 16px;
                }}
            </style>
        </head>
        <body>
            <div id="map"></div>

            <script type="text/javascript">
                // 初始化地图
                function initMap() {{
                    console.log("开始初始化地图...");

                    try {{
                        // 创建地图实例
                        var map = new BMapGL.Map("map");

                        // 设置中心点坐标（北京）
                        var point = new BMapGL.Point({self.current_lon}, {self.current_lat});

                        // 初始化地图，设置中心点坐标和地图级别
                        map.centerAndZoom(point, {self.current_zoom});

                        // 开启鼠标滚轮缩放
                        map.enableScrollWheelZoom(true);

                        // 添加比例尺控件
                        map.addControl(new BMapGL.ScaleControl());

                        // 添加缩放控件
                        map.addControl(new BMapGL.ZoomControl());

                        // 添加默认标记
                        var marker = new BMapGL.Marker(point);
                        map.addOverlay(marker);

                        console.log("百度地图初始化成功！");

                        // 将地图对象保存到全局变量
                        window.baiduMap = map;

                        // 触发事件通知地图已加载
                        var event = new Event('baidumapLoaded');
                        window.dispatchEvent(event);

                    }} catch (error) {{
                        console.error("地图初始化失败:", error);
                        document.getElementById("map").innerHTML = 
                            '<div class="error">地图加载失败: ' + error.message + '</div>';
                    }}
                }}

                // 加载百度地图API
                function loadBaiduMap() {{
                    // 检查是否已加载API
                    if (typeof BMapGL !== 'undefined') {{
                        initMap();
                        return;
                    }}

                    // 创建script元素
                    var script = document.createElement('script');
                    script.type = 'text/javascript';

                    // 使用正确的API地址
                    script.src = 'https://api.map.baidu.com/api?type=webgl&v=1.0&ak={self.baidu_ak}&callback=initMap';

                    // 错误处理
                    script.onerror = function() {{
                        console.error("百度地图API加载失败");
                        document.getElementById("map").innerHTML = 
                            '<div class="error">无法加载百度地图API<br>请检查：<br>1. 网络连接<br>2. API密钥是否有效</div>';
                    }};

                    // 添加到文档
                    document.head.appendChild(script);

                    // 同时加载样式
                    var link = document.createElement('link');
                    link.rel = 'stylesheet';
                    link.type = 'text/css';
                    link.href = 'https://api.map.baidu.com/res/webgl/10/bmap.css';
                    document.head.appendChild(link);
                }}

                // 页面加载完成后执行
                window.onload = loadBaiduMap;
            </script>
        </body>
        </html>
        '''

        self.map_view.setHtml(html)

    def on_map_loaded(self, success):
        """地图加载完成回调"""
        if success:
            self.status_label.setText('地图加载成功！您可以开始搜索目的地。')
            print("地图视图加载成功")

            # 检查地图状态
            self.map_view.page().runJavaScript("window.mapStatus", self.update_map_status)
        else:
            self.status_label.setText('地图加载失败，请检查网络连接')
            print("地图视图加载失败")

    def update_map_status(self, status):
        """更新地图状态信息"""
        status_messages = {
            "ready": "地图就绪",
            "error": "地图初始化错误",
            "load_error": "API加载失败"
        }
        if status in status_messages:
            self.status_label.setText(f"状态: {status_messages[status]}")

    def search_destination(self):
        """搜索目的地"""
        destination = self.search_input.text().strip()
        if not destination:
            QMessageBox.warning(self, '提示', '请输入目的地！')
            return

        self.status_label.setText(f'正在搜索: {destination}...')

        # 使用JavaScript进行地理编码
        js_code = f"""
        function searchLocation() {{
            var destination = "{destination}";
            console.log("开始搜索位置:", destination);

            // 检查地图对象是否存在
            if (!window.baiduMap) {{
                console.error("地图对象未初始化");
                window.searchResult = {{success: false, message: "地图未初始化，请稍后重试"}};
                return;
            }}

            // 创建地理编码实例
            var myGeo = new BMapGL.Geocoder();

            myGeo.getPoint(destination, function(point) {{
                if (point) {{
                    console.log("找到位置:", point.lng, point.lat);

                    // 清除现有标记
                    window.baiduMap.clearOverlays();

                    // 移动到新位置
                    window.baiduMap.centerAndZoom(point, 15);

                    // 添加新标记
                    var marker = new BMapGL.Marker(point);
                    window.baiduMap.addOverlay(marker);

                    // 添加信息窗口
                    var infoWindow = new BMapGL.InfoWindow(destination);
                    marker.addEventListener("click", function() {{
                        window.baiduMap.openInfoWindow(infoWindow, point);
                    }});

                    // 弹跳动画
                    marker.setAnimation(BMAP_ANIMATION_BOUNCE);

                    console.log("成功定位到: " + destination);
                    window.searchResult = {{success: true, message: "成功定位到: " + destination}};

                }} else {{
                    console.log("未找到位置: " + destination);
                    window.searchResult = {{success: false, message: "未找到位置: " + destination}};
                }}
            }}, "全国");
        }}

        // 检查API是否已加载
        if (typeof BMapGL !== 'undefined') {{
            searchLocation();
        }} else {{
            console.error("百度地图API未加载");
            window.searchResult = {{success: false, message: "API未加载，请稍后重试"}};
        }}
        """

        # 执行JavaScript
        self.map_view.page().runJavaScript(js_code, lambda result: self.handle_search_result())

    def handle_search_result(self):
        """处理搜索结果"""
        self.map_view.page().runJavaScript("window.searchResult", self.on_search_complete)

    def on_search_complete(self, result):
        """搜索完成回调"""
        if result:
            if result.get('success'):
                self.status_label.setText(result.get('message', '搜索成功'))
                print(f"搜索成功: {result.get('message')}")
            else:
                self.status_label.setText(result.get('message', '搜索失败'))
                QMessageBox.warning(self, '搜索失败', result.get('message', '未找到该位置，请确认输入是否正确。'))

    def zoom_in(self):
        """放大地图"""
        js_code = """
        if (window.baiduMap) {
            var zoom = window.baiduMap.getZoom();
            window.baiduMap.setZoom(zoom + 1);
            console.log("放大地图，当前级别: " + (zoom + 1));
        } else {
            console.error("地图对象不存在");
        }
        """
        self.map_view.page().runJavaScript(js_code)

    def zoom_out(self):
        """缩小地图"""
        js_code = """
        if (window.baiduMap) {
            var zoom = window.baiduMap.getZoom();
            window.baiduMap.setZoom(zoom - 1);
            console.log("缩小地图，当前级别: " + (zoom - 1));
        } else {
            console.error("地图对象不存在");
        }
        """
        self.map_view.page().runJavaScript(js_code)

    def reset_map(self):
        """重置地图到初始位置"""
        js_code = f"""
        if (window.baiduMap) {{
            var point = new BMapGL.Point({self.current_lon}, {self.current_lat});
            window.baiduMap.centerAndZoom(point, {self.current_zoom});
            window.baiduMap.clearOverlays();

            // 添加标记
            var marker = new BMapGL.Marker(point);
            window.baiduMap.addOverlay(marker);

            console.log("地图已重置");
            window.searchResult = {{success: true, message: "地图已重置到初始位置"}};
        }} else {{
            console.error("地图对象不存在");
        }}
        """
        self.map_view.page().runJavaScript(js_code)
        self.status_label.setText('地图已重置到初始位置')
        self.search_input.clear()

    def locate_current(self):
        """定位当前位置"""
        # 这里可以扩展为获取真实GPS位置
        self.status_label.setText('定位中...')

        js_code = """
        // 这里可以集成HTML5的Geolocation API来获取真实位置
        if (window.baiduMap) {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(position) {
                    var point = new BMapGL.Point(position.coords.longitude, position.coords.latitude);
                    window.baiduMap.centerAndZoom(point, 15);

                    // 清除现有标记
                    window.baiduMap.clearOverlays();

                    // 添加标记
                    var marker = new BMapGL.Marker(point);
                    window.baiduMap.addOverlay(marker);

                    console.log("定位到当前位置:", point.lng, point.lat);
                }, function(error) {
                    console.log("定位失败:", error.message);
                });
            } else {
                console.log("浏览器不支持Geolocation");
            }
        }
        """

        # 由于安全限制，HTML5定位在本地文件中可能不可用
        # 暂时使用模拟定位
        self.status_label.setText('定位完成（演示模式）')
        self.map_view.page().runJavaScript(f"""
        if (window.baiduMap) {{
            var point = new BMapGL.Point({self.current_lon}, {self.current_lat});
            window.baiduMap.centerAndZoom(point, 15);

            // 清除现有标记
            window.baiduMap.clearOverlays();

            // 添加标记
            var marker = new BMapGL.Marker(point);
            window.baiduMap.addOverlay(marker);

            // 添加信息窗口
            var infoWindow = new BMapGL.InfoWindow("当前位置（演示）");
            marker.addEventListener("click", function() {{
                window.baiduMap.openInfoWindow(infoWindow, point);
            }});
        }}
        """)

    def showEvent(self, event):
        """当页面显示时触发"""
        super().showEvent(event)
        # 可以在这里添加页面显示时的初始化代码
        print("导航页面已显示")

    def hideEvent(self, event):
        """当页面隐藏时触发"""
        super().hideEvent(event)
        # 可以在这里添加页面隐藏时的清理代码
        print("导航页面已隐藏")


# 百度AK获取说明函数
def show_ak_help():
    """显示百度AK获取帮助"""
    help_text = """
    ================================================
    百度地图AK密钥获取说明：
    ================================================
    1. 访问百度地图开放平台：https://lbsyun.baidu.com/
    2. 注册并登录百度账号
    3. 进入控制台 -> 应用管理 -> 我的应用
    4. 点击"创建应用"
    5. 填写应用信息：
       - 应用名称：导航系统
       - 应用类型：浏览器端
       - 白名单：* (或填写你的IP地址)
    6. 创建后获取AK密钥
    7. 将获取的AK替换代码中的 self.baidu_ak

    注意：新AK需要几分钟才能生效
    ================================================
    """
    print(help_text)
    return help_text


# 测试代码
if __name__ == "__main__":
    # 注意：这个测试代码只在直接运行此文件时有效
    # 在主程序中，NavigationPage会被集成到堆叠窗口中

    # 显示帮助信息
    show_ak_help()

    # 检查百度AK
    app = QApplication(sys.argv)

    # 创建单独的导航页面窗口（仅用于测试）
    test_window = QWidget()
    test_layout = QVBoxLayout(test_window)

    nav_page = NavigationPage()

    # 检查是否设置了百度AK
    if nav_page.baidu_ak == "你的百度AK密钥":
        reply = QMessageBox.question(test_window, '配置提醒',
                                     '请先配置百度地图AK密钥！\n\n是否查看帮助文档？',
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            QMessageBox.information(test_window, '帮助信息', show_ak_help())

    test_layout.addWidget(nav_page)
    test_window.resize(900, 700)
    test_window.setWindowTitle('导航页面测试')
    test_window.show()

    sys.exit(app.exec_())