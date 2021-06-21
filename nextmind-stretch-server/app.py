
import os

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route


async def homepage(request):
    return JSONResponse({'hello': 'world'})

async def open_grip(request):
    move_amount = request.path_params["amount"]
    os.system("python /home/hello-robot/Chatbot/moveGrip.py 'open' "+ str(move_amount))
    return JSONResponse({'open': str(move_amount)})

async def close_grip(request):
    move_amount = request.path_params["amount"]
    os.system("python /home/hello-robot/Chatbot/moveGrip.py 'close' "+ str(move_amount))
    return JSONResponse({'close': str(move_amount)})

async def arm_out(request):
    move_amount = request.path_params["amount"]
    os.system("python /home/hello-robot/Chatbot/movearm.py up 0 'out' "+ str(move_amount))
    return JSONResponse({'out': str(move_amount)})

async def arm_in(request):
    move_amount = request.path_params["amount"]
    os.system("python /home/hello-robot/Chatbot/movearm.py up 0 'in' "+ str(move_amount))
    return JSONResponse({'in': str(move_amount)})

async def arm_up(request):
    move_amount = request.path_params["amount"]
    os.system("python /home/hello-robot/Chatbot/movearm.py 'up' " + str(move_amount) + " 'in' 0")
    return JSONResponse({'up': str(move_amount)})

async def arm_down(request):
    move_amount = request.path_params["amount"]
    os.system("python /home/hello-robot/Chatbot/movearm.py 'down' " + str(move_amount) + " 'in' 0")
    return JSONResponse({'down': str(move_amount)})

app = Starlette(debug=True, routes=[
    Route('/', homepage),
    Route('/opengrip/{amount}',open_grip,methods=["POST"]),
    Route('/closegrip/{amount}',close_grip,methods=["POST"]),
    Route('/armout/{amount}',arm_out,methods=["POST"]),
    Route('/armin/{amount}',arm_in,methods=["POST"]),
    Route('/armup/{amount}',arm_up,methods=["POST"]),
    Route('/armdown/{amount}',arm_down,methods=["POST"]),



])
