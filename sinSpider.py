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
        'DOWNLOAD_DELAY': 1,
    }

    def __init__(self):
        self.path = "D:\\paradise\\stuff\\sinisterBabes\\"
        self.videoPath = "D:\\paradise\\stuff\\sinisterVideos\\"


    def start_requests(self):
        with open("instaLinks.opml", "r+") as instalink:
            urls = instalink.readlines()

        random.shuffle(urls)
        for url in urls:
            print("currently opening the url =" + url)
            yield scrapy.Request(url.rstrip("\n"), callback=self.parse, errback=self.on404)

    def on404(self, failure):
        print(failure.value.response.status)
        if failure.value.response.status == 429:
            time.sleep(10)
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

    def parse(self, response):
        profileId = response.url.split("/")[3]
        completedPicIds = self.getCompletedId(profileId)
        fileNames = ["%s(%s)" % (profileId, x) for x in response.css("body").re("\"shortcode\":[ ]*\"(.*?)\"")]
        links = response.css("body").re("\"display_url\":[ ]*\"(.*?)\"")
        picIds = response.css("body").re("\"shortcode\":[ ]*\"(.*?)\"")
        types = response.css("body").re("\"__typename\":[ ]*\"(.*?)\"")

        for i in range(len(links)):
            if picIds[i] not in completedPicIds:
                imageurl = links[i]
                imageName = fileNames[i]
                if types[i] != 'GraphVideo':
                    self.downloadImg(imageurl, imageName + ".jpg", self.path)
                else:
                    self.downloadImg(imageurl, imageName + ".jpg", self.videoPath)
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
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
        process.crawl(sinSpider)
        process.start()
    except Exception as e:
        with open("log.txt", "a+") as inF:
            inF.write(str(e) + "\n")
