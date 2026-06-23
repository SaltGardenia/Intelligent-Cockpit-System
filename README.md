# 🚗 智慧座舱系统 (Intelligent Cockpit System)

基于 **PyQt5** 和 **YOLOv7** 的智能座舱桌面应用，集成了座舱目标检测、导航、音乐播放、电话等功能，为您提供一体化智能驾驶体验。

---

## ✨ 功能特性

### 📷 座舱检测
- 基于 **YOLOv7** 的实时目标检测（使用 `best.pt` 模型）
- 调用摄像头实时检测座舱内物体并标注
- 支持拍照保存与视频录制
- 照片与视频列表管理

### 🗺️ 导航系统
- 集成 **百度地图** API，支持地点搜索与地图展示
- 可缩放、拖拽地图，查看实时位置

### 🎵 音乐播放器
- 本地音乐文件播放
- 歌曲列表管理
- 播放进度控制、音量调节

### 📞 电话功能
- 模拟拨号盘界面
- 拨打与挂断操作

### 🔐 用户系统
- 用户登录 / 注册（基于 MySQL 数据库）
- 用户密码加密存储
- 个性化欢迎界面

### 🎬 启动动画
- 炫酷的启动加载界面，模拟系统启动进度

---

## 🛠️ 技术栈

| 技术 | 用途 |
|------|------|
| **Python 3.10+** | 开发语言 |
| **PyQt5** | 桌面 GUI 框架 |
| **PyTorch** | 深度学习框架 |
| **YOLOv7** | 目标检测模型 |
| **OpenCV** | 图像处理与摄像头调用 |
| **MySQL + PyMySQL** | 用户数据存储 |
| **百度地图 API** | 地图导航服务 |
| **Docker** | 容器化部署 |

---

## 📁 项目结构

```
Intelligent-Cockpit-System/
├── main.py                  # 程序入口
├── driving_detect.py        # YOLOv7 目标检测模块
├── requirements.txt         # Python 依赖
├── Dockerfile               # Docker 构建文件
├── docker-compose.yml       # Docker Compose 配置
├── best.pt                  # YOLOv7 训练权重
├── yolov7.pt                # YOLOv7 预训练权重
├── data/
│   ├── ai250802.sql         # 数据库建表脚本
│   ├── img/                 # 图片资源
│   ├── music/               # 音乐文件
│   ├── photos/              # 拍摄照片存储
│   │   └── photos_list.json # 照片列表记录
│   └── videos/              # 录制视频存储
│       └── videos_list.json # 视频列表记录
├── pages/
│   ├── splash_screen.py     # 启动动画页面
│   ├── login_window.py      # 登录窗口
│   ├── register_window.py   # 注册窗口
│   ├── main_window.py       # 主窗口（导航侧栏 + 页面切换）
│   ├── home_page.py         # 首页（座舱检测、拍照、录像）
│   ├── navigation_page.py   # 导航页面（百度地图）
│   ├── music_page.py        # 音乐播放器页面
│   ├── phone_page.py        # 电话拨号页面
│   └── DB_util.py           # 数据库工具类
├── models/                  # YOLOv7 模型组件
├── utils/                   # YOLOv7 工具函数
└── README.md                # 项目说明文档
```

---

## 🚀 快速开始

### 1️⃣ 环境准备

确保已安装 **Python 3.10+** 和 **MySQL** 数据库。

### 2️⃣ 克隆项目

```bash
git clone https://github.com/yourusername/Intelligent-Cockpit-System.git
cd Intelligent-Cockpit-System
```

### 3️⃣ 安装依赖

```bash
pip install -r requirements.txt
```

### 4️⃣ 配置数据库

1. 创建 MySQL 数据库（默认数据库名 `ai250802`）：

```sql
CREATE DATABASE ai250802 CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
```

2. 导入数据库表结构：

```bash
mysql -u root -p ai250802 < data/ai250802.sql
```

3. （可选）修改数据库连接配置，编辑 `pages/DB_util.py`：

```python
DButil(host='localhost', port=3306, user='root', password='123456', database='ai250802')
```

### 5️⃣ 配置百度地图 API（导航功能）

编辑 `pages/navigation_page.py`，替换 `baidu_ak` 变量的值为你的百度地图 AK：

```python
self.baidu_ak = "你的百度AK"  # 在百度地图开放平台申请
```

### 6️⃣ 运行程序

```bash
python main.py
```

---

## 🐳 Docker 部署

### 使用 Docker Compose（推荐）

```bash
docker-compose up -d
```

### 手动 Docker 构建

```bash
docker build -t intelligent-cockpit:latest .
docker run -it --rm \
  -v ./logs:/app/logs \
  -v ./config:/app/config \
  intelligent-cockpit:latest
```

---

## 🧠 目标检测模型

- **`best.pt`**：在 YOLOv7 基础上针对座舱场景微调后的模型权重
- **`yolov7.pt`**：YOLOv7 官方预训练权重（80 类 COCO 数据集）

如需更换模型，修改 `driving_detect.py` 中的 `self.weights` 参数即可。

---

## 📸 截图预览

| 启动画面 | 登录页面 | 主页 |
|---------|---------|------|
| 加载动画与启动进度 | 用户名密码登录 | 座舱检测与功能面板 |

| 导航系统 | 音乐播放器 | 电话拨号 |
|---------|-----------|---------|
| 百度地图搜索与展示 | 本地音乐播放与控制 | 模拟拨号盘 |

---

## 📌 注意事项

1. **摄像头**：座舱检测功能需要连接可用摄像头
2. **百度 AK**：导航功能需自行申请百度地图开放平台密钥
3. **MySQL**：登录注册功能依赖 MySQL 数据库，请确保服务运行正常
4. **模型文件**：`best.pt` 为训练后的座舱检测专用权重，首次使用请确保文件完整

---

## 📄 开源协议

本项目仅供学习交流使用，未经许可不得用于商业用途。

---

## 👤 作者

- **Zzz** - 初始开发

---

> **智慧座舱系统** — 让驾驶更智能，让出行更安心 🚗💨
