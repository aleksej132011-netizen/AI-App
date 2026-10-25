import os, sys

path_project = os.path.dirname(os.path.abspath(__file__))
os.chdir(path_project)
if path_project not in sys.path:
    sys.path.insert(0, path_project)

from PyQt6.QtWidgets import QApplication
from gui.gui_func import MainGui, give_style_info
from tray_icon import TrayIcon

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)   # живём без окон, пока есть трей
    app.setStyleSheet(give_style_info())

    window = MainGui()
    window.show()

    tray = TrayIcon(
        app,
        on_show_main=window.show_and_raise,   # ← показать главное
        on_quick_ask=window.quick_ask,        # ← быстрый вопрос
    )
    tray.start()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()