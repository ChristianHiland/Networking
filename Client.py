import socket

class Client:
    def __init__(self, dest, bandwidth):
        self.dest = dest
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Info
        self.current_clients = []
        self.bandwidth = bandwidth

    def Start(self):
        