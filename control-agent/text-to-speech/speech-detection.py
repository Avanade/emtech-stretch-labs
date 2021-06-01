import azure.cognitiveservices.speech as speechsdk
import os
import json
import requests
from datetime import datetime

import speech
import realsense


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

speech.speak("starting up")

while run == True:

    intent = recognize_intent()
    try:
        if intent.intent_id == "Vision":
            speech.speak("I'm looking")

            image = realsense.take_photo()

            result = speech.recognize(image)

            if "person" in result:
                # TODO more than one person?
                person = speech.recognize_face(image)[0]["faceId"]
                speech.speak(
                    "I can see"
                    + str(result["description"]["captions"][0]["text"]).replace(
                        "a person", str(person)
                    )
                )

            else:
                speech.speak(
                    "I can see" + str(result["description"]["captions"][0]["text"])
                )

        elif intent.intent_id == "Move":

            intentJson = json.loads(intent.intent_json)
            try:
                direction = intentJson["entities"][0]["entity"]
                speech.speak("I'm going to move " + str(direction))
                if direction == "forward":
                    os.system(
                        "python /home/hello-robot/Chatbot/moveFB.py 'forward' 0.3"
                    )
                elif direction == "back":
                    os.system(
                        "python /home/hello-robot/Chatbot/moveFB.py 'backwards' 0.3"
                    )
                elif direction == "left":
                    os.system("python /home/hello-robot/Chatbot/moveLR.py 'left' 0.3")
                elif direction == "right":
                    os.system("python /home/hello-robot/Chatbot/moveLR.py 'right' 0.3")

            except:
                speech.speak("I don't know what direction to move")

        elif intent.intent_id == "Weather.QueryWeather":
            speech.speak("I don't have the capacity for thermoregulation")
        elif intent.intent_id == "Time":

            now = datetime.now()
            speakabletime = now.strftime("%H:%M")
            speech.speak("The time is, " + speakabletime)

        elif intent.intent_id == "Stop":
            break
        elif intent.intent_id == "Selfie":
            speech.speak("Smile. 3, 2, 1.")
            image = realsense.take_photo()
            speech.speak("click")
            speech.uploadBlob(image)
            speech.speak("I've saved that to Azure for you")

        elif intent.intent_id == "Arm":
            up_down = ""
            in_out = ""

            intentJson = json.loads(intent.intent_json)

            if "'up'" in str(intentJson):
                up_down = "up"
            elif "'down'" in str(intentJson):
                up_down = "down"
            if "'in'" in str(intentJson):
                in_out = "in"
            elif "'out'" in str(intentJson):
                in_out = "out"

            os.system(
                "python /home/hello-robot/Chatbot/movearm.py '"
                + up_down
                + "' 1 '"
                + in_out
                + "' 1"
            )

        elif intent.intent_id == "Grip":
            intentJson = json.loads(intent.intent_json)
            if "'open'" in str(intentJson):
                os.system("python /home/hello-robot/Chatbot/moveGrip.py 'open' 100")
            elif "'close'" in str(intentJson):
                os.system("python /home/hello-robot/Chatbot/moveGrip.py 'close' 20")
            else:
                speech.speak("open or close it?")

        elif intent.intent_id == "Calibrate":
            speech.speak("calibrating, stand back")
            os.system("stretch_robot_home.py")
            speech.speak("calibration complete, I can now use my limbs")

    except:
        if intent != "No good match found in KB.":
            speech.speak(intent)
        else:
            speech.speak("I'm not sure I understood that")
