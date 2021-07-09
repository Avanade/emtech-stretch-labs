import json
import os
from datetime import datetime, timedelta
import http.client, urllib.request, urllib.parse, urllib.error
from dotenv import load_dotenv

import asyncio


from azure.cognitiveservices.speech import (
    AudioDataStream,
    SpeechConfig,
    SpeechSynthesizer,
    SpeechSynthesisOutputFormat,
)
from azure.cognitiveservices.speech.audio import AudioOutputConfig

from azure.storage.blob import (
    BlobClient,
    BlobServiceClient,
    generate_blob_sas,
    BlobSasPermissions,
    ResourceTypes,
    AccountSasPermissions,
)

PERSON_GROUP_ID = "53cdefb1-c211-4215-a944-6b64128fa39f"
FACE_IDS = {"f9611b03-dc30-48bd-88f5-9ce251f688b6": "Fergus"}


def get_speech_keys():
    """Retrieve Keys for Azure Speech"""
    load_dotenv()

    key = os.getenv("SPEECH_KEY")
    region = os.getenv("SPEECH_LOCATION")

    return key, region


def get_vision_keys():
    """Retrieve Keys for Azure Vision"""
    load_dotenv()

    key = os.getenv("VISION_KEY")
    url = os.getenv("VISION_URL")

    return key, url


def get_face_keys():
    """Retrieve Keys for Azure Vision - Face"""
    load_dotenv()

    key = os.getenv("FACE_KEY")
    url = os.getenv("FACE_URL")

    return key, url


def get_blob_keys():
    """Retrieve Keys for Azure Blob Storage"""
    load_dotenv()

    conn = os.getenv("BLOB_CONN_STRING")
    container = os.getenv("BLOB_CONTAINER_NAME")
    name = os.getenv("BLOB_STORE_NAME")
    key = os.getenv("BLOB_STORE_KEY")

    return conn, container, name, key


def get_qna_keys():
    """Retrieve Keys for Azure QnA Maker"""
    load_dotenv()

    url = os.getenv("QNA_URL")
    key = os.getenv("QNA_KEY")

    return url, key


def get_luis_keys():
    """Retrieve Keys for LUIS app"""

    load_dotenv()

    key = os.getenv("LUIS_KEY")
    region = os.getenv("LUIS_REGION")
    app_id = os.getenv("LUIS_APP_ID")

    return key, region, app_id


def blob_sas(blob_name):
    """Retrieve a SAS url for a secified blob name
    Keyword arguments:
    blobName -- the name of the blob in the storage account
    """
    conn, container, name, key = get_blob_keys()

    sas_token = generate_blob_sas(
        account_name=name,
        account_key=key,
        blob_name=blob_name,
        container_name=container,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1),
    )

    url = (
        "https://"
        + name
        + ".blob.core.windows.net/"
        + container
        + "/"
        + blob_name
        + "?"
        + sas_token
    )

    return url


@asyncio.coroutine
async def speak_async(text):
    """async calling of speach"""
    speak(text)


def speak(text):
    """Read out input text on the local system playback device
    Keyword arguments:
    text -- a string of text to be read
    """
    key, region = get_speech_keys()
    speech_config = SpeechConfig(subscription=key, region=region)
    speech_config.speech_synthesis_voice_name = "en-GB-RyanNeural"
    audio_config = AudioOutputConfig(use_default_speaker=True)
    synthesizer = SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )
    synthesizer.speak_text_async(text)


@asyncio.coroutine
async def recognize(blobData):
    """Use Azure computer vision recognize from an image as bytes
    Keyword arguments:
    blobData -- bytes data of an image
    """

    key, url = get_vision_keys()

    headers = {
        # Request headers
        "Content-Type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": key,
    }

    params = urllib.parse.urlencode(
        {
            # Request parameters
            "visualFeatures": "Description",
            "language": "en",
        }
    )

    body = blobData

    try:
        conn = http.client.HTTPSConnection(url)
        conn.request("POST", "/vision/v3.1/analyze?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("Vision Error: ", e)
        return "error"

    return json.loads(data)


def recognize_face(blob_data):
    """Use Azure computer vision recognize identified faces from an image as bytes
    Keyword arguments:
    blobData -- bytes data of an image
    """

    key, url = get_face_keys()

    headers = {
        # Request headers
        "Content-Type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": key,
    }

    request_params = urllib.parse.urlencode(
        {
            "detectionModel": "detection_03",
            "returnFaceId": "true",
            "returnFaceLandmarks": "false",
        }
    )

    body = blob_data

    try:
        conn = http.client.HTTPSConnection(url)
        conn.request("POST", "/face/v1.0/detect?%s" % request_params, body, headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("Vision Error: ", e)
        return "error"

    people = []
    for face in json.loads(data):
        people.append(identify_face(face["faceId"]))

    return people


def identify_face(face_id):

    key, url = get_face_keys()

    headers = {
        # Request headers`
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": key,
    }

    params = urllib.parse.urlencode(
        {
            # Request parameters
            "detectionModel": "detection_03",
            "returnFaceId": "true",
            "returnFaceLandmarks": "false",
        }
    )

    body = {
        "PersonGroupId": PERSON_GROUP_ID,
        "faceIds": [str(face_id)],
        "maxNumOfCandidatesReturned": 1,
        "confidenceThreshold": 0.5,
    }

    try:
        conn = http.client.HTTPSConnection(url)
        conn.request("POST", "/face/v1.0/identify?%s" % params, str(body), headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("Vision Error: ", e)
        return "error"

    # face logic
    results = json.loads(data)
    try:
        return FACE_IDS[results[0]["candidates"][0]["personId"]]
    except KeyError:
        return "a stranger"


def upload_blob(blob_bytes):
    """upload a blob to the Azure storage account named as a timestamp
    Keyword arguments:
    blobBytes -- bytes data of a file to uplaod
    """
    blob_name = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    conn, container, name, key = get_blob_keys()
    blob = BlobClient.from_connection_string(
        conn_str=conn,
        container_name=container,
        blob_name=blob_name,
    )

    blob.upload_blob(blob_bytes)
