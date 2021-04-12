import grpc
import teletubby_pb2.py
import teletubby_pb2_grpc.py


def turnLeft():
    channel = grpc.insecure_channel("api2.rocos.io:443")
    print(channel)


turnLeft()