import socket

# My Modules
from Helpers import Recv, Send, WaitForACK

def Server(dest, bandwidth_limits = (10, 1024, 2048)):
    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"Starting server on {dest}")
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
            print("[Server]: Shutdown")
            conn.close()
            quit()
        elif flag == "reply":
            msg = input("(msg): ")
            conn.sendto(msg.encode(), address)
            print("Waiting for ACK...")
            WaitForACK(conn)
        else:
            print("[Client]: Waiting...")
        # Always send end ACK.
        conn.sendto("ACK".encode(), address)

if __name__ == "__main__":
    dest = ("0.0.0.0", 9000)
    Server(dest)