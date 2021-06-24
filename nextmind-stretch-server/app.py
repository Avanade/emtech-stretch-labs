import os

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

PATH_TO_COMMANDS = "/home/hello-robot/Chatbot"
COMMAND_DICT = {"opengrip": {"command": "moveGrip", "operation": "open"}}


async def run_command(request):

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


async def close_grip(request):  # scan:ignore
    move_amount = request.path_params["amount"]
    run_command("moveGrip", "close", move_amount)
    return JSONResponse({"close": str(move_amount)})


async def arm_out(request):  # scan:ignore
    move_amount = request.path_params["amount"]
    run_command("movearm", "out", move_amount)
    return JSONResponse({"out": str(move_amount)})


async def arm_in(request):  # scan:ignore
    move_amount = request.path_params["amount"]
    run_command("movearm", "in", move_amount)
    return JSONResponse({"in": str(move_amount)})


async def arm_up(request):  # scan:ignore
    move_amount = request.path_params["amount"]
    run_command("movearm", "up", move_amount)
    return JSONResponse({"up": str(move_amount)})


async def arm_down(request):  # scan:ignore
    move_amount = request.path_params["amount"]
    run_command("movearm", "down", move_amount)
    return JSONResponse({"down": str(move_amount)})


async def move_forward(request):  # scan:ignore
    move_amount = request.path_params["amount"]
    run_command("moveFB", "forward", move_amount)
    return JSONResponse({"forward": str(move_amount)})


async def move_back(request):  # scan:ignore
    move_amount = request.path_params["amount"]
    run_command("moveFB", "backwards", move_amount)
    return JSONResponse({"back": str(move_amount)})


async def move_left(request):  # scan:ignore
    move_amount = request.path_params["amount"]
    run_command("moveLR", "left", move_amount)
    return JSONResponse({"left": str(move_amount)})


async def move_right(request):  # scan:ignore
    move_amount = request.path_params["amount"]
    run_command("moveLR", "right", move_amount)
    return JSONResponse({"right": str(move_amount)})


app = Starlette(
    debug=True,
    routes=[
        Route("/opengrip/{amount}", run_command, methods=["POST"]),
        Route("/closegrip/{amount}", close_grip, methods=["POST"]),
        Route("/armout/{amount}", arm_out, methods=["POST"]),
        Route("/armin/{amount}", arm_in, methods=["POST"]),
        Route("/armup/{amount}", arm_up, methods=["POST"]),
        Route("/armdown/{amount}", arm_down, methods=["POST"]),
        Route("/forward/{amount}", move_forward, methods=["POST"]),
        Route("/backwards/{amount}", move_back, methods=["POST"]),
        Route("/left/{amount}", move_left, methods=["POST"]),
        Route("/right/{amount}", move_right, methods=["POST"]),
    ],
)
