🎤 Local AI Voice Assistant (Push-to-Talk)
This project is a voice-controlled AI assistant that:

Listens when you hold the Shift key
Transcribes speech using Whisper
Sends the text to Ollama / LM Studio for AI responses
Speaks the response using Edge TTS

🚀 Installation

✅ Step 1: Clone the Repository

git clone https://github.com/your-repo-name/your-project-name.git
cd your-project-name
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows

✅ Step 3: Install Dependencies

pip install -r requirements.txt

🏠 Ollama Setup
Ollama is used to run local AI models for generating responses.

✅ Step 1: Install Ollama
Windows / Mac / Linux: Download Ollama
Run the installer and restart your terminal after installation.

✅ Step 2: Pull an AI Model
Before running the assistant, download an AI model (e.g., mistral):

ollama pull mistral
Other available models:

gemma
llama2
phi
codellama

✅ Step 3: Start Ollama
Make sure Ollama is running in the background:

ollama serve

🎙️ Check Your Microphone Device Index
Run the following test script to find your microphone index:

import sounddevice as sd
print(sd.query_devices())
Update MIC_DEVICE_INDEX in assistant.py with your correct mic index.

🎬 Usage
Run the Assistant

python assistant.py

How to Use
Press & Hold the Shift key to record your question.
Release the Shift key → The assistant transcribes & sends it to Ollama.
Ollama generates a response, and the assistant speaks it.

The answers can be rather long and detailed so press Escape if you want to cut off the spoken response.

🛠 Troubleshooting
❌ No AI Response?
Ensure Ollama is running (ollama serve).
Try switching models by updating MODEL_NAME in assistant.py.
❌ Microphone Issues?
Check your mic index (sd.query_devices()).
Ensure your mic is set to 16-bit, 48000 Hz in Windows Sound Settings.
❌ TTS (Speech) Doesn’t Work?
Check console logs for ❌ ERROR: TTS output file was not created!
Ensure Edge TTS is installed (pip install edge-tts).

🤝 Contributing
Feel free to fork, modify, and submit pull requests! 🚀

📜 License
MIT License - Use, modify, and distribute freely.

🎉 Now You Have a Local AI Voice Assistant!
🚀 Try it out and let me know if you have any questions! 🔥🎙️







You said:
give me the readme in a format i can just copy paste
ChatGPT said:
Here’s the README.md in a clean copy-paste format:

md
Copy
Edit
# 🎤 Local AI Voice Assistant (Push-to-Talk)

This project is a **voice-controlled AI assistant** that:
- **Listens when you hold the Space key**
- **Transcribes speech using Whisper**
- **Sends the text to Ollama for AI responses**
- **Speaks the response using Edge TTS**

---

## 🚀 Installation

### ✅ Step 1: Clone the Repository
```bash
git clone https://github.com/your-repo-name/your-project-name.git
cd your-project-name
✅ Step 2: Set Up a Virtual Environment (Recommended)
bash
Copy
Edit
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows
✅ Step 3: Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
🏠 Ollama Setup
Ollama is used to run local AI models for generating responses.

✅ Step 1: Install Ollama
Windows / Mac / Linux: Download Ollama
Run the installer and restart your terminal after installation.

✅ Step 2: Pull an AI Model
Before running the assistant, download an AI model (e.g., mistral):

ollama pull mistral

Other available models:
gemma
llama2
phi
codellama

✅ Step 3: Start Ollama
Make sure Ollama is running in the background:

ollama serve

🎙️ Check Your Microphone Device Index
Run the following test script to find your microphone index:

import sounddevice as sd
print(sd.query_devices())

Update MIC_DEVICE_INDEX in assistant.py with your correct mic index.

🎬 Usage
Run the Assistant

python assistant.py

How to Use

Press & Hold the Space key to record your question.
Release the Space key → The assistant transcribes & sends it to Ollama.
Ollama generates a response, and the assistant speaks it.

🛠 Troubleshooting
❌ No AI Response?
Ensure Ollama is running (ollama serve).
Try switching models by updating MODEL_NAME in assistant.py.
❌ Microphone Issues?
Check your mic index (sd.query_devices()).
Ensure your mic is set to 16-bit, 48000 Hz in Windows Sound Settings.
❌ TTS (Speech) Doesn’t Work?
Check console logs for ❌ ERROR: TTS output file was not created!
Ensure Edge TTS is installed (pip install edge-tts).
🤝 Contributing
Feel free to fork, modify, and submit pull requests! 🚀
