import threading
import socket


print("Script Ran")

class Server(threading.Thread):
    def __init__(self,  dest, bandwidth = 1024):
        self.dest = dest
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Info
        self.current_clients = []
        self.bandwidth = bandwidth

    def Start(self):
        # Starting Server
        print(f"Starting server on {dest}")
        self.socket.bind(self.dest)

        while True:
            # Get Flag
            flag, address = self.Recv()
            flag = flag.decode()

            # Process Client Request (Based on Flag.)
            if flag == "msg":
                msg = self.Recv()[0].decode()
                print(f"[Client]: {msg}")
            elif flag == "connect":
                # Get Client Name, and address add them to the connected clients list.
                client_info = self.Recv()
                info = (client_info[0], client_info[1])
                self.current_clients.append(info)
            elif flag == "pass":
                data = self.Recv()                                                      # Get 2nd Flag
                flag2 = data[0].decode()
                
                if flag2 == "msg":                                                      # Client wants to send a message to another client.
                    client_info = self.Recv()                                           # Get "to" info. (Client Name)
                    for currently_connected in self.current_clients:
                        if currently_connected[0] == client_info[0].decode():
                            self.socket.sendto("ACK".encode(), address)                 # Send ACK to sender.
                            msg = self.Recv()[0]                                        # Get Sender's Message
                            self.Send(msg, currently_connected[1], WaitACK=True)        # Send & Wait For ACK.
                        else:
                            self.socket.sendto("ERR".encode(), address)                 # Error Occred.
                            print(f"[Client Error]: Client: {client_info} not found.")



            # Always send end ACK.
            self.socket.sendto("ACK".encode(), address)



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
            self.SendACK(address, flag="ACK")
        return (data, address)

    def SendACK(self, address, flag = "ACK"):
        self.socket.sendto(flag.encode(), address)    
        if flag == "ERR":
            print("[Server]: Error")

    
    def WaitForACK(self):
        data, address = self.socket.recvfrom(self.bandwidth)
        if data.decode() == "ACK":
            return True
        elif data.decode() == "ERR":
            print("[ERROR] Failed NET SYNC!")
            return False
        else:
            return False


dest = ("0.0.0.0", 9001)
server = Server(dest)
server.Start()