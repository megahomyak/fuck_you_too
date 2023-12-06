from PyQt6.QtCore import QThread, Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow
from fuckoff import FuckOff
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)


class MiddleFingerListener(QThread):
    show = pyqtSignal()
    hide = pyqtSignal()

    def run(self):
        with FuckOff() as fuckoff:
            while True:
                if fuckoff.check():
                    self.show.emit()
                else:
                    self.hide.emit()


class Cat(QMainWindow):
    def __init__(self):
        super().__init__()

        screen_size = app.primaryScreen().size()

        box_side = min(screen_size.width(), screen_size.height()) // 4 * 3

        self.setWindowFlags(
            self.windowFlags()
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )

        x = (screen_size.width() - box_side) // 2
        y = (screen_size.height() - box_side) // 2

        self.setGeometry(x, y, box_side, box_side)

        self.cat = QPixmap("cat.png")

        self.checking_thread = MiddleFingerListener()
        self.checking_thread.hide.connect(self.hide)
        self.checking_thread.show.connect(self.show)
        self.checking_thread.start()

    def paintEvent(self, _event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.cat)

app = QApplication([])

cat = Cat()

app.exec()
