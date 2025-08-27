from os import system
import socket
import sys


dest = ("127.0.0.1", 9000)
bandwidth_limits = (10, 1024, 2048)
debug = False

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

def SendChuck(connection, address, data):
    # Start sending size, max bandwidth, recive max Server bandwidth, Start sending at max server bandwidth.
    size = sys.getsizeof(data)
    max_bandwidth = bandwidth_limits[2]
    connection.sendto(f"{size}".encode(), address)
    connection.sendto(f"{max_bandwidth}".encode(), address)
    max_server_bandwidth = Recv(connection)[0].decode()
    connection.sendto(f"{data}".encode(), address)



def Recv(connection):
    data, address = connection.recvfrom(1024)
    return (data, address)

def Client():
    # Connecting to Server
    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Reply allow the server to reply.")
    WaitClear = True
    while True:
        option = input("(msg, set, quit, reply, clear): ")

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