import grpc, drone_pb2_grpc
from drone_pb2 import Request, Response
import time

class PingClient():
    def __init__(self, host='0.0.0.0', port=3000):
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = drone_pb2_grpc.PingPongStub(self.channel)

    def retrieveID(self, data):
        req = Request(data=str(data))
        return self.stub.retrieveID(req)

    def retrievePosition(self, data):
        req = Request(data=str(data))
        return self.stub.retrievePosition(req)

def validate():
    client = PingClient()
    resp = client.retrieveID("ping")
    print("Client id [{}] connected to the server.".format((resp.data)))
    return int(resp.data)

def fetchPosition(my_id):
    client = PingClient()
    resp = client.retrievePosition(my_id)
    return resp.data

if __name__ == '__main__':
    my_id = validate()
    oldPosition = "foo"
    while True:
        time.sleep(1)
        newPosition = fetchPosition(my_id)
        if oldPosition != newPosition:
            print("[received] moving to [{}]".format((newPosition)))
            oldPosition = newPosition
            