import sounddevice as sd
import numpy as np
import whisper
import edge_tts
import asyncio
import os
import wave
import pygame
import requests
import threading
from pynput import keyboard

# ✅ Load Whisper Model
whisper_model = whisper.load_model("small.en")

# ✅ LM Studio / Ollama Configuration
LM_STUDIO_URL = "http://localhost:11434/api/generate"  # Change if needed
MODEL_NAME = "mistral"  # Change to your LLM model name

# ✅ Audio Configuration
MIC_DEVICE_INDEX = 32  # Set your microphone index
SAMPLE_RATE = 48000  # Your mic's sample rate
BLOCK_SIZE = 1024  # Audio block size

sd.default.device = MIC_DEVICE_INDEX  # Force correct mic

# ✅ Push-to-Talk State
recording = False
audio_buffer = []
stop_playback = False  # Flag to stop speech mid-answer
playback_thread = None  # Thread for playing audio


def stop_current_answer():
    """Stops the current response playback and prepares for the next question."""
    global stop_playback, playback_thread
    stop_playback = True  # Set flag to stop playback
    print("🔴 Answer interrupted. Ready for next question.")

    # Stop playback immediately
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
        pygame.mixer.quit()

    # If the TTS playback thread is still running, forcefully stop it
    if playback_thread and playback_thread.is_alive():
        playback_thread.join(timeout=1)


def generate_response(prompt):
    """Sends transcribed text to LM Studio/Ollama for an AI-generated response."""
    if not prompt.strip():
        return "I didn't hear anything. Can you repeat that?"

    print(f"🤖 Sending to LLM: {prompt}")

    response = requests.post(
        LM_STUDIO_URL,
        json={"model": MODEL_NAME, "prompt": prompt, "stream": False}
    )

    if response.status_code == 200:
        answer = response.json().get("response", "I didn't understand that.")
        print(f"🤖 AI Response: {answer}")
        return answer
    else:
        print(f"❌ ERROR: Failed to get response from LLM ({response.status_code})")
        return "I'm having trouble thinking right now."


async def speak_async(text):
    """Uses Edge TTS to speak the response."""
    global stop_playback
    print(f"🔊 Generating TTS audio for: {text}")

    output_file = "output.mp3"
    tts = edge_tts.Communicate(text, voice="en-US-AriaNeural")
    await tts.save(output_file)

    if stop_playback:
        print("⏹️ Playback was interrupted before starting.")
        return  # Don't play audio if interrupted

    play_audio(output_file)


def play_audio(file):
    """Plays the generated TTS audio in a separate thread."""
    global stop_playback, playback_thread
    stop_playback = False  # Reset playback stop flag

    def audio_thread():
        if stop_playback:
            print("⏹️ Playback was already interrupted before it started.")
            return

        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()

        while pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            if stop_playback:  # Check if user interrupted playback
                pygame.mixer.music.stop()
                print("⏹️ Playback interrupted!")
                break
            pygame.time.Clock().tick(10)

        pygame.mixer.quit()  # Ensure it's fully released
        os.remove(file)  # Clean up
        print("✅ Audio playback finished and file removed.")

    # Start a separate thread for playback
    playback_thread = threading.Thread(target=audio_thread)
    playback_thread.start()


def speak(text):
    """Runs the async TTS function."""
    global stop_playback
    stop_playback = False  # Reset playback stop flag
    print(f"🗣️ Speaking: {text}")
    asyncio.run(speak_async(text))


def start_recording():
    """Start capturing audio when Shift key is pressed."""
    global recording, audio_buffer
    if not recording:  # Prevent spamming
        recording = True
        audio_buffer = []  # Reset buffer
        print("🎤 Recording started... Speak now!")


def stop_recording():
    """Stop recording only if currently recording."""
    global recording
    if recording:
        recording = False
        print("🔄 Processing audio...")
    else:
        print("❌ Not recording, ignoring stop command.")

    if len(audio_buffer) == 0:
        print("❌ No audio recorded!")
        return

    # ✅ Limit recording size (avoid excessive memory usage)
    MAX_SAMPLES = SAMPLE_RATE * 10  # 10 seconds max
    recorded_audio = np.concatenate(audio_buffer, axis=0)[:MAX_SAMPLES]

    # ✅ Ensure audio is in float32 format
    recorded_audio = recorded_audio.astype(np.float32)

    # ✅ Save to a temporary WAV file (required by Whisper)
    temp_wav = "temp_recording.wav"
    with wave.open(temp_wav, 'wb') as wf:
        wf.setnchannels(1)  # Mono audio
        wf.setsampwidth(2)  # 16-bit audio
        wf.setframerate(SAMPLE_RATE)  # Set sample rate
        wf.writeframes((recorded_audio * 32768).astype(np.int16).tobytes())

    # ✅ Transcribe with Whisper
    text = whisper_model.transcribe(temp_wav, fp16=False)["text"]
    os.remove(temp_wav)  # Cleanup WAV file
    print(f"📝 You said: {text}")

    # ✅ Get AI Response
    response = generate_response(text)

    # ✅ Speak Response
    speak(response)


def audio_callback(indata, frames, time, status):
    """Continuously records audio while Shift key is held and converts to float32."""
    if recording:
        audio_buffer.append(indata.copy().astype(np.float32) / 32768.0)


def keyboard_listener():
    """Listens for the Shift key to start/stop recording and Esc to interrupt playback."""
    def on_press(key):
        global stop_playback
        if key == keyboard.Key.shift:  # Use Shift instead of Space
            stop_playback = False  # Reset flag when recording starts
            start_recording()
        elif key == keyboard.Key.esc:  # Interrupt playback
            print("⏹️ Escape key pressed! Stopping playback...")
            stop_current_answer()

    def on_release(key):
        if key == keyboard.Key.shift:
            stop_recording()

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


# ✅ Start the audio stream
with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="int16",
                    blocksize=BLOCK_SIZE, callback=audio_callback):
    print("🎧 Hold the SHIFT key to talk, press ESC to stop speech.")
    keyboard_listener()
