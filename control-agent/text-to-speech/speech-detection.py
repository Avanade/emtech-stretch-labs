import azure.cognitiveservices.speech as speechsdk
import os
import json
import requests

import speech


def __location__():
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    return __location__


def getSpeechKeys():

    with open(os.path.join(__location__(), "config.json")) as json_file:
        data = json.load(json_file)
        key = data["speechKey"]
        region = data["speechLocation"]

    return key, region


def getLuisKeys():

    with open(os.path.join(__location__(), "config.json")) as json_file:
        data = json.load(json_file)
        key = data["LuisKey"]
        region = data["LuisRegion"]
        appid = data["LuisAppId"]

    return key, region, appid


def getQnAKeys():

    with open(os.path.join(__location__(), "config.json")) as json_file:
        data = json.load(json_file)
        url = data["qnaURL"]
        key = data["qnaKey"]

    return url, key


def from_mic():
    key, region = getSpeechKeys()

    speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("Speak into your microphone.")
    result = speech_recognizer.recognize_once_async().get()
    print(result.text)

    return result.text


def recognize_intent():

    key, region, appid = getLuisKeys()

    intent_config = speechsdk.SpeechConfig(
        subscription=key,
        region=region,
    )
    intent_recognizer = speechsdk.intent.IntentRecognizer(speech_config=intent_config)

    model = speechsdk.intent.LanguageUnderstandingModel(app_id=appid)
    intent_recognizer.add_all_intents(model)

    intent_result = intent_recognizer.recognize_once()

    # Check the results
    try:
        intentJson = json.loads(intent_result.intent_json)
    except:
        return ""
    print(intentJson)
    # if low score, do QnA
    if intentJson["topScoringIntent"]["score"] < 0.9:
        qna = json.loads(QnA(intent_result.text))
        return qna["answers"][0]["answer"]

    if intent_result.reason == speechsdk.ResultReason.RecognizedIntent:
        print(
            'Recognized: "{}" with intent id `{}`'.format(
                intent_result.text, intent_result.intent_id
            )
        )
    elif intent_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(intent_result.text))
    elif intent_result.reason == speechsdk.ResultReason.NoMatch:
        print(
            "No speech could be recognized: {}".format(intent_result.no_match_details)
        )
    elif intent_result.reason == speechsdk.ResultReason.Canceled:
        print(
            "Intent recognition canceled: {}".format(
                intent_result.cancellation_details.reason
            )
        )
        if (
            intent_result.cancellation_details.reason
            == speechsdk.CancellationReason.Error
        ):
            print(
                "Error details: {}".format(
                    intent_result.cancellation_details.error_details
                )
            )
    return intent_result


def QnA(question):

    url, key = getQnAKeys()
    url = url

    payload = '{"question":"' + question + '"}'
    headers = {
        "Authorization": key,
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text


run = True

while run == True:

    intent = recognize_intent()
    try:
        if intent.intent_id == "Vision":
            speech.speak("I'm looking")
            result = speech.recognize(
                "https://robots.ieee.org/robots/stretch/stretch-1200x630.jpg"
            )

            speech.speak(
                "I can see" + str(result["description"]["captions"][0]["text"])
            )

        elif intent.intent_id == "Move":

            intentJson = json.loads(intent.intent_json)
            try:
                direction = intentJson["entities"][0]["entity"]
                speech.speak("I'm going to move " + str(direction))
            except:
                speech.speak("I don't know what direction to move")

        elif intent.intent_id == "Weather.QueryWeather":
            speech.speak("I don't have the capacity for thermoregulation")

    except:
        if intent != "No good match found in KB.":
            speech.speak(intent)