import socket

class Network:
    def __init__(self, ip="127.0.0.1", port=9000, initType="client", bandwidth=1024):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.currentAddress = (0, 0)
        
        # Info
        self.dest = (ip, port)
        self.initType = initType
        self.bandwidth = bandwidth

    def Start(self):
        # Check if we're the client or server.
        if self.initType == "server":
            print(f"Starting Server at {self.dest}")
            try:
                # Bind The Socket to Dest.
                self.socket.bind(self.dest)
                # Listen for input.
                print("Waiting for incoming...")
                while True:
                    self.StandbyIncoming()
            except socket.error as e:
                print(f"[Server]: ERROR!\n{e}")

        elif self.initType == "client":
            print(f"Connecting to Server at {self.dest}")


    def StandbyIncoming(self):
        flag = self.Recv().decode()
        
        if flag == "none":
                print("wait")

        if self.initType == "server":    
            if flag == "msg":
                # Handle Incoming Message.
                msg = self.Recv().decode()
                print(f"[Client]: {msg}")
            elif flag == "name":
                # Handle Changing names.
                self.ChangeNames()
            else:
                print(f"Unknown flag: {flag}")
        elif self.initType == "client":
            pass



    # Send From Socket to Target
    def Send(self, data = "DEBUG"):
        if self.initType == "server":
            self.socket.sendto(f"{data}".encode(), self.dest)
        elif self.initType == "client":
            self.socket.sendto(f"{data}".encode(), self.dest)

    # Recvive Data from socket.
    def Recv(self):
        data, address = self.socket.recvfrom(self.bandwidth)
        if self.currentAddress == (0, 0):
            self.currentAddress = address
        return data