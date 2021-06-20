from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .forms import RegisterationForm, DocumentForm, TranscriptForm
from .models import Document, Transcript
from .helpers.gcp import CloudStorage, SpeechToText
from .helpers import video_editor as ve

import json, os, mimetypes, re

def index(request):
    return render(request, 'auto_subtitles/index.html')

def signup(request):
    if request.method == "POST":
        form = RegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = RegisterationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def model_form_upload(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        user_docs = Document.objects.filter(user=request.user.pk)
        user_storage = sum([doc.size for doc in user_docs])
        file_size = request.FILES['document'].size
        if form.is_valid() and request.FILES['document'].content_type.split('/')[0] == 'video' and user_storage + file_size <= 1:
            document = form.save(commit=False)
            document.user = request.user
            document.document.name = '{}/{}'.format(document.user.id, str(document.document))
            document.size = document.document.size / 1000000000
            document.name = str(document.document).split('/')[-1]
            document.save()
            # send file to bucket
            filepath = str(document.document)
            filepath = 'media/{}'.format(filepath)
            filename = filepath.replace('media/documents/', '')
            cs = CloudStorage()
            cs.upload_blob(filepath, filename)
            # extract audio and send to bucket
            ve.video_to_audio(filepath)
            audio_filepath = filepath.replace('.mp4', '.flac')
            audio_filename = audio_filepath.replace('media/documents/', '')
            cs.upload_blob(audio_filepath, audio_filename)
            # get trenscript
            stt = SpeechToText(document.language)
            results = stt.speech_to_text(audio_filename)
            results_dict = stt.text_object_to_dict(results)
            # create transcript object
            transcript = Transcript(transcript=json.dumps(results_dict))
            transcript.save()
            document.transcript = transcript
            document.save()
            return redirect('generate', document_id=document.pk)
    else:
        form = DocumentForm()
    return render(request, 'auto_subtitles/upload.html', { 'form': form })

@login_required
def generate_video(request, document_id):
    # after validating transcript, save it and add it to video
    document = get_object_or_404(Document, pk=document_id)
    transcript = get_object_or_404(Transcript, pk=document.transcript_id)
    results = json.loads(transcript.transcript)

    # download vido if it's not savec locally
    if not os.path.exists(document.document.path):
        cs = CloudStorage()
        filepath = str(document.document)
        filepath = 'media/{}'.format(filepath)
        source_blob_name = '{}/{}'.format(document.user.pk, document.name)
        cs.download_blob(source_blob_name, filepath)

    # set the preview time to 0.1s or the time in the query parameters
    video_duration = ve.get_duration(document.document.path)
    preview_path = ve.get_static_preview(ve.replace_last(document.document.path, '.', '-subbed.'))

    if request.method == 'POST':
        form = TranscriptForm(instance=transcript, data=request.POST)
        if form.is_valid():
            transcript = form.save(commit=False)
            transcripts = []
            for key in request.POST:
                if key.startswith('transcript-'):
                    transcript_number = key.split("-")[-1]
                    transcripts.append({
                        "transcript": request.POST[key],
                        "start_time": request.POST['transcript_start-{}'.format(transcript_number)],
                        "end_time": request.POST['transcript_end-{}'.format(transcript_number)],
                    })
            new_transcript = ve.replace_in_transcript(results, transcripts)
            transcript.transcript = json.dumps(new_transcript)
            transcript.save()
            # apply transcript to video
            filepath = str(document.document)
            filename = filepath.replace('documents/', '')
            subs = ve.create_subtitles(results["results"])
            ve.add_subs_to_video(subs, filename, transcript, request.POST['text_x'], request.POST['text_y'])
            # create new preview
            preview_path = ve.get_static_preview(ve.replace_last(document.document.path, '.', '-subbed.'))
    else:
        form = TranscriptForm(instance=transcript)

    transcripts = ve.create_subtitles(results["results"])
    download_link = '/generate/{}/download'.format(document.pk)
    save_link = download_link.replace('download', 'save')
    return render(request, 'auto_subtitles/generate.html', {
        'form': form,
        'transcripts': transcripts,
        'download_link': download_link,
        'save_link': save_link,
        'preview': preview_path,
        'video_duration': video_duration,
    })

@login_required
def download(request, document_id):
    if request.method == 'POST':
        document = Document.objects.get(pk=document_id)
        path = ve.replace_last(str(document.document), '.', '-subbed.')
        path = os.path.join(settings.MEDIA_ROOT, path)
        filename = path.split('/')[-1]
        with open(path, 'rb') as fl:
            mime_type, _ = mimetypes.guess_type(path)
            response = HttpResponse(fl.read(), content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" % filename
            return response
        raise Http404
    return redirect('generate', document_id=document_id)

@login_required
def save_video(request, document_id):
    if request.method == 'POST':
        document = Document.objects.get(pk=document_id)
        path = ve.replace_last(str(document.document), '.', '-subbed.')
        path = os.path.join(settings.MEDIA_ROOT, path)
        if os.path.exists(path):
            # save it to gcp
            filepath = ve.replace_last(str(document.document), '.', '-subbed.')
            filepath = 'media/{}'.format(filepath)
            filename = filepath.replace('media/documents/', '')
            cs = CloudStorage()
            cs.upload_blob(filepath, filename)
            # delete video from local documents folder
            if os.path.exists(document.document.path):
                os.remove(document.document.path)
    return redirect('index')        

@login_required
def videos(request):
    documents = Document.objects.filter(user=request.user.pk)
    return render(request, 'auto_subtitles/videos.html', { 'documents': documents })

@login_required
def profile(request):
    documents = Document.objects.filter(user=request.user.pk)
    storage_used = sum([doc.document.size for doc in documents])
    storage_used_ko = round(storage_used / 1000, 2)
    storage_used_mo = round(storage_used / 1000000, 5)
    storage_used_go = round(storage_used / 1000000000, 8)
    return render(request, 'registration/profile.html', { 'storage_used_ko': storage_used_ko, 'storage_used_mo': storage_used_mo, 'storage_used_go': storage_used_go, 'max_storage': '1Go' })