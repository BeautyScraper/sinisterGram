import sinSpider as t
import re
import pandas as pd
from pathlib import Path
from urllib.parse import quote

class MoolestingBear(t.sinSpider):
    delay = False
    DownImage = True
    DownVideo = True
    def start_requests(self):
        profileLink = input('Enter the url:')
        # t.random.shuffle(urls)
        # for url in [profileLink]:
        self.DownVideo = input('download videos') == 'y'
        self.DownImage = input('download Images') == 'y'
        
        for url in [profileLink]:
            rl = url.split("/")[3]
            self.path = 'C:\\GalImgs\\imageSet\\' + rl
            # url = "https://www.instastalker2.com/user/%s" % rl
            url = "https://www.pixwox.com/id/profile/%s/" % rl
            print("currently opening the url =" + url)
            
            # yield scrapy.Request(url.rstrip("\n"), callback=self.parse,  cookies={"csrftoken":"Hs8MEf1oSXv4t2q8FtcOtqrdxqFtsLW1","ds_user_id":"3246264185","ig_did":"217B2DB9-A084-4B9E-9F04-948BA42645B6","mid":"XmzqZgALAAHUdojAunjvlnGCtfs3","rur":"VLL","sessionid":"3246264185:1Ow06LaBDCbLAi:9","shbid":"4720","shbts":"1584196241.7547708","urlgen":"\"{\\\"103.226.202.5\\\": 133283}:1jD7p4:Dym3Kv6FDjxauuyx0bQCNHrkwsY\""}, errback=self.on404, )
            yield t.scrapy.Request(url.rstrip("\n"), callback=self.getXHRurl )

    def getId(self, response):
        id = response.css("body").re("profilePage_([^\"]*)")[0]
        rl = response.url.split("/")[3]
        url = "https://gramho.com/profile/%s/%s" % (rl,id)
        with open("gramhoUrls.opml","a+") as fp:
            fp.write(url+"\n")
        yield t.scrapy.Request(url.rstrip("\n"), callback=self.profileStalker,priority = 1)
    
    def getXHRurl(self,response):
        nextxhr = response.css('.more_btn::attr(data-next)').extract()
        nextxhr = quote(nextxhr[0])
        userId = response.css('input[name=userid]::attr(value)').extract()[0]
        xhrUrl = 'https://api.pixwox.com/posts?userid=%s&next=%s&hl=id' % (userId, nextxhr)
        meta = {'profileId':response.url.strip("/").split("/")[-1] +'FPXX' ,'userId': userId}
        # import pdb;pdb.set_trace()
        for url in [xhrUrl]:
            yield t.scrapy.Request(url.rstrip("\n"), callback=self.profileStalker,meta = meta)
            
    def extractFromThisItem(self,item):
        imgUrls = []
        if item['type'] == 'img_multi' and self.DownImage:
            imgUrls = [x['down_pic'] for x in item['children_items']]
        elif item['type'] == 'img_sig' and self.DownImage:
            imgUrls = [item['down_pic']]
            # import pdb;pdb.set_trace()
        elif (item['type'] == "video" or item['type'] == "igtv" ) and self.DownVideo:
            imgUrls = [item['video']]
            # import pdb;pdb.set_trace()
        # else:
            # import pdb;pdb.set_trace()
        return imgUrls
    
    def profileStalker(self, response):
        print("Starting profile stalking %s" % response.url)
        # postLinks = response.css('a[href*=post]::attr(href)').extract()
        
        # import pdb;pdb.set_trace()
        df = pd.read_json(response.text)
        filename = []
        # imgUrls = []
        profileId = response.meta['profileId']
        userId = response.meta['userId']
        completedPicIds = self.getCompletedId(profileId)
        for item in df['items']:
            postId = item['shortcode']
            if postId not in completedPicIds:
                imgUrls = self.extractFromThisItem(item)
                if len(imgUrls) <= 0:
                    continue
                completedPicIds = postId + "\n" + completedPicIds
                
                fileNames = ["%s(%s)" % (profileId,postId+str(i).replace("0","")) for i,_ in enumerate(imgUrls)]
                self.BatchDownloader(response,imgUrls,fileNames)
                self.setCompletedId(profileId, completedPicIds)
        # import pdb;pdb.set_trace()
        if df['has_next'][0]:
            nextxhr = quote(df['next'][0])
            xhrUrl = 'https://api.pixwox.com/posts?userid=%s&next=%s&hl=id' % (userId, nextxhr)
            # meta = {'profileId': ,'userId': userId}
            for url in [xhrUrl]:
                yield t.scrapy.Request(url.rstrip("\n"), callback=self.profileStalker,meta = response.meta)
            
        # postIds = [re.sub('\/#\d+','',x).strip('/').split("/")[-1] for x in postLinks]
        
        
        # print(response.url,' total posts found on this page ',len(postLinks))
        # if self.delay:
            # t.time.sleep(random.randint(0,60))
        # completedPicIds = self.getCompletedId(profileId)
        # for links,post in zip(postLinks,postIds):
            # if post not in completedPicIds:
                # import pdb;pdb.set_trace()
                # meta = {'pid':profileId,'postId':post}
                # url = t.urllib.request.urljoin(response.url, links)
                # yield t.scrapy.Request(url.rstrip(), callback=self.PostStalker, errback=self.on404,meta=meta,priority=2 )
                # completedPicIds = post + "\n" + completedPicIds
        # self.setCompletedId(profileId, completedPicIds)


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
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            
        })
        process.crawl(MoolestingBear)
        process.start()
    except Exception as e:
        with open("log.txt", "a+") as inF:
            inF.write(str(e) + "\n")
