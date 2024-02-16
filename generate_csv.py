import os
import csv
import numpy as np
import librosa
from scipy.io import wavfile

class AudioProcessor:
    def __init__(self):
        pass

    def load_signal(self, filename):
        f_rate, yData = wavfile.read(filename)
        if len(yData.shape) > 1:
            yData = yData[:, 0]

        yData = yData / (2.0**15) * 4
        SIZE = len(yData)
        xAxisData = np.linspace(0, SIZE / f_rate, num=SIZE)

        return xAxisData, yData, f_rate

    def compute_frequency_magnitude(self, yData, f_rate):
        n_fft = min(2048, len(yData))
        frequency_magnitude = np.abs(librosa.stft(yData, n_fft=n_fft)) ** 2
        mel_spectrogram = librosa.feature.melspectrogram(S=frequency_magnitude, sr=f_rate, n_mels=1024)
        decibel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)
        return np.mean(decibel_spectrogram)

    def process_audio_files(self, audio_folder):
        audio_data = []

        for filename in os.listdir(audio_folder):
            if filename.endswith(".wav"):
                file_path = os.path.join(audio_folder, filename)
                xAxisData, yData, f_rate = self.load_signal(file_path)
                data = yData.astype('float32').ravel()
                n_fft = min(2048, len(data))
                frequency_magnitude = np.abs(librosa.stft(data, n_fft=n_fft)) ** 2

                self.audio_data.append([filename, frequency_magnitude])


    def export_to_csv(self, csv_filename, csv_data):
        with open(csv_filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(['Filename', 'Frequency Magnitude'])
            # Write data rows
            writer.writerows(csv_data)

# Example usage
if __name__ == "__main__":
    processor = AudioProcessor()
    processor.process_audio_files('audio')

