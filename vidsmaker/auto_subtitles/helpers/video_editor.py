from moviepy import editor
from moviepy.config import change_settings
import os.path as op
import os
import math
from datetime import timedelta
import re

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

def add_subs_to_video(subs, filename, transcript, x, y):
    video = editor.VideoFileClip('media/documents/{}'.format(filename))
    annotated_clips = [annotate(video.subclip(from_t, to_t), txt, transcript, x, y) for (from_t, to_t), txt in subs]
    video = editor.concatenate_videoclips(annotated_clips)
    video.write_videofile('media/documents/{}'.format(replace_last(filename, '.', '-subbed.')), temp_audiofile='temp-audio.m4a', remove_temp=True, codec="libx264", audio_codec="aac")

def annotate(video, text, transcript, x, y):
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
    textclip = textclip.on_color(size=(textclip.w, textclip.h), color=bg_color_rgb, pos=(0,0), col_opacity=transcript.background_opacity)
    # define animation
    # text_mov = textclip.set_pos( lambda t: (max(w/30,int(w-0.5*w*t)),max(5*h/6,int(100*t))) )
    if re.match(r"^([0-9\.]+)$", x):
        x = float(x) 
    elif (x not in ["center", "left", 'right']):
        x = "center"
    
    if re.match(r"^([0-9\.]+)$", y):
        y = float(y) 
    elif (y not in ["top", "center", 'bottom']):
        y = "bottom"
    textclip = textclip.set_position((x,y))
    # add to video
    cvc = editor.CompositeVideoClip([video, textclip])
    return cvc.set_duration(video.duration)

def replace_in_transcript(gcp_words_list, alternatives):
    for index, result in enumerate(gcp_words_list["results"]):
        if result["alternatives"][0]["transcript"] != alternatives[index]["transcript"]:
            gcp_words_list['results'][index]["alternatives"][0]["transcript"] = alternatives[index]["transcript"]
            words_list = alternatives[index]["transcript"].split(" ")
            for word_index, word in enumerate(result["alternatives"][0]["words"]):
                if word["word"] != words_list[word_index]:
                    gcp_words_list['results'][index]["alternatives"][0]["words"][word_index] = words_list[word_index]
        if result["alternatives"][0]["words"][0]["start_time"] != alternatives[index]["start_time"]:
            result["alternatives"][0]["words"][0]["start_time"] = alternatives[index]["start_time"]
        last_index = len(result["alternatives"][0]["words"]) - 1
        if result["alternatives"][0]["words"][last_index]["end_time"] != alternatives[index]["end_time"]:
            result["alternatives"][0]["words"][last_index]["end_time"] = alternatives[index]["end_time"]
    return gcp_words_list

def get_static_preview(path):
    path_without_file = '/'.join(path.split('/')[:-1])
    video = editor.VideoFileClip(path)
    path = replace_last(path, '/media/', '/static/')
    path = replace_last(path, '/vidsmaker/', '/vidsmaker/auto_subtitles/')
    if not os.path.exists(path):
        os.makedirs(path_without_file)
    video.write_videofile(path, temp_audiofile='temp-audio.m4a', remove_temp=True, codec="libx264", audio_codec="aac")
    user = path.split('/')[-2]
    name = path.split('/')[-1]
    return '/static/documents/{}/{}'.format(user, name)

def get_static_path(path):
    path = replace_last(path, '.', '-subbed.')
    path = replace_last(path, '/media/', '/static/')
    path = replace_last(path, '/vidsmaker/', '/vidsmaker/auto_subtitles/')
    user = path.split('/')[-2]
    name = path.split('/')[-1]
    return {'relative_path': '/static/documents/{}/{}'.format(user, name), 'full_path': path }

def get_duration(path):
    clip = editor.VideoFileClip(path)
    return clip.duration

def create_translated_subs(translation, transcripts):
    translations = replace_unicodes(translation).split('//')
    result = []
    for index, transcript in enumerate(transcripts):
        result.append({
            "text": translations[index],
            "start_time": transcript["alternatives"][0]["words"][0]['start_time'],
            "end_time": transcript["alternatives"][0]["words"][-1]['end_time']
        })
    return result

def replace_unicodes(text):
    matches = re.findall(r'&#([0-9]+);', text)
    matches = set(matches)
    for match in matches:
        text = text.replace('&#{};'.format(match), chr(int(match)))
    return text