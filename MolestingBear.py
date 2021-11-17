import sinSpider as t

class MoolestingBear(t.sinSpider):
    def start_requests(self):
        with open("instaLinks.opml", "r+") as instalink:
            # time.sleep(60)
            urls = instalink.readlines()

        t.random.shuffle(urls)
        for url in urls:
            rl = url.split("/")[3]
            url = "https://picbear.co/profile/%s" % rl
            print("currently opening the url =" + url)
            
            # yield scrapy.Request(url.rstrip("\n"), callback=self.parse,  cookies={"csrftoken":"Hs8MEf1oSXv4t2q8FtcOtqrdxqFtsLW1","ds_user_id":"3246264185","ig_did":"217B2DB9-A084-4B9E-9F04-948BA42645B6","mid":"XmzqZgALAAHUdojAunjvlnGCtfs3","rur":"VLL","sessionid":"3246264185:1Ow06LaBDCbLAi:9","shbid":"4720","shbts":"1584196241.7547708","urlgen":"\"{\\\"103.226.202.5\\\": 133283}:1jD7p4:Dym3Kv6FDjxauuyx0bQCNHrkwsY\""}, errback=self.on404, )
            yield t.scrapy.Request(url.rstrip("\n"), callback=self.profileStalker, errback=self.on404, )



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
