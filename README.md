# 🌌 Aura: Your Intelligent Local AI Assistant !!

Aura is a sophisticated, multimodal AI assistant designed to run locally, providing powerful system automation and personal assistance while prioritizing privacy. It combines a **Python/Flask** backend with a modern **Electron-based** user interface, powered by large language models like **Ollama**.

---

## ✨ Features

### 🛠️ System Automation
- **App Management**: Open and close any application (e.g., Notepad, Chrome, Calculator).
- **System Control**: Restart, shutdown, or sleep your computer.
- **Volume Control**: Effortlessly adjust, mute, or unmute system volume.
- **File System**: Create and delete folders in specified paths or standard locations (Desktop, Documents).
- **Screenshots**: Capture your screen instantly.

### 📱 Communication & Productivity
- **WhatsApp Integration**: Send messages or make voice calls via WhatsApp.
- **Email Drafting**: Generate and send professional emails using AI.
- **Memory System**: Aura remembers details about you—your name, interests, and preferences—to provide a personalized experience.

### 🌐 Information & Media
- **Real-time Web Access**: Search Google, play videos on YouTube, or get definitions for any term.
- **Local Intel**: Get the latest weather updates and top news headlines (Tech, Crypto, etc.).
- **Multilingual Support**: Translate text between multiple languages.
- **Music**: Play your favorite tracks on Spotify.

---

## 🚀 Tech Stack

- **Backend**: Python 3.x, Flask
- **Frontend**: Electron, HTML5, CSS3, JavaScript
- **AI Core**: Ollama (Ollama & Phi-3 models)
- **Voice**: SpeechRecognition, pyttsx3
- **Automation**: pyautogui, pycaw

---

## 🛠️ Installation

### 1. Prerequisites
- **Python 3.x**: [Download here](https://www.python.org/)
- **Node.js**: [Download here](https://nodejs.org/)
- **Ollama**: [Install Ollama](https://ollama.ai/) and ensure the models specified in `config.py` are downloaded.

### 2. Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Anusha-Sekharan/AURA.git
   cd AURA
   ```

2. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install UI Dependencies**:
   ```bash
   cd ui-electron
   npm install
   cd ..
   ```

---

## 🔘 Running Aura

To start Aura, simply run the main Python script from the root directory:

```bash
python main.py
```

This will automatically initialize the Flask backend and launch the Electron interface.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.
