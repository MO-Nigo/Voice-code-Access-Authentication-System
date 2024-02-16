from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QMainWindow
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
from os import path
from PyQt5.QtCore import QTimer
from pyqtgraph import PlotWidget, ImageItem
import matplotlib.pyplot as plt
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFrame
import pyqtgraph as pg
import librosa.display
from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import os
from os import path
import sys
import pyqtgraph as pg
from pydub import AudioSegment
from pydub.playback import play
from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget
import vlc
from logic_app import Logic  # Import the new function
from voice_identification import Voice  # Import the new function


FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "main.ui"))

class MainApp(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)


        QMainWindow.__init__(self, parent=None)
        self.setupUi(self)
        self.gridLayout = QGridLayout()
        self.setLayout(self.gridLayout)
        self.setWindowTitle("Vocal Guard")
        self.logic_app = Logic(self)
        self.voice_identification = Voice(self)

        self.set_app_icon()
        self.set_app_name()
        self.image_item = ImageItem()
        self.setup_style_sheet()
        self.person_status.hide()
        self.word_status.hide()
        self.plotSpec = MatplotlibWidget()
        self.plotSpec.fig.patch.set_facecolor((0.8,0.8,0.8))
        self.plotSpec.setMinimumSize(QtCore.QSize(300, 300))
        self.plotSpec.setMaximumSize(QtCore.QSize(600, 600))
        self.gridLayout.addWidget(self.plotSpec, 4, 2, 0, 0)
        self.plotSpec.fig.subplots_adjust(right=0.96, left=0.04, bottom=0.04)


        self.frameSpec.setLayout(QVBoxLayout())
        self.frameSpec.layout().addWidget(self.plotSpec)
        # audio_files = []
        # for root, dirs, files in os.walk("audio"):
        #     for file in files:
        #         # Check if the file has an audio extension (you may customize this condition)
        #         if file.endswith((".wav")):
        #             # Construct the full path to the audio file
        #             audio_file_path = os.path.join(root, file)
        #             # Append the file path to the list of audio files
        #             audio_files.append(audio_file_path)
        # self.boxTester.addItems(audio_files)
        # audio_folder_path = os.path.join(os.path.dirname(__file__), 'audio')

        # # Use QDir to list the folder names
        # audio_folder = QDir(audio_folder_path)
        # audio_folder.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot)
        # folder_names = audio_folder.entryList()
        #
        # # Populate the QComboBox with folder names
        # self.boxVoice.addItems(folder_names)
        # Create a QTimer instance

        # audio_folder_path = os.path.join(os.path.dirname(__file__), 'voice')
        #
        # # Use QDir to list the folder names
        # audio_folder = QDir(audio_folder_path)
        # audio_folder.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot)
        # folder_names = audio_folder.entryList()
        #
        # # Populate the QComboBox with folder names
        # self.boxVoice.addItems(folder_names)

        self.timerPerson = QTimer(self)
        # Connect the timeout signal to a slot (function)
        self.timerPerson.timeout.connect(lambda: self.logic_app.hide_person_status())

        self.timerWord = QTimer(self)
        # Connect the timeout signal to a slot (function)
        self.timerWord.timeout.connect(lambda: self.logic_app.hide_word_status())
        self.btnRecord.clicked.connect(lambda: self.logic_app.record_and_process_voice())
        # self.btnRecord.clicked.connect(lambda: self.voice_identification.record_voice())

        # self.btnMode.clicked.connect(lambda: self.voice_identification.mode_changed())
        # self.btnTester.clicked.connect(lambda: self.logic_app.tester())



    def set_app_icon(self):
        app_icon = QIcon('icons/icon.png')
        self.setWindowIcon(app_icon)

    def set_app_name(self):
        app.setApplicationName("Vocal Guard")

    def setup_style_sheet(self):
        style_sheet = '''
            QWidget {
                background-color: white;  /* Dark Gray Background */
            }
            QLabel {
                font-size: 14px;
                background-color: white;
                color: black;
            }
            QLineEdit {
                background-color: white;
                color: black;
                border: 1px solid #CCCCFF;
                border-radius: 5px;
                padding: 5px;
            }

            QPushButton {
                background-color: white;
                color: black;
                border: 1px solid #CCCCFF;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover { 
                background-color: #CCCCFF;
                color: black;
            }
            QSlider::handle:horizontal {
                background: #CCCCFF;
                border: 1px solid #CCCCFF;
                width: 20px;
            }
            QSlider::handle:vertical {
                background: #CCCCFF;
                border: 1px solid #CCCCFF;
                width: 20px;
            }
            QComboBox {
                background-color: white;
                border: 1px solid #CCCCFF;
                padding: 1px 18px 1px 3px;
            }
            QComboBox:hover {
                background-color: #CCCCFF;
                border: 1px solid #CCCCFF;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #CCCCFF;
            }
            QComboBox QAbstractItemView {
                background: #CCCCFF;
                border: 1px solid #CCCCFF;
            }
            QProgressBar {
                border: 2px solid #CCCCFF;
                border-radius: 5px;
                background: white;
                padding: 1px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #CCCCFF;
                width: 5px;
                margin: 0.5px;
            }
        '''
        self.setStyleSheet(style_sheet)




if __name__ == "__main__":
    app = QApplication([])
    window = MainApp()
    window.show()
    app.exec_()
