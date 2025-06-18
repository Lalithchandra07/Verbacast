from django.shortcuts import render,redirect
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from gtts import gTTS
from googletrans import Translator
from django.core.files.storage import default_storage
from transformers import pipeline
from django.http import JsonResponse 



def home(request):
    return render(request, 'app/home.html')

def about(request):
    return render(request, 'app/about.html')


def user_register(request):
    form=UserRegistrationForm #empty form 
    context={'form':form}

    if request.method=="GET":
        return render(request,'app/register.html',context)
    
    if request.method=="POST":
        #request .POST contains user submitted data (form data)
        form=UserRegistrationForm(request.POST) #user submitted form

        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            context['error']='invalid form submission,try again'
            return render(request,'app/register.html',context)

def user_login(request):
    if request.method == "GET":
        return render(request, 'app/login.html')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)  # returns user object

        if user is not None:  # if user exists
            login(request, user)
            return render(request, 'app/translate_video.html')  # render translator.html directly
        else:
            error = 'Invalid username or password'
            context = {'error': error}
            return render(request, 'app/login.html', context)

        
                                                              
def user_logout(request):
    logout(request)
    return redirect('login')



# @login_required(login_url='login')  # Redirects to 'login' page if not authenticated
# def translator(request):
#     return render(request, 'app/translator.html')


from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import default_storage
from moviepy.editor import VideoFileClip, AudioFileClip
from pydub import AudioSegment
from gtts import gTTS
from deep_translator import GoogleTranslator
from langdetect import detect
import whisper
import os
from .forms import VideoUploadForm



@login_required(login_url='login')
def translate_video_view(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video_file = request.FILES['video_file']
            lang_code = form.cleaned_data['language_code']
            
            saved_path = default_storage.save('uploads/' + video_file.name, video_file)
            abs_path = os.path.join(settings.MEDIA_ROOT, saved_path)

            # Extract audio
            clip = VideoFileClip(abs_path)
            audio_path = os.path.join(settings.MEDIA_ROOT, 'extracted_audio.wav')
            clip.audio.write_audiofile(audio_path)

            # Transcribe with Whisper
            model = whisper.load_model("base")
            result = model.transcribe(audio_path)
            segments = result['segments']
            full_text = result['text']
            detected_lang = detect(full_text)

            # Translate and generate audio
            translated_segments = []
            translated_captions = []
            for idx, segment in enumerate(segments):
                start = segment['start']
                end = segment['end']
                duration_ms = int((end - start) * 1000)
                original_text = segment['text']

                translated_text = GoogleTranslator(source=detected_lang, target=lang_code).translate(original_text)
                tts = gTTS(translated_text, lang=lang_code)
                tts_path = os.path.join(settings.MEDIA_ROOT, f"tts_{idx}.mp3")
                tts.save(tts_path)

                audio = AudioSegment.from_file(tts_path)
                if len(audio) > duration_ms:
                    audio = audio[:duration_ms]
                else:
                    padding = AudioSegment.silent(duration=(duration_ms - len(audio)))
                    audio += padding

                translated_segments.append((start, audio))
                translated_captions.append(f"{round(start, 2)}s - {round(end, 2)}s: {translated_text}")

            final_audio = AudioSegment.silent(duration=0)
            for start_time, seg_audio in translated_segments:
                start_ms = int(start_time * 1000)
                if start_ms > len(final_audio):
                    final_audio += AudioSegment.silent(duration=(start_ms - len(final_audio)))
                final_audio += seg_audio

            final_audio_path = os.path.join(settings.MEDIA_ROOT, "final_translated_audio.mp3")
            final_audio.export(final_audio_path, format="mp3")

            audio_clip = AudioFileClip(final_audio_path).set_duration(clip.duration)
            final_video = clip.set_audio(audio_clip)

            output_video_path = os.path.join(settings.MEDIA_ROOT, 'translated_video.mp4')
            final_video.write_videofile(output_video_path, codec='libx264', audio_codec='aac')

            return JsonResponse({
                'video_url': settings.MEDIA_URL + 'translated_video.mp4',
                'translated_captions': translated_captions
            })
    else:
        form = VideoUploadForm()

    return render(request, 'app/translate_video.html', {'form': form})



