# 📦 Required Imports
import whisper
import moviepy.editor as mp
from pydub import AudioSegment
from gtts import gTTS
import os
from deep_translator import GoogleTranslator
from langdetect import detect
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# 📁 File Picker (Instead of Colab's file upload)
print("📁 Please select a video file...")
Tk().withdraw()  # Hide root window
video_path = askopenfilename(title="Select video file")

if not video_path:
    print("❌ No file selected. Exiting.")
    exit()

print(f"📄 Selected file: {video_path}")

# 🎞️ Extract audio from video
clip = mp.VideoFileClip(video_path)
clip.audio.write_audiofile("extracted_audio.wav")

# 🧠 Transcribe with timestamps using Whisper
print("🧠 Transcribing with timestamps...")
model = whisper.load_model("base")
result = model.transcribe("extracted_audio.wav")

segments = result['segments']
full_text = result['text']
detected_lang = detect(full_text)

print(f"\n📜 Full Transcription: {full_text}")
print(f"🗣️ Detected Language: {detected_lang}")


# 🌍 Translation targets 
target_languages = {
    'af': 'Afrikaans',
    'ar': 'Arabic',
    'bn': 'Bengali',
    'zh-cn': 'Chinese (Simplified)',
    'zh-tw': 'Chinese (Traditional)',
    'nl': 'Dutch',
    'en': 'English',
    'fr': 'French',
    'de': 'German',
    'gu': 'Gujarati',
    'hi': 'Hindi',
    'it': 'Italian',
    'ja': 'Japanese',
    'kn': 'Kannada',
    'ml': 'Malayalam',
    'mr': 'Marathi',
    'pa': 'Punjabi',
    'ta': 'Tamil',
    'te': 'Telugu',
    'ur': 'Urdu'
}

# 🧠 Ask user to choose target language
print("\nChoose a language to translate the video into:")
for code, lang in target_languages.items():
    print(f"{code} - {lang}")

while True:
    selected_lang_code = input("Enter the language code: ").strip().lower()
    if selected_lang_code in target_languages:
        selected_lang_name = target_languages[selected_lang_code]
        break
    else:
        print("Invalid code. Try again.")

print(f"\n🔁 Translating to: {selected_lang_name}")

# 🎙️ Translate + TTS for each segment with silence padding
translated_segments = []
for idx, segment in enumerate(segments):
    start = segment['start']
    end = segment['end']
    duration_ms = int((end - start) * 1000)
    original_text = segment['text']

    # Translate segment
    translated_text = GoogleTranslator(source=detected_lang, target=selected_lang_code).translate(original_text)

    # TTS
    tts = gTTS(translated_text, lang=selected_lang_code)
    tts_path = f"segment_{idx}.mp3"
    tts.save(tts_path)

    # Load and fit into original duration
    audio = AudioSegment.from_file(tts_path)
    if len(audio) > duration_ms:
        audio = audio[:duration_ms]
    else:
        padding = AudioSegment.silent(duration=(duration_ms - len(audio)))
        audio = audio + padding

    translated_segments.append((start, audio))

# 🔊 Stitch with silence gaps
final_audio = AudioSegment.silent(duration=0)

for start_time, seg_audio in translated_segments:
    start_ms = int(start_time * 1000)
    if start_ms > len(final_audio):
        gap = AudioSegment.silent(duration=(start_ms - len(final_audio)))
        final_audio += gap
    final_audio += seg_audio

final_audio.export("final_translated_audio.mp3", format="mp3")

# 🎬 Replace original audio with translated audio
video_clip = mp.VideoFileClip(video_path)
audio_clip = mp.AudioFileClip("final_translated_audio.mp3")
audio_clip = audio_clip.set_duration(video_clip.duration)

final_video = video_clip.set_audio(audio_clip)
final_video.write_videofile("translated_video.mp4")

print("\n✅ Done! Translated video saved as 'translated_video.mp4'")

