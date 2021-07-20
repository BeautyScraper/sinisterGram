import sinSpider as t
import re

class MoolestingBear(t.sinSpider):
    delay = False
    def start_requests(self):
        with open("instaLinks.opml", "r+") as instalink:
            # time.sleep(60)
            urls = instalink.readlines()

        t.random.shuffle(urls)
        for url in urls:
            rl = url.split("/")[3]
            # url = "https://www.instastalker2.com/user/%s" % rl
            url = "https://www.pixwox.com/id/profile/%s/" % rl
            print("currently opening the url =" + url)
            
            # yield scrapy.Request(url.rstrip("\n"), callback=self.parse,  cookies={"csrftoken":"Hs8MEf1oSXv4t2q8FtcOtqrdxqFtsLW1","ds_user_id":"3246264185","ig_did":"217B2DB9-A084-4B9E-9F04-948BA42645B6","mid":"XmzqZgALAAHUdojAunjvlnGCtfs3","rur":"VLL","sessionid":"3246264185:1Ow06LaBDCbLAi:9","shbid":"4720","shbts":"1584196241.7547708","urlgen":"\"{\\\"103.226.202.5\\\": 133283}:1jD7p4:Dym3Kv6FDjxauuyx0bQCNHrkwsY\""}, errback=self.on404, )
            yield t.scrapy.Request(url.rstrip("\n"), callback=self.profileStalker )

    def getId(self, response):
        id = response.css("body").re("profilePage_([^\"]*)")[0]
        rl = response.url.split("/")[3]
        url = "https://gramho.com/profile/%s/%s" % (rl,id)
        with open("gramhoUrls.opml","a+") as fp:
            fp.write(url+"\n")
        yield t.scrapy.Request(url.rstrip("\n"), callback=self.profileStalker,priority = 1)
        

    def profileStalker(self, response):
        print("Starting profile stalking %s" % response.url)
        postLinks = response.css('a[href*=post]::attr(href)').extract()
        
        # import pdb;pdb.set_trace()
        postIds = [re.sub('\/#\d+','',x).strip('/').split("/")[-1] for x in postLinks]
        profileId = response.url.strip("/").split("/")[-1]
        
        print(response.url,' total posts found on this page ',len(postLinks))
        if self.delay:
            t.time.sleep(random.randint(0,60))
        completedPicIds = self.getCompletedId(profileId)
        for links,post in zip(postLinks,postIds):
            if post not in completedPicIds:
                # import pdb;pdb.set_trace()
                meta = {'pid':profileId,'postId':post}
                url = t.urllib.request.urljoin(response.url, links)
                yield t.scrapy.Request(url.rstrip(), callback=self.PostStalker, errback=self.on404,meta=meta,priority=2 )
                completedPicIds = post + "\n" + completedPicIds
        self.setCompletedId(profileId, completedPicIds)


    def PostStalker(self, response):
        imgLinks = [x for x in response.css('.downbtn::attr(href)').extract() if '.mp4' not in x]
        # imgLinks = response.css(".media-img::attr(src)").extract() if len(imgLinks) <= 0 else imgLinks
        profileId = response.meta['pid']
        postId = response.meta['postId']
        if len(postId) < 4:
            import pdb;pdb.set_trace()
        fileNames = ["%s(%s)" % (profileId,postId+str(i).replace("0","")) for i,_ in enumerate(imgLinks)]
        # import pdb;pdb.set_trace()
        self.BatchDownloader(response,imgLinks,fileNames)

    def BatchDownloader(self,response,imgLinks,FileNames):
        for iUrl, FileName in zip(imgLinks,FileNames):
            self.downloadThisWithIDM(iUrl, FileName + ".jpg", self.path)

if __name__ == "__main__":
    print("Starting")
    try:
        process = t.CrawlerProcess({
            'USER_AGENT': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            
        })
        process.crawl(MoolestingBear)
        process.start()
    except Exception as e:
        with open("log.txt", "a+") as inF:
            inF.write(str(e) + "\n")
