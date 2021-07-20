import re
import scrapy
import urllib.request
import requests
import shutil
import time
import random
import sys
import os
from scrapy.crawler import CrawlerProcess
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class sinSpider(scrapy.Spider):
    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }

    def __init__(self):
        self.path = "D:\\paradise\\stuff\\sinisterBabes"
        self.videoPath = "D:\\paradise\\stuff\\sinisterVideos"

    def start_requests(self):
        with open("instaLinks.opml", "r+") as instalink:
            # time.sleep(60)
            urls = instalink.readlines()

        random.shuffle(urls)
        for url in urls:
            rl = url.split("/")[3]
            url = "https://profile-stalker.to/profile/%s" % rl
            print("currently opening the url =" + url)
            
            # yield scrapy.Request(url.rstrip("\n"), callback=self.parse,  cookies={"csrftoken":"Hs8MEf1oSXv4t2q8FtcOtqrdxqFtsLW1","ds_user_id":"3246264185","ig_did":"217B2DB9-A084-4B9E-9F04-948BA42645B6","mid":"XmzqZgALAAHUdojAunjvlnGCtfs3","rur":"VLL","sessionid":"3246264185:1Ow06LaBDCbLAi:9","shbid":"4720","shbts":"1584196241.7547708","urlgen":"\"{\\\"103.226.202.5\\\": 133283}:1jD7p4:Dym3Kv6FDjxauuyx0bQCNHrkwsY\""}, errback=self.on404, )
            yield scrapy.Request(url.rstrip("\n"), callback=self.profileStalker, errback=self.on404, )

    def on404(self, failure):
        print(failure.value.response.status)
        if failure.value.response.status == 429:
            print("time to sleep")
            time.sleep(60*45)
        if failure.check(HttpError) and failure.value.response.status == 404:
            print("found a dead url " + failure.request.url)
            filename = "elimination.opml"
            with open(filename, "a+") as inF:
                inF.write(failure.request.url + "\n")
            self.removeLine("instaLinks.opml", failure.request.url.split("/")[3] + "\n")
            self.removeLine("instaLinks.opml", failure.request.url.split("/")[3] + "/")
            # self.removeLine("instaLinks.opml", failure.request.url+"/"\)

    def removeLine(self, filename, id):
        with open(filename, "r") as inF:
            t = inF.readlines()
            j = [x for x in t if id not in x]
            if (len(j) < len(t) - 4):
                print("this is the culprit " + id)
            print(j)
        with open(filename, "w") as inF:
            inF.writelines(j)

    def getCompletedId(self, profileId):
        self.ensure_dir("Completed\\")
        self.ensureFile("Completed\\" + profileId + ".ccode")
        print("opening " + profileId + ".ccode for checking")
        with open("Completed\\" + profileId + ".ccode", "r") as completed:
            return completed.read()

    def ensureFile(self, filename):
        try:
            with open(filename, "r") as inf:
                return
        except Exception as e:
            with open(filename, "w") as inf:
                return

    def properName(self, name):
        name = name.replace("amp", "")
        return re.sub('[^\(\)A-Za-z0-9\-\.\\\ ]+', "", name)

    def ensure_dir(self, file_path):
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def downloadImgWithIDM(self, imgUrl, Path):
        filename = Path.split("\\")[-1]
        folder = "\\".join(Path.split("\\")[:-1])
        # print("DDDD"+folder)
        # time.sleep(10)
        folder = re.sub("[^\w\\\ \d-]","", folder)
        folder = re.sub("\s+"," ", folder)
        # print("YYYY"+folder)
        print(r"C:\GalImgs\%s" % folder)
        self.downloadThisVideo(10, r"C:\GalImgs\%s" % folder, filename, imgUrl)


    def downloadThisWithIDM(self, videoUrl, filename, videoPath):
        filename = self.properName(filename)
        print("videos"+filename[:3])
        if True:
            cmd = r"C:\Program Files (x86)\Internet Download Manager\IDMan.exe"
            wholeCommand = 'start "" "%s" /d "%s" /p "%s" /f \"%s\" /n /a' % (cmd, videoUrl, videoPath, filename)
            print(wholeCommand)
            os.system(wholeCommand)
            # self.downloadCompleteRegister("videos"+filename[:3], filename)

    def downloadImg(self, Url, fileName, path=""):
        fileName = self.properName(fileName)
        time.sleep(5)
        r = requests.get(Url, stream=True)
        if r.status_code == 200:
            i = 0
            self.ensure_dir("incomplete\\" + fileName)
            with open("incomplete\\" + fileName, 'wb') as pdf:
                for chunk in r.iter_content(chunk_size=1024 * 4):
                    # print(i)
                    # i = i + 1
                    # writing one chunk at a time to pdf file
                    if chunk:
                        pdf.write(chunk)
        try:
            self.ensure_dir(self.path)
            os.rename("incomplete\\" + fileName, path + fileName)
        except Exception as e:
            with open("logRenaming.txt", "a+") as inF:
                inF.write(str(e) + "\n")
                os.remove("incomplete\\" + fileName)

    def profilePost(self, response):
        print("Post Stalking is starting")
        imageurl = response.css("a.download-button::attr(href)").extract()[0]
        if ".mp4" in imageurl:
            return
        picIds = response.url.split("/")[-2]
        profileId = response.meta['pid']
        imageName = "%s(%s)" % (profileId, picIds)
        completedPicIds = self.getCompletedId(profileId)
        self.downloadThisWithIDM(imageurl, imageName + ".jpg", self.path)
        completedPicIds = picIds + "\n" + completedPicIds
        self.setCompletedId(profileId, completedPicIds)


    def profileStalker(self, response):
        print("profile Stalking is starting")
        posts = response.css("a[href*=post]::attr(href)").extract()
        profileId = response.url.split("/")[-1]
        completedPicIds = self.getCompletedId(profileId)
        for post in posts:
            picIds = post.split("/")[-2]
            if picIds not in completedPicIds:
                DpName = {'pid':profileId}
                yield scrapy.Request(post.rstrip("\n"), callback=self.profilePost, meta=DpName )
                # self.setCompletedId(picIds, completedPicIds)

    def parse(self, response):
        print("Time to wait")
        time.sleep(random.randint(0,60))
        profileId = response.url.split("/")[3]
        completedPicIds = self.getCompletedId(profileId)
        fileNames = ["%s(%s)" % (profileId, x) for x in response.css("body").re("\"shortcode\":[ ]*\"(.*?)\"")]
        # links = response.css("body").re("\"display_url\":[ ]*\"(.*?)\"")[:12]
        # links = [x.split("\\u")[0] for x in response.css("body").re("\"display_url\":[ ]*\"(.*?)\"")[:12]]
        links =  [x.replace("\\u0026","&") for x in response.css("body").re("\"display_url\":[ ]*\"(.*?)\"")[:12]]
        picIds = response.css("body").re("\"shortcode\":[ ]*\"(.*?)\"")
        types = response.css("body").re("\"__typename\":[ ]*\"(.*?)\"")
        for i in range(len(links)):
            try:
                a = picIds[i]
            except Exception as e:
                print(response.url + str(i))
                print(i)
            if picIds[i] not in completedPicIds:
                imageurl = links[i]
                imageName = fileNames[i]
                if types[i] == 'GraphVideo':
                    self.downloadThisWithIDM(imageurl, imageName + ".jpg", self.videoPath)
                elif types[i] == 'GraphSidecar':
                    spiderMeta = {}
                    spiderMeta["profileName"] = profileId + " Slide"
                    madeUpUrl = "https://www.instagram.com/p/%s/" % picIds[i]
                    print("its time to ride a car")
                    print(madeUpUrl)
                    yield scrapy.Request(url=madeUpUrl,callback=self.downloadSlideShow,priority=1,meta=spiderMeta, cookies={"csrftoken":"Hs8MEf1oSXv4t2q8FtcOtqrdxqFtsLW1","ds_user_id":"3246264185","ig_did":"217B2DB9-A084-4B9E-9F04-948BA42645B6","mid":"XmzqZgALAAHUdojAunjvlnGCtfs3","rur":"VLL","sessionid":"3246264185:1Ow06LaBDCbLAi:9","shbid":"4720","shbts":"1584196241.7547708","urlgen":"\"{\\\"103.226.202.5\\\": 133283}:1jD7p4:Dym3Kv6FDjxauuyx0bQCNHrkwsY\""})
                else:
                    self.downloadThisWithIDM(imageurl, imageName + ".jpg", self.path)
                completedPicIds = picIds[i] + "\n" + completedPicIds
        self.setCompletedId(profileId, completedPicIds)

    def downloadSlideShow(self, response):
        profileId = response.meta["profileName"]
        # import pdb; pdb.set_trace()
        completedPicIds = self.getCompletedId(profileId)
        fileNames = ["%s(%s)" % (profileId, x) for x in response.css("body").re("\"shortcode\":[ ]*\"(.*?)\"")]
        # links = response.css("body").re("\"display_url\":[ ]*\"(.*?)\"")
        links = [x.replace("\\/", "/") for x in response.css("body").re("\"display_url\":[ ]*\"(.*?)\"")]
        # import pdb; pdb.set_trace()
        picIds = response.css("body").re("\"shortcode\":[ ]*\"(.*?)\"")
        # input(links)
        for i in range(len(links)):
            if picIds[i] not in completedPicIds:
                imageurl = links[i]
                imageName = fileNames[i]
                self.downloadImg(imageurl, imageName + ".jpg", self.path)
                completedPicIds = picIds[i] + "\n" + completedPicIds

        self.setCompletedId(profileId, completedPicIds)

    def debug(self, msg):
        if True:
            print(msg)

    def setCompletedId(self, profileId, completedPicIds):
        self.ensure_dir("Completed\\")
        with open("Completed\\" + profileId + ".ccode", "w") as completed:
            completed.write(completedPicIds)


if __name__ == "__main__":
    try:
        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            
        })
        process.crawl(sinSpider)
        process.start()
    except Exception as e:
        with open("log.txt", "a+") as inF:
            inF.write(str(e) + "\n")
