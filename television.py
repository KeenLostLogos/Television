import sys

from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtWidgets import QApplication

from televisionLogic import TelevisionLogic


class Television:

    def __init__(self):
        self.application = QApplication(sys.argv)
        self.window = TelevisionLogic()
        self.window.show()
        sys.exit(self.application.exec())



if __name__ == "__main__":
    Television()
