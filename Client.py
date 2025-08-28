import threading
import socket

class Client:
    def __init__(self,  dest, bandwidth = 1024):
        self.dest = dest
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Info
        self.bandwidth = bandwidth

    def Start(self):
        # Starting Server
        print(f"Connecting Client to {self.dest}")

        while True:
            # Get Flag
            print("Msg, Connect, Pass")
            flag = input("Option: ").lower()
            self.Send(flag, self.dest)

            # Process Client Request (Based on Flag.)
            if flag == "msg":
                msg = input("(Message): ")
                self.Send(msg, self.dest)
            elif flag == "connect":
                # Get Client Name, and address add them to the connected clients list.
                info = input("Name: ")
                client_info = self.Send(info, self.dest)
            elif flag == "pass":
                print("Msg")
                option = input("Option: ")
                self.Send(option, self.dest)                                            # Send 2nd Flag
                
                if option == "msg":                                                      # Client wants to send a message to another client.
                    client_info = input("Client Name: ")                                # Get "to" info. (Client Name)
                    self.Send(client_info, self.dest, WaitACK=True)                     # Send "to" info to server, and wait for a ACK.
                    msg = input("(Message): ")
                    self.Send(msg, self.dest)
            elif flag == "scan":
                clients = self.Recv()[0].decode()
                print(f"Current Clients: {clients}")

            # Always send end ACK.
            self.WaitForACK()


    # Helpers 

    def Send(self, data, address, WaitACK=False):
        self.socket.sendto(f"{data}".encode(), address)
        # Get ACK Flag (If True)
        if WaitACK:
            if self.WaitForACK():
                return True
            else:
                return False

    def Recv(self, SendACK=False):
        data, address = self.socket.recvfrom(self.bandwidth)
        if SendACK:
            self.socket.sendto("ACK".encode(), address)
        return (data, address)
    
    def WaitForACK(self):
        data, address = self.socket.recvfrom(self.bandwidth)
        if data.decode() == "ACK":
            return True
        elif data.decode() == "ERR":
            print("[Server]: Request ERROR")
            return False
        else:
            print("[ERROR] Failed NET SYNC!")
            return False
        

client = Client(("45.79.207.244", 9001))
client.Start()