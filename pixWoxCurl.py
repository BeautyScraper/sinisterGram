# from sinSpider import sinSpider as telf
import re
import pycurl_requests as requests
from scrapy.http import HtmlResponse
import random
from urllib.request import urljoin
import os
from pathlib import Path

delay = False
path = "D:\\paradise\\stuff\\sinisterBabes"
vpath = r'D:\paradise\stuff\SinToWatch'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Alt-Used': 'www.pixwox.com',
    'Connection': 'keep-alive',
    'Referer': 'http://www.pixwox.com/',
    'Upgrade-Insecure-Requests': '1',
    }

def start_requests():
    with open("instaLinks.opml", "r+") as instalink:
        # time.sleep(60)
        urls = instalink.readlines()


    random.shuffle(urls)
    for url in urls:
        try:
            rl = url.split("/")[3]
        except:
            continue
        # url = "https://www.instastalker2.com/user/%s" % rl
        url = "https://www.pixwox.com/id/profile/%s/" % rl
        print("currently opening the url =" + url)
        
        resp = requests.get(url.rstrip("\n"),headers=headers)
        response = HtmlResponse(url=url.rstrip("\n"), body=resp.text, encoding='utf-8')  
        profileStalker(response)
            
def profileStalker(response):
    print("Starting profile stalking %s" % response.url)
    postLinks = response.css('a[href*=post]::attr(href)').extract()
    
    # import pdb;pdb.set_trace()
    postIds = [re.sub('\/#\d+','',x).strip('/').split("/")[-1] for x in postLinks]
    profileId = response.url.strip("/").split("/")[-1]
    profileId = profileId.rstrip('\n')
    print(response.url,' total posts found on this page ',len(postLinks))
    if delay:
        t.time.sleep(random.randint(0,60))
    completedPicIds = getCompletedId(profileId)
    for links,post in zip(postLinks,postIds):
        if post not in completedPicIds:
            # import pdb;pdb.set_trace()
            meta = {'pid':profileId,'postId':post}
            url = urljoin(response.url, links)
            resp = requests.get(url.rstrip("\n"),headers=headers)
            response = HtmlResponse(url=url, body=resp.text, encoding='utf-8')  
            PostStalker(response,profileId,post)
            completedPicIds = post + "\n" + completedPicIds
    setCompletedId(profileId, completedPicIds)

def setCompletedId( profileId, completedPicIds):
    ensure_dir("Completed\\")
    with open("Completed\\" + profileId + ".ccode", "w") as completed:
        completed.write(completedPicIds)
    def removeLine( filename, id):
        with open(filename, "r") as inF:
            t = inF.readlines()
            j = [x for x in t if id not in x]
            if (len(j) < len(t) - 4):
                print("this is the culprit " + id)
            # print(j)
        with open(filename, "w") as inF:
            inF.writelines(j)

def getCompletedId( profileId):
    
    ensure_dir("Completed\\")
    ensureFile("Completed\\" + profileId + ".ccode")
    print("opening " + profileId + ".ccode for checking")
    with open("Completed\\" + profileId + ".ccode", "r") as completed:
        return completed.read()

def ensureFile( filename):
    if not Path(filename).is_file():
        Path(filename).touch()

def properName( name):
    name = name.replace("amp", "")
    return re.sub('[^\(\)A-Za-z0-9\-\.\\\ ]+', "", name)

def ensure_dir( file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

        
def PostStalker(response,profileId,postId):
    imgLinks = [x for x in response.css('.downbtn::attr(href)').extract() if '.mp4' not in x]
    VideoLinks = [x for x in response.css('.downbtn::attr(href)').extract() if '.mp4' in x]
    # imgLinks = response.css(".media-img::attr(src)").extract() if len(imgLinks) <= 0 else imgLinks
    # profileId = response.meta['pid']
    # postId = response.meta['postId']
    if len(postId) < 4:
        import pdb;pdb.set_trace()
    fileNames = ["%s(%s).jpg" % (profileId,postId+str(i).replace("0","")) for i,_ in enumerate(imgLinks)]
    VfileNames = ["%s(%s).mp4" % (profileId,postId+str(i).replace("0","")) for i,_ in enumerate(VideoLinks)]
    # import pdb;pdb.set_trace()
    BatchDownloader(response,imgLinks,fileNames)
    BatchDownloader(response,VideoLinks,VfileNames,vpath)

def BatchDownloader(response,imgLinks,FileNames,path="D:\\paradise\\stuff\\sinisterBabes"):
    for iUrl, FileName in zip(imgLinks,FileNames):
        # import pdb;pdb.set_trace()
        downloadThisWithIDM(iUrl, FileName , path)

        
def downloadThisWithIDM(videoUrl, filename, videoPath):
    filename = properName(filename)
    print("videos"+filename[:3])
    if True:
        cmd = r"C:\Program Files (x86)\Internet Download Manager\IDMan.exe"
        wholeCommand = 'start "" "%s" /d "%s" /p "%s" /f \"%s\" /n /a' % (cmd, videoUrl, videoPath, filename)
        print(wholeCommand)
        os.system(wholeCommand)
        # self.downloadCompleteRegister("videos"+filename[:3], filename)

start_requests()
