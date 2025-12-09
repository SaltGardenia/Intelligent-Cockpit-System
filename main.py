import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from pages.splash_screen import SplashScreen
from pages.login_window import LoginWindow
from pages.main_window import MainWindow


class Application:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.splash = None
        self.login_window = None
        self.main_window = None

    def show_splash(self):
        """显示启动动画"""
        self.splash = SplashScreen()
        self.splash.show()

        # 3秒后关闭启动动画并显示登录页面
        QTimer.singleShot(3000, self.show_login)

    def show_login(self):
        """显示登录页面"""
        self.splash.close()
        self.login_window = LoginWindow()
        self.login_window.login_successful.connect(self.show_main_window)
        self.login_window.show()

    def show_main_window(self, username):
        """显示主窗口"""
        if self.login_window:
            self.login_window.close()

        self.main_window = MainWindow(username)
        self.main_window.show()

    def run(self):
        """运行应用程序"""
        self.show_splash()
        sys.exit(self.app.exec_())


if __name__ == '__main__':
    application = Application()
    application.run()