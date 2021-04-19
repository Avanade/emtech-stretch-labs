# Rocos Setup

Main Rocos documentation is found [on the Rocos Website](https://docs.rocos.io/docs/grpc-telemetry-message-service), including the GRPC protocol we're using.

prerequesites:

1. You must have set up an account and created a project in the Rocos portal
2. The robot must be connected to the internet at the time you install the agent
3. The agent is installed on the command line, so you need a terminal open to your robot or to have a keyboard and monitor plugged into it directly.
4. On Linux operating systems, you'll need to have enough rights to run commands with sudo

More infomration on robot profiles [here](https://docs.rocos.io/prod/docs/robot-definitions)

## Rocos on Stretch

First kill any other instance of pyhon if not already done:

```
pkill -9 python
```

To initiate a complete Rocos connection on stretch, the following three need to be running on the stretch:

1. Rocos agent. Install Details [here](https://docs.rocos.io/prod/docs/ubuntu) first time,

then, once installed, run:

```
    sudo rocos-agent -d
```

2. In a seperate termnial, run the pre-installed roscore using:
   ```
   roscore
   ```
3. Run any stretch python script, for example the funmap demo using:
   ```
   roslaunch stretch_funmap mapping.launch
   ```

## Rocos Portal

By this point you should have set up and connected your robot. With the three services above running, navigate to the Rocos dashboard. Under 'Realsence' camera press connect to start the video stream.

Use the buttons to enter navigation mode, and move around

If a gamepad is setup on the controller pane, you can use it by entering operation mode, selecting the robot, amnd clicking 'enable gamepad'

### Live data viewer

The live data viewer can be used to access the raw data delemetry of the robot. It can aso be used to call commands on the robot individually.

### Commands

Commands can be added on the 'command' pane to add Rocos functionality, like moving the robot or changing modes. These can then be used by controllers or buttons at a later date.

### Storage Streams

Storage streams are used to save telemetry as it comes through. Streams can be added so telemetry can be saved, and viewed in the storage explorer pane at a later date.
