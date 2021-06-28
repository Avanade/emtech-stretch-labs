import os

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

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


async def run_command(request):# scan:ignore

    move_amount = request.path_params["amount"]

    path = str(request.url.path).split("/")[1]

    command = COMMAND_DICT[str(path)]["command"]
    operation = COMMAND_DICT[str(path)]["operation"]

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

    return JSONResponse({path: str(move_amount)})


app = Starlette(
    debug=True,
    routes=[
        Route("/opengrip/{amount}", run_command, methods=["POST"]),
        Route("/closegrip/{amount}", run_command, methods=["POST"]),
        Route("/armout/{amount}", run_command, methods=["POST"]),
        Route("/armin/{amount}", run_command, methods=["POST"]),
        Route("/armup/{amount}", run_command, methods=["POST"]),
        Route("/armdown/{amount}", run_command, methods=["POST"]),
        Route("/forward/{amount}", run_command, methods=["POST"]),
        Route("/backwards/{amount}", run_command, methods=["POST"]),
        Route("/left/{amount}", run_command, methods=["POST"]),
        Route("/right/{amount}", run_command, methods=["POST"]),
    ],
)
