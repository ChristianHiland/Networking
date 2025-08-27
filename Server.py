import socket

# My Modules
from Helpers import Recv, Send, WaitForACK

info = {
    "Client": {
        "Clients": [],  # Clients: [("127.0.0.1", 9000)]
    },
    "Server": {
        "Source": ("0.0.0.0", 9000)
    }
}


class Server:
    def __init__(self,  dest, bandwidth_limits = (10, 1024, 2028)):
        self.dest = dest
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Info
        self.current_clients = []
        self.bandwidth_limits = bandwidth_limits

    def Server(self):
        # Starting Server
        print(f"Starting server on {dest}")
        self.socket.bind(self.dest)

        while True:
            # Get Flag
            flag, address = Recv(self.socket)
            flag = flag.decode()

            # Process Client Request (Based on Flag.)
            if flag == "client":
                flag2, address = Recv(self.socket)
                flag2 = flag2.decode()

                if flag2 == "scan":
                    # Send List of Client
                    Send(self.socket, self.current_clients, address, False)


            
            # Always send end ACK.
            self.socket.sendto("ACK".encode(), address)

if __name__ == "__main__":
    dest = ("0.0.0.0", 9000)
    Server(dest)