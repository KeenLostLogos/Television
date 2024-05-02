import time

from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import QMainWindow
from PySide6.QtCore import Slot

from televisionUI import Ui_MainWindow


class TelevisionLogic(QMainWindow, Ui_MainWindow):
    """
    Holds the logic to recreate a basic television and display a few video choices
    """
    MIN_VOLUME: int = 0
    MAX_VOLUME: int = 5
    MIN_CHANNEL: int = 0
    MAX_CHANNEL: int = 3

    def __init__(self) -> None:
        """
        sets up initial values for the television
        :return: None
        """
        super().__init__()
        self.setupUi(self)
        self.__status: bool = False
        self.__muted: bool = False
        self.__volume: int = 2
        self.__channel: int = TelevisionLogic.MIN_CHANNEL
        self.__audio_output = QAudioOutput()
        self.__player = QMediaPlayer()
        self.__player.setAudioOutput(self.__audio_output)
        self.__video_widget = QVideoWidget(parent=self.centralwidget)
        self.config_UI()

    def config_UI(self) -> None:
        """
        configures the User Interface and adds button functionality
        :return: None
        """
        self.__video_widget.setFixedSize(960, 400)
        self.__player.setVideoOutput(self.__video_widget)
        self.power_pushButton.clicked.connect(self.power)
        self.mute_pushButton.clicked.connect(self.mute)
        self.c_up_pushButton.clicked.connect(self.channel_up)
        self.c_down_pushButton.clicked.connect(self.channel_down)
        self.v_up_pushButton.clicked.connect(self.volume_up)
        self.v_down_pushButton.clicked.connect(self.volume_down)
        self.__audio_output.setVolume(self.__volume * 0.2)

    def closeEvent(self, event) -> None:
        """
        Makes sure the playback is stopped on close
        :param event: the Close event
        :return:
        """
        self.__player.stop()
        event.accept()

    def new_channel(self) -> None:
        """
        updates the television to the new channel and displays the contents for that channel
        :return:
        """
        self.__player.stop()
        time.sleep(.1)
        self.__player.setSource(QUrl.fromLocalFile(f"./videos/channel{self.__channel}.mp4"))
        self.__player.play()

    def power(self) -> None:
        """
        Method to toggle the current power state of the Television
        :return: None
        """
        self.__status = not self.__status
        if self.__status:
            self.new_channel()
        else:
            self.__player.stop()

    def mute(self) -> None:
        """
        Method to toggle the current mute state of the Television
        :return: None
        """
        if self.__status:
            self.__muted = not self.__muted
            self.volume_lcdNumber.display(self.__volume if not self.__muted else 0)
            self.__audio_output.setVolume(self.__volume * 0.2 if not self.__muted else 0)

    def channel_up(self) -> None:
        """
        Method to increase the channel of the television by one unless it is at its maximum in which case it rolls to
        the minimum channel
        :return: None
        """
        if self.__status:
            self.__channel = self.__channel + 1 if self.__channel != TelevisionLogic.MAX_CHANNEL else TelevisionLogic.MIN_CHANNEL
            self.channel_lcdNumber.display(self.__channel)
            self.new_channel()

    def channel_down(self) -> None:
        """
        Method to decrease the channel of the television by one unless it is at its minimum in which case it rolls to
        the maximum channel
        :return: None
        """
        if self.__status:
            self.__channel = self.__channel - 1 if self.__channel != TelevisionLogic.MIN_CHANNEL else TelevisionLogic.MAX_CHANNEL
            self.channel_lcdNumber.display(self.__channel)
            self.new_channel()

    def volume_up(self) -> None:
        """
        Method to increase the volume of the television by one unless it is at its maximum in which case it stays at the maximum
        :return: None
        """
        if self.__status:

            if self.__muted:
                self.__muted = False

            self.__volume = self.__volume + 1 if self.__volume != TelevisionLogic.MAX_VOLUME else TelevisionLogic.MAX_VOLUME
            self.volume_lcdNumber.display(self.__volume)
            self.__audio_output.setVolume(self.__volume * 0.2)

    def volume_down(self) -> None:
        """
        Method to decrease the volume of the television by one unless it is at its minimum in which case it stays at the minimum
        :return: None
        """
        if self.__status:

            if self.__muted:
                self.__muted = False

            self.__volume = self.__volume - 1 if self.__volume != TelevisionLogic.MIN_VOLUME else TelevisionLogic.MIN_VOLUME
            self.volume_lcdNumber.display(self.__volume)
            self.__audio_output.setVolume(self.__volume * 0.2)
