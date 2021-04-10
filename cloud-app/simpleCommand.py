import grpc


def run():
    channel = grpc.insecure_channel("api2.rocos.io:443")
    print(channel)


run()

