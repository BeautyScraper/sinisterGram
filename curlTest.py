from scrapy import Request

url = 'https://www.pixwox.com/id/profile/pang_phakakul/'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Alt-Used": "www.pixwox.com",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0",
    "TE": "Trailers"
}

req = Request(
    url=url,
    method='GET',
    dont_filter=True,
    headers=headers,
)

# fetch(request)
# import pdb;pdb.set_trace()