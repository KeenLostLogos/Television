from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import QMainWindow
from PySide6.QtCore import Slot

from televisionUI import Ui_MainWindow


class TelevisionLogic(QMainWindow, Ui_MainWindow):
    MIN_VOLUME: int = 0
    MAX_VOLUME: int = 2
    MIN_CHANNEL: int = 0
    MAX_CHANNEL: int = 3

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.__status: bool = False
        self.__muted: bool = False
        self.__volume: int = TelevisionLogic.MIN_VOLUME
        self.__channel: int = TelevisionLogic.MIN_CHANNEL
        self._audio_output = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self._audio_output)
        self.video_widget = QVideoWidget(parent=self.centralwidget)
        self.video_widget.setFixedSize(960, 400)
        self.player.setVideoOutput(self.video_widget)
        self.power_pushButton.clicked.connect(self.power)
        self.mute_pushButton.clicked.connect(self.mute)
        self.c_up_pushButton.clicked.connect(self.channel_up)
        self.c_down_pushButton.clicked.connect(self.channel_down)
        self.v_up_pushButton.clicked.connect(self.volume_up)
        self.v_down_pushButton.clicked.connect(self.volume_down)

    def closeEvent(self, event):
        self._ensure_stopped()
        event.accept()

    def _ensure_stopped(self):
        if self.player.playbackState() != QMediaPlayer.StoppedState:
            self.player.stop()

    def power(self) -> None:
        """
        Method to toggle the current power state of the Television
        """
        self.player.stop()
        self.__status = not self.__status
        self.player.setSource(QUrl.fromLocalFile("./videos/sample_960x400_ocean_with_audio.mp4"))
        self.player.play()

    def mute(self) -> None:
        """
        Method to toggle the current mute state of the Television
        """

        print(self.player.mediaStatus())
        if self.__status:
            self.__muted = not self.__muted
            self.volume_lcdNumber.display(0)

    def channel_up(self) -> None:
        """
        Method to increase the channel of the television by one unless it is at its maximum in which case it rolls to
        the minimum channel
        """
        if self.__status:
            self.__channel = self.__channel + 1 if self.__channel != TelevisionLogic.MAX_CHANNEL else TelevisionLogic.MIN_CHANNEL
            self.channel_lcdNumber.display(self.__channel)

    def channel_down(self) -> None:
        """
        Method to decrease the channel of the television by one unless it is at its minimum in which case it rolls to
        the maximum channel
        """
        if self.__status:
            self.__channel = self.__channel - 1 if self.__channel != TelevisionLogic.MIN_CHANNEL else TelevisionLogic.MAX_CHANNEL
            self.channel_lcdNumber.display(self.__channel)

    def volume_up(self) -> None:
        """
        Method to increase the volume of the television by one unless it is at its maximum in which case it stays at the maximum
        """
        if self.__status:

            if self.__muted:
                self.__muted = False

            self.__volume = self.__volume + 1 if self.__volume != TelevisionLogic.MAX_VOLUME else TelevisionLogic.MAX_VOLUME
            self.volume_lcdNumber.display(self.__volume)

    def volume_down(self) -> None:
        """
        Method to decrease the volume of the television by one unless it is at its minimum in which case it stays at the minimum
        """
        if self.__status:

            if self.__muted:
                self.__muted = False

            self.__volume = self.__volume - 1 if self.__volume != TelevisionLogic.MIN_VOLUME else TelevisionLogic.MIN_VOLUME
            self.volume_lcdNumber.display(self.__volume if not self.__muted else 0)
