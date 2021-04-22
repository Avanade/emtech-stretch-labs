import azure.cognitiveservices.speech as speechsdk
import os
import json

import speech


def getSpeechKeys():
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )

    with open(os.path.join(__location__, "config.json")) as json_file:
        data = json.load(json_file)
        key = data["speechKey"]
        region = data["speechLocation"]

    return key, region


def getLuisKeys():
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )

    with open(os.path.join(__location__, "config.json")) as json_file:
        data = json.load(json_file)
        key = data["LuisKey"]
        region = data["LuisRegion"]
        appid = data["LuisAppId"]

    return key, region, appid


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


run = True

while run == True:

    intent = recognize_intent()
    speech.speak(intent.text)

    if intent.intent_id == "Vision":
        speech.speak("I'm looking")
        result = speech.recognize(
            "https://robots.ieee.org/robots/stretch/stretch-1200x630.jpg"
        )

        speech.speak("I can see" + str(result["description"]["captions"][0]["text"]))
