import socket


def Recv(connection, buffer=1024):
    data, address = connection.recvfrom(buffer)
    return (data, address)

def Send(connection, data, address, buffer=1024):
    connection.sendto(f"{data}".encode(), address)
    # Get ACK Flag
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