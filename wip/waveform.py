import json
import os

import librosa


def generate_waveform(audio_file, json_file, sr=200):
    data, _ = librosa.load(audio_file, sr=sr)
    dic = {'waveform': data.tolist()}
    with open(json_file, 'w') as file:
        json.dump(dic, file, indent=2)


if __name__ == '__main__':
    generate_waveform(
        os.path.join('data', 'Curson_original.mp3'),
        os.path.join('data', 'waveform.json')
    )
