from azure.cognitiveservices.speech import (
    AudioDataStream,
    SpeechConfig,
    SpeechSynthesizer,
    SpeechSynthesisOutputFormat,
)
from azure.cognitiveservices.speech.audio import AudioOutputConfig

from datetime import datetime, timedelta
import requests
from azure.storage.blob import (
    BlobClient,
    BlobServiceClient,
    generate_blob_sas,
    BlobSasPermissions,
    ResourceTypes,
    AccountSasPermissions,
)

import http.client, urllib.request, urllib.parse, urllib.error, base64

import json
import os


def getSpeechKeys():
    """Retrieve Keys for Azure Speech"""
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )

    with open(os.path.join(__location__, "config.json")) as json_file:
        data = json.load(json_file)
        key = data["speechKey"]
        region = data["speechLocation"]

    return key, region


def getVisionKeys():
    """Retrieve Keys for Azure Vision"""
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )

    with open(os.path.join(__location__, "config.json")) as json_file:
        data = json.load(json_file)
        key = data["visionKey"]
        url = data["visionUrl"]

    return key, url


def getFaceKeys():
    """Retrieve Keys for Azure Vision - Face"""
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )

    with open(os.path.join(__location__, "config.json")) as json_file:
        data = json.load(json_file)
        key = data["FaceKey"]
        url = data["FaceUrl"]

    return key, url


def getBlobKeys():
    """Retrieve Keys for Azure Blob Storage"""
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )

    with open(os.path.join(__location__, "config.json")) as json_file:
        data = json.load(json_file)
        conn = data["blobConnection"]
        container = data["blobContainer"]
        name = data["blobstore"]
        key = data["blobKey"]

    return conn, container, name, key


def blobSas(blobName):
    """Retrieve a SAS url for a secified blob name
    Keyword arguments:
    blobName -- the name of the blob in the storage account
    """
    conn, container, name, key = getBlobKeys()

    sas_token = generate_blob_sas(
        account_name=name,
        account_key=key,
        blob_name=blobName,
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
        + blobName
        + "?"
        + sas_token
    )

    return url


def speak(text):
    """Read out input text on the local system playback device
    Keyword arguments:
    text -- a string of text to be read
    """
    key, region = getSpeechKeys()
    speech_config = SpeechConfig(subscription=key, region=region)
    speech_config.speech_synthesis_voice_name = "en-GB-RyanNeural"
    audio_config = AudioOutputConfig(use_default_speaker=True)
    synthesizer = SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )
    synthesizer.speak_text_async(text)


def recognize(blobData):
    """Use Azure computer vision recognize from an image as bytes
    Keyword arguments:
    blobData -- bytes data of an image
    """

    key, url = getVisionKeys()

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


def recognize_face(blobData):
    """Use Azure computer vision recognize from an image as bytes
    Keyword arguments:
    blobData -- bytes data of an image
    """

    key, url = getFaceKeys()

    headers = {
        # Request headers
        "Content-Type": "application/octet-stream",
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

    body = blobData

    try:
        conn = http.client.HTTPSConnection(url)
        conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("Vision Error: ", e)
        return "error"

    return json.loads(data)


def identify_face(face_id):

    key, url = getFaceKeys()

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
        "PersonGroupId": "53cdefb1-c211-4215-a944-6b64128fa39f",
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
    # TODO remove hard coding
    results = json.loads(data)
    if (
        results[0]["candidates"][0]["personId"]
        == "f9611b03-dc30-48bd-88f5-9ce251f688b6"
    ):
        return "Fergus"

    return "a stranger"


def uploadBlob(blobBytes):
    """upload a blob to the Azure storage account named as a timestamp
    Keyword arguments:
    blobBytes -- bytes data of a file to uplaod
    """
    name = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    conn, container, name, key = getBlobKeys()
    blob = BlobClient.from_connection_string(
        conn_str=conn,
        container_name=container,
        blob_name=name,
    )

    blob.upload_blob(blobBytes)
