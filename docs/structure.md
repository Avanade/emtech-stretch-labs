# Folder Structure

- docs - documentation
- docs/mermaid - process flows and state diagrams, and the .mmd files used to generate them
- docs/diagrams-as-code - technical architecture images and the python code used to generate them
- .vscode - configuration and recommendations for the VS Code IDE
- cloud-app - the cloud app which runs in Azure, connecting to either the IoT hub or Rocos
- nextmind-robot-telepresence - the unity application which embeds the NextMind SDK
- stretch-python-agent - the python agent which supports IoT hub deployment
- infra - the folder containing infrastructure as code requirements for the repository

# Python Requirements
It's recommended to use a conda environment when installing requirements, e.g. `conda create --name stretchlabs python=3.9 -y`

- requirements.txt -  will install all requirements
- requirements-dev.txt - will install requirements for developer tooling
- requirements-docs.txt - will install requirements used to generate diagrams for documentation
- requirements-infra.txt - will install requirements used for cloud infrastructure
- requirements-cloud-app.txt - will install requirements for the cloud application in Azure
- requirements-python-agent.txt - will install requirements for users runnning a Python agent on Stretch rather than Rocos


# Unity Requirements
You will require a unity licence. Read the [documentation from NextMind](https://www.next-mind.com/documentation/unity-sdk/tutorials/01-setting-up-environment/) for more information on setting up the SDK.