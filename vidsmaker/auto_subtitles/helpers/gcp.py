from google.cloud import storage
from google.cloud import speech
# import speech_recognition as sr
from os import path
import pickle

class CloudStorage:

    def __init__(self):
        self.client = storage.Client()
        self.bucket_name = "vidsmaker_bucker"
    
    def upload_blob(self, source_file_name, destination_blob_name):
        """Uploads a file to the bucket."""
        storage_client = storage.Client()
        bucket = storage_client.bucket(self.bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
    
    def download_blob(self, source_blob_name, destination_file_name):
        """Downloads a blob from the bucket."""
        print(destination_file_name)
        storage_client = storage.Client()
        bucket = storage_client.bucket(self.bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)



class SpeechToText:

    def __init__(self, language):
        self.client = speech.SpeechClient()
        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
            language_code=language,
            audio_channel_count=2,
            enable_word_time_offsets=True,
        )
    
    def speech_to_text(self, filename):
        audio = speech.RecognitionAudio(uri="gs://vidsmaker_bucker/{}".format(filename))
        operation = self.client.long_running_recognize(config=self.config, audio=audio)
        response = operation.result(timeout=90)
        return response.results
    
    def text_object_to_dict(self, results):
        result_dict = {"results": []}
        for result in results:
            alternative = result.alternatives[0]
            obj = {
                "alternatives": [{
                    "transcript": alternative.transcript,
                    "confidence": alternative.confidence,
                    "words": [{"word": word.word, "start_time": word.start_time.total_seconds(), "end_time": word.end_time.total_seconds()} for word in alternative.words]
                }]
            }
            result_dict['results'].append(obj)
        return result_dict

# test_dict = {
#     "results": [
#       {
#         "alternatives": [
#           {
#             "transcript": "okay so what am I doing here...(etc)...",
#             "confidence": 0.96596134,
#             "words": [
#               {
#                 "start_time": "1.400s",
#                 "end_time": "1.800s",
#                 "word": "okay"
#               },
#               {
#                 "start_time": "1.800s",
#                 "end_time": "2.300s",
#                 "word": "so"
#               },
#               {
#                 "start_time": "2.300s",
#                 "end_time": "2.400s",
#                 "word": "what"
#               },
#               {
#                 "start_time": "2.400s",
#                 "end_time": "2.600s",
#                 "word": "am"
#               },
#               {
#                 "start_time": "2.600s",
#                 "end_time": "2.600s",
#                 "word": "I"
#               },
#               {
#                 "start_time": "2.600s",
#                 "end_time": "2.700s",
#                 "word": "doing"
#               },
#               {
#                 "start_time": "2.700s",
#                 "end_time": "3s",
#                 "word": "here"
#               },
#               {
#                 "start_time": "3s",
#                 "end_time": "3.300s",
#                 "word": "why"
#               },
#               {
#                 "start_time": "3.300s",
#                 "end_time": "3.400s",
#                 "word": "am"
#               },
#               {
#                 "start_time": "3.400s",
#                 "end_time": "3.500s",
#                 "word": "I"
#               },
#               {
#                 "start_time": "3.500s",
#                 "end_time": "3.500s",
#                 "word": "here"
#               },
#             ]
#           }
#         ]
#       },
#       {
#         "alternatives": [
#           {
#             "transcript": "okay so what am I doing here...(etc)...",
#             "confidence": 0.96596134,
#             "words": [
#               {
#                 "start_time": "1.400s",
#                 "end_time": "1.800s",
#                 "word": "okay"
#               },
#               {
#                 "start_time": "1.800s",
#                 "end_time": "2.300s",
#                 "word": "so"
#               },
#               {
#                 "start_time": "2.300s",
#                 "end_time": "2.400s",
#                 "word": "what"
#               },
#               {
#                 "start_time": "2.400s",
#                 "end_time": "2.600s",
#                 "word": "am"
#               },
#               {
#                 "start_time": "2.600s",
#                 "end_time": "2.600s",
#                 "word": "I"
#               },
#               {
#                 "start_time": "2.600s",
#                 "end_time": "2.700s",
#                 "word": "doing"
#               },
#               {
#                 "start_time": "2.700s",
#                 "end_time": "3s",
#                 "word": "here"
#               },
#               {
#                 "start_time": "3s",
#                 "end_time": "3.300s",
#                 "word": "why"
#               },
#               {
#                 "start_time": "3.300s",
#                 "end_time": "3.400s",
#                 "word": "am"
#               },
#               {
#                 "start_time": "3.400s",
#                 "end_time": "3.500s",
#                 "word": "I"
#               },
#               {
#                 "start_time": "3.500s",
#                 "end_time": "3.500s",
#                 "word": "here"
#               },
#             ]
#           }
#         ]
#       }
#     ]
# }