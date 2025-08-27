import socket


class Client:
    def __init__(self, ip="127.0.0.1", port=9000, bandwidth=1024):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Info
        self.dest = (ip, port)
        self.bandwidth = bandwidth

    def Start(self):
        self.Runtime()

    def Runtime(self):
        print("Client connected & Ready for transfer!")
        while True:
            option = input("(msg, name, wait): ")

            if option == "wait":
                self.Send("wait")
            elif option == "msg":
                self.Send(input("Msg: "))


    def Send(self, data="DEBUG"):
        self.socket.sendto(f"{data}".encode(), self.dest)

    def Recv(self):
        data, address = self.socket.recvfrom(self.bandwidth)
        return (data, address)
