import requests
import os
url = "https://www.pixwox.com/id/profile/_imyour_joy"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Alt-Used': 'www.pixwox.com',
    'Connection': 'keep-alive',
    'Referer': 'http://www.pixwox.com/',
    'Upgrade-Insecure-Requests': '1',
}


# response = requests.get(url,headers=headers,allow_redirects=True, verify=True,proxies=None)
response = requests.get(url,headers=headers,cert=None)

with open('tgc.htm','w') as tg:
    tg.write(str(response.text))
os.system('curlTest.bat')