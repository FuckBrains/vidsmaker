from moviepy import editor
from moviepy.config import change_settings
import os.path as op
import os
import math
from datetime import timedelta

def replace_last(s, old, new):
    last_char_index = s.rfind(old)
    return s[:last_char_index] + new + s[last_char_index+len(old):]

def video_to_audio(filename):
    # Insert Local Video File Path 
    clip = editor.VideoFileClip(filename)
    audio_filename = filename.split(".")[0] + ".flac"
    # Insert Local Audio File Path
    clip.audio.write_audiofile(audio_filename, codec="flac")

# subs = [((0.0, 3.5), "here's a map of ancient Egypt"), ((4.4, 11.7), " I've inserted two sticks or obelisks one up here and Alexandria and one down here in Seguin")]
def create_subtitles(gcp_words_list):
    # FORMAT: subs = [((start, end), 'sentence'), ((start, end), 'sentence')]
    subs = []
    time_type = type(gcp_words_list[0]["alternatives"][0]["words"][0]["start_time"])
    for index, result in enumerate(gcp_words_list):
        alternative = result["alternatives"][0]
        transcript = alternative["transcript"]
        start = alternative["words"][0]["start_time"].total_seconds() if time_type == timedelta else alternative["words"][0]["start_time"]
        end = alternative["words"][-1]["end_time"].total_seconds() if time_type == timedelta else alternative["words"][-1]["end_time"]
        subs.append(((start, end), transcript))
    return subs

def get_time_from_word_object(word_obj):
    seconds = 0 if word_obj.seconds == None else word_obj.seconds
    nanos = 0 if word_obj['nanos'] == None else word_obj['nanos'] / 10**(-9)
    return seconds + nanos

def add_subs_to_video(subs, filename, transcript):
    video = editor.VideoFileClip('media/documents/{}'.format(filename))
    annotated_clips = [annotate(video.subclip(from_t, to_t), txt, transcript) for (from_t, to_t), txt in subs]
    video = editor.concatenate_videoclips(annotated_clips)
    video.write_videofile('media/documents/{}'.format(replace_last(filename, '.', '-subbed.')), temp_audiofile='temp-audio.m4a', remove_temp=True, codec="libx264", audio_codec="aac")

def annotate(video, text, transcript):
    """ Writes a text at the bottom of the clip. """
    # create text
    textclip = editor.TextClip(text, fontsize=transcript.text_size, font=transcript.font, color=transcript.text_color)
    while textclip.w > video.w:
        lines = math.ceil(textclip.w / video.w)
        split = text.split(' ')
        for i in range(1, lines):
            index = round(len(split) / lines) * i
            split[index] += '\n'
        text = ' '.join(split)
        textclip = editor.TextClip(text, fontsize=transcript.text_size, font=transcript.font, color=transcript.text_color)
    # create background
    bg_color = transcript.background_color.replace('#', '')
    bg_color_rgb = tuple(int(bg_color[i:i+2], 16) for i in (0, 2, 4))
    textclip = textclip.on_color(size=(textclip.w, textclip.h), color=bg_color_rgb, pos=('center', 'bottom'), col_opacity=transcript.background_opacity)
    # define animation
    # text_mov = textclip.set_pos( lambda t: (max(w/30,int(w-0.5*w*t)),max(5*h/6,int(100*t))) )
    textclip = textclip.set_pos(('center', 'bottom'))
    # add to video
    cvc = editor.CompositeVideoClip([video, textclip])
    return cvc.set_duration(video.duration)

def replace_in_transcript(gcp_words_list, alternatives):
    for index, result in enumerate(gcp_words_list["results"]):
        if result["alternatives"][0]["transcript"] != alternatives[index]:
            gcp_words_list['results'][index]["alternatives"][0]["transcript"] = alternatives[index]
            words_list = alternatives[index].split(" ")
            for word_index, word in enumerate(result["alternatives"][0]["words"]):
                if word["word"] != words_list[word_index]:
                    gcp_words_list['results'][index]["alternatives"][0]["words"][word_index] = words_list[word_index]
    return gcp_words_list

def extract_frame(path, time):
    clip = editor.VideoFileClip(path)
    name = path.split('/')[-1].split('.')[0]
    imgdir = '/'.join(path.split('/')[:-1])
    imgdir = replace_last(imgdir, '/media/', '/static/')
    imgdir = replace_last(imgdir, '/vidsmaker/', '/vidsmaker/auto_subtitles/')
    if not os.path.exists(imgdir):
        os.makedirs(imgdir)
    imgpath = op.join(imgdir, '{}.jpg'.format(name))
    clip.save_frame(imgpath, time)
    user = path.split('/')[-2]
    return '/static/documents/{}/{}.jpg'.format(user, name)