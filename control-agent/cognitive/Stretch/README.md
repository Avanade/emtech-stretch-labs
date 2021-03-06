# Stretch Speech Augmentation - inbuilt object detection model

This package adds Azure speech capability to the stretch robot using python3 and Azure speech services.

## Stretch Files

This file replaces the hello robot version found [here](https://github.com/hello-robot/stretch_ros/blob/master/stretch_deep_perception/nodes/object_detector_python3.py)

## Use

To use, simply replace the file on the stretch at the following location on the stretch's file system:

```
/home/hello-robot/catkin_ws/src/stretch_ros/stretch_deep_perception/nodes
```

Once the file has been replaced run

```
roslaunch stretch_deep_perception stretch_detect_objects.launch
```

as normal.

## Expected behaviour

The expected behaviour is to drive the robot head manually using the terminal input as described in the console. As the detector system recognises objects, the objects will be printed in the terminal window. The additional functionality is that the robot will now announce what objects it can see by stating 'I can see a [object]' using the Azure text to speech service. Internet access is required.

## Speech Detection

Azure Speech detection is used to run speech to text for use in commands, or on-board chatbots. To use, the unique device Id of a microphone is needed. This can be found [here](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/how-to-select-audio-input-devices)

For Linux devices like the stretch robot, additional installation prerequisties are required. details of these can be found [here](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/quickstarts/setup-platform?tabs=dotnet%2Cmacos%2Cjre%2Cbrowser&pivots=programming-language-python)

`N.B. Visual studio may not ask for the correct microphone permissions, and no result will be returned`

The default microphone should be selected automatically. If no result is seen, try running the script from a terminal instance, and granting permission.

You can also start visual studio code with:

```
sudo /Applications/Visual\ Studio\ Code.app/Contents/MacOS/Electron
```

until the bug is corrected in VS Code.

# LUIS Integration

The following are the required intents for current code functionality:

| Intent                         | Entities                      | Example                          | Current Action                                  |
| ------------------------------ | ----------------------------- | -------------------------------- | ----------------------------------------------- |
| Move                           | Forwards,Backwards,Left,Right | "Move Forwards"                  | Dictates intent to move (currently no movement) |
| Vision                         | N/A                           | "What can you see?"              | Call the vision service and dictate the caption |
| (prebuilt)Weather.QueryWeather | N/A                           | "What's the weather like today?" | Simple retort                                   |
| Stop                           | N/A                           | "STOP!"                          | Exit code and stop running                      |
| Time                           | N/A                           | "What time is it?"               | Dictates the current system time                |

# QnA integration

Any QnA structure can be used, and customisations can be added. The default 'witty' QnA additions are recomended to quickly exapand the KB with simple answers to common questions
