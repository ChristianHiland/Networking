import socket


def Recv(connection, buffer=1024, SendACK=True):
    data, address = connection.recvfrom(buffer)
    # Send ACK Flag (If True)
    if SendACK:
        connection.sendto("ACK".encode(), address)
    return (data, address)

def Send(connection, data, address, WaitACK=True):
    connection.sendto(f"{data}".encode(), address)
    # Get ACK Flag (If True)
    if WaitACK:
        if WaitForACK(connection):
            return True
        else:
            return False

def WaitForACK(connection):
    data = Recv(connection)
    if data[0].decode() == "ACK":
        return True
    else:
        print("[ERROR]: Failed NET SYNC!")
        return False
    

class Packet:
    def __init__(self, data, address):
        self.data = data
        self.address = address

    def Send(self, connection):
        # To send a packet, Send: Packet (Flag), Size, Data.
        connection.sendto()