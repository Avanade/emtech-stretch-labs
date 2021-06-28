import azure.cognitiveservices.speech as speechsdk
import os
import json
from azure.cognitiveservices.speech.speech_py_impl import IntentTrigger
import requests
from datetime import datetime

import speech

# import realsense

LUIS_CONFIDENCE_LIMIT = 0.7
PATH_TO_COMMANDS = "/home/hello-robot/Chatbot"
COMMAND_DICT = {
    "opengrip": {"command": "moveGrip", "operation": "open"},
    "closegrip": {"command": "moveGrip", "operation": "close"},
    "armout": {"command": "moveArmIO", "operation": "out"},
    "armup": {"command": "moveArmUD", "operation": "up"},
    "armdown": {"command": "moveArmUD", "operation": "down"},
    "armin": {"command": "moveArmIO", "operation": "in"},
    "forward": {"command": "moveFB", "operation": "forward"},
    "backwards": {"command": "moveFB", "operation": "backwards"},
    "left": {"command": "moveLR", "operation": "left"},
    "right": {"command": "moveLR", "operation": "right"},
}


def __location__():
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    return __location__


def get_speech_keys():

    with open(os.path.join(__location__(), "config.json")) as json_file:
        data = json.load(json_file)
        key = data["speechKey"]
        region = data["speechLocation"]

    return key, region


def get_luis_keys():

    with open(os.path.join(__location__(), "config.json")) as json_file:
        data = json.load(json_file)
        key = data["LuisKey"]
        region = data["LuisRegion"]
        appid = data["LuisAppId"]

    return key, region, appid


def get_qna_keys():

    with open(os.path.join(__location__(), "config.json")) as json_file:
        data = json.load(json_file)
        url = data["qnaURL"]
        key = data["qnaKey"]

    return url, key


def from_mic():
    """Currently Unused function to call a single system microphone utterance to text"""
    key, region = get_speech_keys()

    speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("Speak into your microphone.")
    result = speech_recognizer.recognize_once_async().get()
    print(result.text)

    return result.text


def recognize_intent():
    """System microphone to LUIS and QnA maker, returns either a
    confident intent, or a QnA answer"""
    key, region, appid = get_luis_keys()

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
    if intentJson["topScoringIntent"]["score"] < LUIS_CONFIDENCE_LIMIT:
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
    """Take a question string and return an answer string from QnA maker"""
    url, key = get_qna_keys()
    url = url

    payload = '{"question":"' + question + '"}'
    headers = {
        "Authorization": key,
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text


async def run_command(instruction, move_amount):
    """convert a simple instruction and move ammount to a movement on stretch using
    the python 2 scripts - this will be upgraded to python 3 when available"""

    command = COMMAND_DICT[str(instruction)]["command"]
    operation = COMMAND_DICT[str(instruction)]["operation"]

    os.system(
        "python "
        + PATH_TO_COMMANDS
        + "/"
        + command
        + ".py '"
        + str(operation)
        + "' "
        + str(move_amount)
    )

    return {command: str(move_amount)}


def get_amount(intent_json):
    """search for builin number entity in an intent json
    return either the number, or 'default' to indicate a defualt value
    should be selected"""
    for entity in intent_json["entities"]:
        if entity["type"] == "builtin.number":
            amount = str(entity["resolution"]["value"])
    try:
        return amount
    except:
        return "default"


def move_intent(intent):
    """Intent response to move the stretch FBLR"""
    intent_json = json.loads(intent.intent_json)

    for entity in intent_json["entities"]:
        print(entity)
        if entity["type"] == "Direction":
            print("direction found")
            direction = str(entity["entity"])

    # set ammount if specificed
    amount = get_amount(intent_json)
    if amount == "default":
        amount = 0.5

    try:
        speech.speak("I'm going to move " + str(direction) + str(amount))
        if direction == "forward":
            run_command("forward", amount)
        elif direction == "back":
            run_command("backwards", amount)
        elif direction == "left":
            run_command("left", amount)
        elif direction == "right":
            run_command("right", amount)

    except:
        speech.speak("I don't know what direction to move")


def weather_intent():
    """This intent functinality is not yet implemented"""
    speech.speak("I don't have the capacity for thermoregulation")


def time_intent():
    """Intent response speaks the current system time"""
    now = datetime.now()
    speakabletime = now.strftime("%H:%M")
    speech.speak("The time is, " + speakabletime)


def calibrate_intent():
    """Intent response calls the stretch calibration script"""
    speech.speak("calibrating, stand back")
    os.system("stretch_robot_home.py")
    speech.speak("calibration complete, I can now use my limbs")


def selfie_intent():
    """Intent response takes a photo on realsense and uplaod
    to azure blob"""
    speech.speak("Smile. 3, 2, 1.")
    image = realsense.take_photo()
    speech.speak("click")
    speech.uploadBlob(image)
    speech.speak("I've saved that to Azure for you, check it out in my blob storage")


def grip_intent(intent):
    """Intent response to open or close stretch grip"""
    intent_json = json.loads(intent.intent_json)

    amount = get_amount(intent_json)
    if amount == "default":
        amount = 20

    if "'open'" in str(intent_json):
        run_command("opengrip", amount)
    elif "'close'" in str(intent_json):
        run_command("closegrip", amount)
    else:
        speech.speak("open or close it?")


def arm_intent(intent):
    """Intent response to move arm UDIO"""
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


def wrist_intent(intent):
    """Intent response to move the stretch wrist"""
    intentJson = json.loads(intent.intent_json)

    try:
        for entity in intentJson["entities"]:
            if entity["type"] == "builtin.number":
                amount = str(entity["resolution"]["value"])

        os.system("python /home/hello-robot/Chatbot/moveWrist.py " + str(amount))

    except:
        speech.speak("Move it where?")


def vision_intent():
    """Intent response to take a picture and analyse the contents
    using Azure computer vision services"""
    speech.speak("I'm looking")

    image = realsense.take_photo()

    result = speech.recognize(image)

    if (
        "person"
        or "boy"
        or "man"
        or "woman" in result["description"]["captions"][0]["text"]
    ):
        # TODO more than one person?
        try:
            person = speech.identify_face(speech.recognize_face(image)[0]["faceId"])
        except:
            person = "someone I don't recognise"

        speech.speak(
            "I can see"
            + str(result["description"]["captions"][0]["text"])
            .replace("a person", str(person))
            .replace("a man", str(person))
            .replace("a boy", str(person))
        )

    else:
        speech.speak("I can see" + str(result["description"]["captions"][0]["text"]))


def intent_handler(intent):
    """Handles the intent responces and calls the associated fucntions"""

    if isinstance(intent, str):
        if intent != "No good match found in KB.":
            speech.speak(intent)
            return
        else:
            speech.speak("I'm not sure I understood that")
            return

    if intent.intent_id == "Vision":
        vision_intent()
    elif intent.intent_id == "Move":
        move_intent(intent)
    elif intent.intent_id == "Weather.QueryWeather":
        weather_intent()
    elif intent.intent_id == "Time":
        time_intent()
    elif intent.intent_id == "Calibrate":
        calibrate_intent()
    elif intent.intent_id == "Stop":
        return False
    elif intent.intent_id == "Selfie":
        selfie_intent()
    elif intent.intent_id == "Grip":
        grip_intent(intent)
    elif intent.intent_id == "Arm":
        arm_intent(intent)
    elif intent.intent_id == "Wrist":
        wrist_intent()

    return True


# Continuous loop starts here
run = True
# warm up confirmation
speech.speak("starting up")

while run == True:

    intent = recognize_intent()

    run = intent_handler(intent)
