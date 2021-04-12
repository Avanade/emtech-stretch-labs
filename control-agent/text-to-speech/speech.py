from azure.cognitiveservices.speech import (
    AudioDataStream,
    SpeechConfig,
    SpeechSynthesizer,
    SpeechSynthesisOutputFormat,
)
from azure.cognitiveservices.speech.audio import AudioOutputConfig

import http.client, urllib.request, urllib.parse, urllib.error, base64

import json
import os


def getSpeechKeys():
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )

    with open(os.path.join(__location__, "config.json")) as json_file:
        data = json.load(json_file)
        key = data["speechKey"]
        region = data["speechLocation"]

    return key, region


def getVisionKeys():
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )

    with open(os.path.join(__location__, "config.json")) as json_file:
        data = json.load(json_file)
        key = data["visionKey"]
        url = data["visionUrl"]

    return key, url


def speak(text):
    key, region = getSpeechKeys()
    # speech_config = SpeechConfig(subscription=key, region=region)
    speech_config = SpeechConfig(
        subscription="06eb9311f8c94b088627778387860715", region="uksouth"
    )
    speech_config.speech_synthesis_voice_name = "en-GB-RyanNeural"
    audio_config = AudioOutputConfig(use_default_speaker=True)
    synthesizer = SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )
    synthesizer.speak_text_async(text)


def recognize(imgUrl):

    key, url = getVisionKeys()

    headers = {
        # Request headers
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": key,
    }

    params = urllib.parse.urlencode(
        {
            # Request parameters
            "visualFeatures": "Description",
            "language": "en",
        }
    )

    body = '{"url": "' + imgUrl + '"}'

    try:
        conn = http.client.HTTPSConnection(url)
        conn.request("POST", "/vision/v3.1/analyze?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("Vision Error: ", e)

    return json.loads(data)


result = recognize("https://robots.ieee.org/robots/stretch/stretch-1200x630.jpg")

speak("I can see" + str(result["description"]["captions"][0]["text"]))
