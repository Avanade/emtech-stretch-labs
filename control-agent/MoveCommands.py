import grpc
import teletubby_pb2
import teletubby_pb2_grpc


def turnLeft():
    channel = grpc.insecure_channel("api2.rocos.io:443")
    destination = "/ros/cmd_vel"  # check left turn command

    stub = teletubby_pb2_grpc.GreeterStub(channel)
    response = stub.SendTelemetry(teletubby_pb2.SendTelemetry(context=destination))
    print("Greeter client received: " + response.message)


turnLeft()