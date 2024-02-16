import sounddevice as sd
import wavio as wv
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

from PyQt5.QtWidgets import QFileDialog
import numpy as np
import os
from PyQt5.QtWidgets import QApplication, QLabel, QFrame, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
import pyqtgraph as pg
from scipy.io import wavfile
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5 import QtCore
from PyQt5.QtCore import QUrl, QTimer
import vlc
from pydub import AudioSegment
import os
import csv
from sklearn.preprocessing import StandardScaler
import numpy as np
import sys, os
from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtGui import QMovie
import librosa
from sklearn.metrics.pairwise import cosine_similarity
from pydub import AudioSegment
import os
import pyaudio
import wave
from scipy.io import wavfile
import threading
import librosa
from scipy.io import wavfile
from pydub.playback import play
from scipy.signal import gaussian
import pyaudio
from pydub.playback import play
import vlc

from scipy.signal import find_peaks
from pyqtgraph import PlotWidget, ImageItem
from pydub import AudioSegment
import librosa.display  # Import librosa's display module

AudioSegment.converter = "C:\\Program Files (x86)\\ffmpeg-master-latest-win64-gpl\\ffmpeg.exe"

class Logic():
    def __init__(self, ui_instance):
        self.ui_instance = ui_instance
        main_folder = "samples"
        _ = self.process_reference_files(main_folder,1)
        word_folder = "word_sample"
        _ = self.process_reference_files(word_folder,2)
        


    def record_and_process_voice(self):
        # if self.ui_instance.boxMode.currentIndex() == 0:
            self.filename = self.ui_instance.filename_lineedit.text()

            try:
                fs = 44100

                # Record audio
                recording = sd.rec(3 * fs, samplerate=fs, channels=2)
                sd.wait()
                wv.write(self.filename, recording, fs, sampwidth=2)
                self.plot_spectrogram()
                input_mfccs = self.calc_mfccs(self.filename)
                mean_mfcc = np.mean(input_mfccs, axis=1)
                result = self.detect_persion(mean_mfcc, np.load("reference_features.npy", allow_pickle=True).item())
                person = self.detect_word(mean_mfcc, np.load("reference_features1.npy", allow_pickle=True).item())
                message = person + result
                # self.message_change_person(message)

                # Display status label



            except Exception as e:
                print(e)


    def message_change_person(self, message):
        self.ui_instance.person_status.show()
        self.ui_instance.person_status.setText(message)
        print(message)
        self.ui_instance.timerPerson.start(5000)

    def hide_person_status(self):
        self.ui_instance.person_status.hide()
        self.ui_instance.timerPerson.stop()

    def message_change_word(self, message):
        self.ui_instance.word_status.show()
        self.ui_instance.word_status.setText(message)
        print(message)
        self.ui_instance.timerWord.start(5000)

    def hide_word_status(self):
        self.ui_instance.word_status.hide()
        self.ui_instance.timerWord.stop()

    def calc_mfccs(self,audio_file):
        y, sr = librosa.load(audio_file, sr=None)
        # # Normalize the raw audio data
        # scaler = StandardScaler()
        # y_normalized = scaler.fit_transform(y.reshape(-1, 1)).flatten()
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

        return mfccs

    def process_reference_files(self,root_folder,num):


        # Create a dictionary to store reference features
        reference_features = {}

        # Loop over reference files
        for foldername, subfolders, filenames in os.walk(root_folder):
            # Create a list to store features for each folder
            folder_features = []

            for filename in filenames:
                if filename.endswith(".wav"):
                    reference_file = os.path.join(foldername, filename)
                    features = self.calc_mfccs(reference_file)
                    mean_features = np.mean(features, axis=1)

                    folder_features.append(mean_features)

            # Add foldername and its corresponding features to the dictionary
            if folder_features:  # only save if there are features extracted
                # foldername = foldername.replace("samples/", "").lower()

                reference_features[foldername] = folder_features

        if num ==1:
        # Save reference features for later comparison
           np.save("reference_features.npy", reference_features)
        else:
            np.save("reference_features1.npy", reference_features)


        return reference_features


    def plot_spectrogram(self):
        path=self.filename
        self.yData, self.f_rate = librosa.load(path,sr=None)


        self.ui_instance.plotSpec.getFigure().clear()

        # Access the toolbar and hide it
        spectrogram_axes = self.ui_instance.plotSpec.getFigure().add_subplot(111)

        # Ensure that 'data' is a one-dimensional array
        data = self.yData.astype('float32').ravel()


        # Choose a suitable value for n_fft based on the length of the input signal
        n_fft = min(2048, len(data))


        # Compute the spectrogram
        frequency_magnitude = np.abs(librosa.stft(data, n_fft=n_fft)) ** 2

        mel_spectrogram = librosa.feature.melspectrogram(S=frequency_magnitude, sr=self.f_rate, n_mels=1024)

        # Convert power spectrogram to dB scale
        decibel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)

        # Display the spectrogram
        spectrogram_image = librosa.display.specshow(decibel_spectrogram, x_axis='time', y_axis='mel', sr=self.f_rate,
                                                     ax=spectrogram_axes)

        colorbar = self.ui_instance.plotSpec.getFigure().colorbar(spectrogram_image, ax=spectrogram_axes,
                                                                        format='%+2.0f dB')

        # Get the x-axis limits from the colorbar
        x_range = colorbar.ax.get_xlim()
        self.spectrogram_time_min, self.spectrogram_time_max = x_range

        # Draw the spectrogram
        self.ui_instance.plotSpec.draw()

    def add_features_to_person(self,reference_features):

        combined_features = {}
        speakers = {
            "samples\mohammed_nagar": [],
            # "samples\omar": [],
            "samples\hesham": [],
            "samples\gamica": [],
            "samples\marwan": [],
            "samples\sarah": [],
            "samples\osama": [],
            "samples\emir": [],
            "samples\mohamed": []
        }

        for key in reference_features.keys():
            if "samples\mohammed_nagar" in key.lower():
                speakers["samples\mohammed_nagar"].extend(reference_features[key])
            if "samples\hesham" in key.lower():
                speakers["samples\hesham"].extend(reference_features[key])
            elif "samples\marwan" in key.lower():
                speakers["samples\marwan"].extend(reference_features[key])
            elif "samples\gamica" in key.lower():
                speakers["samples\gamica"].extend(reference_features[key])
            elif "samples\sarah" in key.lower():
                speakers["samples\sarah"].extend(reference_features[key])
            elif "samples\osama" in key.lower():
                speakers["samples\osama"].extend(reference_features[key])
            #
            elif "samples\mohamed" in key.lower():
                speakers["samples\mohamed"].extend(reference_features[key])
            elif "samples\emir" in key.lower():
                speakers["samples\emir"].extend(reference_features[key])

        for speaker, features in speakers.items():
            combined_features[speaker] = np.mean(features, axis=0)


        return combined_features

    def add_features_to_word(self,reference_features):
        combined_features = {}
        words = {
            "open_middle_door": [],
            "grant_me_access": [],
            "unlock_the_gate": [],
        }

        for key in reference_features.keys():
            if "open_middle_door" in key.lower():
                words["open_middle_door"].extend(reference_features[key])
            elif "grant_me_access" in key.lower():
                words["grant_me_access"].extend(reference_features[key])
            elif "unlock_the_gate" in key.lower():
                words["unlock_the_gate"].extend(reference_features[key])

        for word, features in words.items():
            combined_features[word] = np.mean(features, axis=0)

        return combined_features

    def detect_persion(self,input_features, reference_features):
        # Loop through the reference features to compare with the input
        speakers = self.add_features_to_person(reference_features)


        min_distance = 100
        recognized_speaker = None


        threshold = 16

        table_accuracy = []
        person_similarities = []

        for speaker, features in speakers.items():
            # similarity = compare_features(input_features.reshape(1, -1), np.array(features).reshape(1, -1))
            distance = self.calculate_ecludian_distance(input_features.reshape(1, -1), np.array(features).reshape(1, -1))
            table_accuracy.append((speaker, distance))
            person_similarities.append((speaker, distance))
            if distance < min_distance:
                min_distance = distance
                recognized_speaker = speaker

        self.calc_probabilities_person(table_accuracy)

        if recognized_speaker is not None and min_distance <= threshold:
            self.message_change_person(f"Person recognized as{recognized_speaker}")
            return recognized_speaker
        self.message_change_person("Person not recognized")
        return "Person not recognized"

    def detect_word(self,input_features, reference_features):
        # Loop through the reference features to compare with the input
        words = self.add_features_to_word(reference_features)
        min_distance = 100
        recognized_word = None
        threshold = 17

        word_similarities = []
        table_accuracy = []

        for word, features in words.items():
            distance = self.calculate_ecludian_distance(input_features.reshape(1, -1), np.array(features).reshape(1, -1))

            word_similarities.append((word, distance))
            table_accuracy.append((word, distance))
            if distance <= min_distance:
                min_distance = distance
                recognized_word = word

        self.calc_probabilities_word(table_accuracy)
        if recognized_word is not None and min_distance < threshold:
            self.message_change_word(f"Word recognized as{recognized_word}")
            return recognized_word
        self.message_change_word("Word not recognized")
        return "Word not recognized"
    
    def calc_probabilities_person(self, table_accuracy):
        total_distance = sum(item[1] for item in table_accuracy)
        result = [[]]
        # Get the current item's row index
        # Get the total distance (replace this with your actual total_distance calculation)
        # Loop through all rows of the table
        # Loop through all rows of the list
        for row in table_accuracy:
            # Assuming each row is a list with at least two elements (speaker and distance)
            if len(row) >= 2:
                speaker = str(row[0])
                distance = float(row[1])

                # Append the result tuple to the 'result' list
                result.append((speaker, round((total_distance - distance) * 100 / total_distance, 2)))
                
        print("person percentages", result)
        self.table_persons(result)
    def calc_probabilities_word(self, table_accuracy):
        total_distance = sum(item[1] for item in table_accuracy)
        result = [[]]
        # Get the current item's row index
        # Get the total distance (replace this with your actual total_distance calculation)
        # Loop through all rows of the table
        # Loop through all rows of the list
        for row in table_accuracy:
            # Assuming each row is a list with at least two elements (speaker and distance)
            if len(row) >= 2:
                speaker = str(row[0])
                distance = float(row[1])

                # Append the result tuple to the 'result' list
                result.append((speaker, round((total_distance - distance) * 100 / total_distance, 2)))

        print("word percentages", result)
        self.table_words(result)
    def table_words(self, result):
            self.ui_instance.tableWidget_2.clearContents()

            # Set the number of rows and columns based on the data
            self.ui_instance.tableWidget_2.setRowCount(len(result))
            self.ui_instance.tableWidget_2.setColumnCount(2)

            # Populate the table with data
            for row, item in enumerate(result):
                for col, value in enumerate(item):
                    table_item = QTableWidgetItem(str(value))
                    self.ui_instance.tableWidget_2.setItem(row-1, col, table_item)
        
    def table_persons(self, result):
            self.ui_instance.tableWidget.clearContents()

            # Set the number of rows and columns based on the data
            self.ui_instance.tableWidget.setRowCount(len(result))
            self.ui_instance.tableWidget.setColumnCount(2)

            # Populate the table with data
            for row, item in enumerate(result):
                for col, value in enumerate(item):
                    table_item = QTableWidgetItem(str(value))
                    self.ui_instance.tableWidget.setItem(row-1, col, table_item)
        
    def calculate_ecludian_distance(self,features1, features2):
        # Reshape to have the same number of columns for comparison
        features1 = features1.T
        features2 = features2.T

        # Compute ecludian distance
        distance_matrix = np.linalg.norm(features1 - features2, axis=1)

        # Average distance over time
        mean_distance = np.mean(distance_matrix)


        return mean_distance


    # def cross_corellation(self, array_1, array_2):
    #     array_1 /= np.max(np.abs(array_1))
    #     array_2 /= np.max(np.abs(array_2))
    #     correlation_coefficient = np.corrcoef(array_1.flatten(), array_2.flatten())[0, 1]
    #     print(correlation_coefficient)
    #     # peaks, _ = find_peaks(cross_corr)
    #     # print(np.max(cross_c))
    #     if 0.01<correlation_coefficient<0.1:
    #         print("The signals are similar.")
    #     else:
    #         print("The signals are not identical.")



