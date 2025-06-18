# 🎥 VerbaCast – Translating Video Audio with Captions

VerbaCast is a Django-powered web application that automates the process of translating video audio into multiple languages while generating synchronized captions. It enables seamless accessibility and content localization across linguistic boundaries.

---

## 🚀 Features

- 🎙️ **Speech Recognition** – Converts spoken audio in videos to text using Whisper.
- 🌍 **Multi-Language Translation** – Supports translation between English, Hindi, Telugu, Tamil, Malayalam, and more via Deep Translator.
- 🔊 **Text-to-Speech (TTS)** – Uses gTTS to generate translated voiceover in the target language.
- 📝 **Auto-Captioning** – Creates accurate, time-synced subtitles.
- 💬 **Bilingual Subtitle Option** – Display original and translated text together.
- 🌐 **Web-Based Interface** – Simple drag-and-drop video upload with language selection.
- 🧠 **Optional Speaker Diarization** – Identify and differentiate between multiple speakers.
- ♿ **Accessibility First** – Designed to break language and audio barriers.

---

## 🛠️ Tech Stack

| Layer             | Technology                  |
|------------------|-----------------------------|
| Backend          | Django (Python)             |
| Frontend         | HTML, CSS, JavaScript       |
| Speech-to-Text   | [Whisper](https://github.com/openai/whisper) |
| Translation      | [deep-translator](https://pypi.org/project/deep-translator/) |
| Text-to-Speech   | [gTTS](https://pypi.org/project/gTTS/) |
| Video Processing | moviepy                     |

---

## 📂 Project Structure

verbacast/
├── core/

│ ├── templates/core/

│ ├── static/core/

│ ├── views.py

│ └── urls.py

├── static/

│ └── app/

├── templates/

├── locale/
├── manage.py


