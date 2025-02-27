import sounddevice as sd
import numpy as np
import json

import torch
from vosk import Model, KaldiRecognizer

# Load Vosk Model
vosk_model_path = r"C:\Users\kidpr\PycharmProjects\LLMVA\vosk-model-small-en-us-0.15"
vosk_model = Model(vosk_model_path)
recognizer = KaldiRecognizer(vosk_model, 16000)  # Vosk needs 16kHz input

# Set Mic Device & Sample Rate
MIC_DEVICE_INDEX = 32  # Your webcam mic
SAMPLE_RATE = 48000  # Your mic supports 48kHz

sd.default.device = MIC_DEVICE_INDEX

# Function to resample 48kHz -> 16kHz
import torchaudio
def resample_audio(audio_array):
    waveform = np.array(audio_array, dtype=np.float32)
    waveform = torch.tensor(waveform).unsqueeze(0)  # Convert to tensor
    waveform_resampled = torchaudio.transforms.Resample(48000, 16000)(waveform).squeeze(0)
    return waveform_resampled.numpy()

print("🎤 Speak something for 10 seconds...")

with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="int16", blocksize=1024) as stream:
    recorded_audio = []
    for _ in range(0, int(SAMPLE_RATE / 1024 * 10)):  # Listen for 10 seconds
        audio_data = stream.read(1024)[0]
        audio_array = np.frombuffer(audio_data, dtype=np.int16)
        recorded_audio.append(audio_array)

recorded_audio = np.concatenate(recorded_audio, axis=0)
resampled_audio = resample_audio(recorded_audio)

# Pass to Vosk and print intermediate results
recognizer.AcceptWaveform(resampled_audio.tobytes())
partial_result = recognizer.PartialResult()  # Get intermediate speech text
final_result = recognizer.FinalResult()  # Get full result

print(f"🔄 Partial Vosk Output: {partial_result}")  # Debug: Show partial words
print(f"✅ Final Vosk Output: {final_result}")  # Debug: Show final recognition
