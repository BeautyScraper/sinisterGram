import sinSpider as t

class MoolestingBear(t.sinSpider):
    def start_requests(self):
        with open("instaLinks.opml", "r+") as instalink:
            # time.sleep(60)
            urls = instalink.readlines()

        t.random.shuffle(urls)
        for url in urls:
            rl = url.split("/")[3]
            url = "https://www.picuki.com/profile/%s" % rl
            print("currently opening the url =" + url)
            
            # yield scrapy.Request(url.rstrip("\n"), callback=self.parse,  cookies={"csrftoken":"Hs8MEf1oSXv4t2q8FtcOtqrdxqFtsLW1","ds_user_id":"3246264185","ig_did":"217B2DB9-A084-4B9E-9F04-948BA42645B6","mid":"XmzqZgALAAHUdojAunjvlnGCtfs3","rur":"VLL","sessionid":"3246264185:1Ow06LaBDCbLAi:9","shbid":"4720","shbts":"1584196241.7547708","urlgen":"\"{\\\"103.226.202.5\\\": 133283}:1jD7p4:Dym3Kv6FDjxauuyx0bQCNHrkwsY\""}, errback=self.on404, )
            yield t.scrapy.Request(url.rstrip("\n"), callback=self.profileStalker )


    def profileStalker(self, response):
        print("Starting profile stalking %s" % response.url)
        postLinks = response.css("a[href*=\/media\/]::attr(href)").extract()
        postIds = [x.split("/")[-1] for x in postLinks]
        profileId = response.url.strip("/").split("/")[-1]
        
        for url in postLinks:
            meta = {'pid':profileId,'postId':url.split("/")[-1]}
            yield t.scrapy.Request(url.rstrip("\n"), callback=self.PostStalker )

    def GenStalker(self,response,postLinks,profileId,postIds):
        import pdb;pdb.set_trace()
        completedPicIds = self.getCompletedId(profileId)
        for links,post in zip(postLinks,postIds):
            if post not in completedPicIds:
                meta = {'pid':profileId,'postId':post}
                yield t.scrapy.Request(url.rstrip(), callback=self.PostStalker, errback=self.on404,meta=meta,priority=2 )
                completedPicIds = picIds + "\n" + completedPicIds
        self.setCompletedId(profileId, completedPicIds)
    
    def PostStalker(self, response):
        imgLinks = response.css("#image-photo::attr(src)").extract()
        profileId = response.meta['pid']
        postId = response.meta['postId']
        fileNames = ["%s(%s)" % (profileId,postId+str(i)) for i,_ in enumerate(imgLinks)]
        self.BatchDownloader(response,imgLinks,FileNames)

    def BatchDownloader(self,response,imgLinks,FileNames):
        for iUrl, FileName in zip(imgLinks,FileNames):
            self.downloadThisWithIDM(iUrl, FileName + ".jpg", self.path)

if __name__ == "__main__":
    print("Starting")
    try:
        process = t.CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            
        })
        process.crawl(MoolestingBear)
        process.start()
    except Exception as e:
        with open("log.txt", "a+") as inF:
            inF.write(str(e) + "\n")
