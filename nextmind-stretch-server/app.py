import os

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

path_to_commands = "/home/hello-robot/Chatbot"


async def open_grip(request):  # scan:ignore
    move_amount = request.path_params["amount"]
    os.system("python " + path_to_commands + "/moveGrip.py 'open' " + str(move_amount))
    return JSONResponse({"open": str(move_amount)})


async def close_grip(request):  # scan:ignore
    move_amount = request.path_params["amount"]
    os.system("python " + path_to_commands + "/moveGrip.py 'close' " + str(move_amount))
    return JSONResponse({"close": str(move_amount)})


async def arm_out(request):  # scan:ignore
    move_amount = request.path_params["amount"]
    os.system(
        "python " + path_to_commands + "/movearm.py 'up' 0 'out' " + str(move_amount)
    )
    return JSONResponse({"out": str(move_amount)})


async def arm_in(request):  # scan:ignore
    move_amount = request.path_params["amount"]
    os.system(
        "python " + path_to_commands + "/movearm.py 'up' 0 'in' " + str(move_amount)
    )
    return JSONResponse({"in": str(move_amount)})


async def arm_up(request):  # scan:ignore
    move_amount = request.path_params["amount"]
    os.system(
        "python "
        + path_to_commands
        + "/movearm.py 'up' "
        + str(move_amount)
        + " 'in' 0"
    )
    return JSONResponse({"up": str(move_amount)})


async def arm_down(request):  # scan:ignore
    move_amount = request.path_params["amount"]
    os.system(
        "python "
        + path_to_commands
        + "/movearm.py 'down' "
        + str(move_amount)
        + " 'in' 0"
    )
    return JSONResponse({"down": str(move_amount)})


async def move_forward(request):  # scan:ignore
    move_amount = request.path_params["amount"]
    os.system("python " + path_to_commands + "/moveFB.py 'forward' " + str(move_amount))
    return JSONResponse({"down": str(move_amount)})


async def move_back(request):  # scan:ignore
    move_amount = request.path_params["amount"]
    os.system(
        "python " + path_to_commands + "/moveFB.py 'backwards' " + str(move_amount)
    )
    return JSONResponse({"down": str(move_amount)})


async def move_left(request):  # scan:ignore
    move_amount = request.path_params["amount"]
    os.system("python " + path_to_commands + "/moveLR.py 'left' " + str(move_amount))
    return JSONResponse({"down": str(move_amount)})


async def move_right(request):  # scan:ignore
    move_amount = request.path_params["amount"]
    os.system("python " + path_to_commands + "/moveLR.py 'right' " + str(move_amount))
    return JSONResponse({"down": str(move_amount)})


app = Starlette(
    debug=True,
    routes=[
        Route("/", homepage),
        Route("/opengrip/{amount}", open_grip, methods=["POST"]),
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
