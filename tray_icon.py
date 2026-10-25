from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QObject
import os

path_icon = os.path.join(os.getcwd(), "icon.ico")


class TrayIcon(QObject):
    def __init__(self, app: QApplication, on_show_main=None, on_quick_ask=None):
        super().__init__()
        self.app = app
        self.on_show_main = on_show_main
        self.on_quick_ask = on_quick_ask

        if not QSystemTrayIcon.isSystemTrayAvailable():
            print("Системный трей недоступен")

        self.tray_icon = QSystemTrayIcon(QIcon(path_icon), self.app)
        self.tray_icon.setToolTip("AI App")

        self._menu = QMenu()
        self.main_gui_v = QAction("Главная", self.app)
        self.zapros_guiv = QAction("Быстрый вопрос", self.app)
        self.exit_app = QAction("Выход", self.app)

        self._menu.addAction(self.main_gui_v)
        self._menu.addAction(self.zapros_guiv)
        self._menu.addSeparator()
        self._menu.addAction(self.exit_app)

        self.tray_icon.setContextMenu(self._menu)
        self.tray_icon.activated.connect(self.on_activated)

        # Подключаем действия меню
        self.main_gui_v.triggered.connect(self._show_main)
        self.zapros_guiv.triggered.connect(self._quick_ask)
        self.exit_app.triggered.connect(self.app.quit)   # ← выход

    def start(self):
        self.tray_icon.show()

    def on_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            print("Левый клик — показать главное окно")
            self._show_main()
        elif reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            print("Двойной клик")
            self._show_main()

    def _show_main(self):
        if self.on_show_main:
            self.on_show_main()

    def _quick_ask(self):
        if self.on_quick_ask:
            self.on_quick_ask()