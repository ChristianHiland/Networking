from os import system
import struct
import socket
import sys

dest = ("127.0.0.1", 9000)
bandwidth_limits = (10, 1024, 2048)
server_limits = (10, 1024, 2048)
debug = True

def WaitForACK(connection):
    data, address = connection.recvfrom(1024)
    if data.decode() == "ACK":
        if debug:
            print(f"NET SYNCED!")
        return True
    else:
        if debug:
            print(f"FAILED NET SYNC!")
        return False
def SendChuck(connection, address, data = [], format="single"):
    # Getting Info For Local...
    size = 0
    if format == "single":
       size = sys.getsizeof(data)
    elif format == "list":
        size = len(data)
    max_bandwidth = bandwidth_limits[2]

    # Sending info & data.
    connection.sendto(format.encode(), address)                 # Send Format
    connection.sendto(f"{size}".encode(), address)              # Send Size
    connection.sendto(f"{max_bandwidth}".encode(), address)     # Send Max Bandwidth
    max_server_bandwidth = Recv(connection)[0].decode()         # Get Server's Max Bandwidth
    if format == "list":
        for hex_item in data:
            connection.sendto(f"{hex_item}".encode('utf-8'), address)                # Send Data
            WaitForACK(connection)                              # Wait for ACK.
    elif format == "single":
        connection.sendto(f"{data}".encode(), address)          # Send Data
    connection.sendto("DONE".encode(), address)
def GetChuck(connection, address):
    bandwidth = 1024
    format = Recv(connection)[0].decode()                       # Get Format
    size = int(Recv(connection)[0].decode())                    # Get Size (Becomes len in list format).
    max_bandwidth = int(Recv(connection)[0].decode())           # Get Client's Max Bandwidth
    connection.sendto(f"{server_limits[2]}".encode(), address)  # Send Server's Max Bandwidth
    
    # Set Bandwidth
    if server_limits[2] <= max_bandwidth:
        bandwidth = server_limits[2]
    else:
        bandwidth = max_bandwidth

    data = []
    if format == "list":
        data_list = []
        for i in range(0, size):
            result = Recv(connection)
            data_list.append(result[0].decode())                # Get Data.
            connection.sendto("ACK".encode(), result[1])        # Send ACK.
    elif format == "single": 
        data = Recv(connection)                                 # Get Data
    return (size, bandwidth, data)
def ListToHex(data):
    hexData = []
    count = 0
    try:
        print("Check, Make sure there's at least 3!")
    except:
        print("Unsafe!, Make Sure to keep your chucks at a size of 3, 6, 9, 12, etc.")
    while True:
        count += 1
        if count >= len(data) - 1:
            break
        hexData.append(data[count][0])       
    return hexData
def Recv(connection, bandwidth=1024):
    data, address = connection.recvfrom(bandwidth)
    return (data, address)

def Client():
    # Connecting to Server
    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Reply allow the server to reply.")
    WaitClear = True
    while True:
        option = input("(msg, set, quit, reply, clear, chuck): ")

        if option == "msg":
            msg = input("(msg): ")
            conn.sendto("msg".encode(), dest)
            conn.sendto(msg.encode(), dest)
        elif option == "set":
            print("Commands: name")
            command = input("(CMD): ")
            conn.sendto(command.encode(), dest)
            if command == "name":
                print("targets: server, client (you)")
                target = input("(target): ")
                name = input("Name: ")
                conn.sendto(target.encode(), dest)
                conn.sendto(name.encode(), dest)
                print("\n[Client]: Set Name!")
        elif option == "quit":
            conn.sendto("exit".encode(), dest)
            conn.close()
            quit()
        elif option == "reply":
            conn.sendto("reply".encode(), dest)
            print("Waiting for Server...")
            msg = Recv(conn)[0]
            print(f"[Server]: {msg}")
            conn.sendto("ACK".encode(), dest)
            WaitClear = False
        elif option == "clear":
            WaitClear = True
        elif option == "chuck":
            print("[INFO]: !BETA FEATURE!")
            print("Formats: Binary, Hex, Text, File")
            option = input("Format: ")
            if option == "text":
                count = 0
                # Get Lines
                lines = []
                while True:
                    line = input(f"{count}: ")
                    count += 1
                    if line.lower() == "end":
                        break
                    lines.append((count, line))
                # Convert to Hex
                hexList = ListToHex(lines)
                SendChuck(conn, dest, hexList, format="list")

        # End ACK
        WaitForACK(conn)
        if WaitClear:
            system("clear")
            system("cls")
def Server():
    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    conn.bind(dest)

    while True:
        # Waiting for flag
        flag, address = Recv(conn)
        flag = flag.decode()
        print(f"flag: {flag}")

        if flag == "none":
            print("[Client]: Waiting...")
        elif flag == "msg":
            msg = Recv(conn)[0].decode()
            print(f"[Client]: {msg}")
        elif flag == "set":
            # Get Next command.
            command = Recv(conn)[0].decode()
            print(command)
            if command == "name":
                print("[ACTION]: Setting Name")
                # Change what?
                who = Recv(conn)[0].decode()
                if who == "client":
                    name = Recv(conn)[0].decode()
                    print(f"[Client]: Name Changed to: {name}")
                elif who == "server":
                    name = Recv(conn)[0].decode()
                    print(f"[Server]: Name Changed to: {name}")
        elif flag == "exit":
            print("[Client]: Disconnect Request")
            print("[Server]: Shutdown")
            conn.close()
            quit()
        elif flag == "reply":
            msg = input("(msg): ")
            conn.sendto(msg.encode(), address)
            print("Waiting for ACK...")
            WaitForACK(conn)
        elif flag == "chuck":
            chuck_data = GetChuck(conn, address)
            data = Recv(conn)
            if data[0].decode() == "DONE":
                print(f"[Client]: Got Chuck Data: {chuck_data[0]}")
            else:
                while True:
                    data = Recv(conn)
                    if data[0].decode() == "DONE":
                        break
                    else:
                        print(f"[Client]: Chuck Missing Data: {Recv(conn)[0].decode()}")
        conn.sendto("ACK".encode(), address)

if __name__ == "__main__":
    args = sys.argv

    print("If Program fails due to port and host being used. Please change port numbers by adding 1")

    # Checking args
    if len(args) > 3:
            if len(args) > 4:
                dest = (args[3], args[2])
            else:
                dest = ("127.0.0.1", args[2])

    if args[1] == "client":
        Client()
    elif args[1] == "server":
        Server()