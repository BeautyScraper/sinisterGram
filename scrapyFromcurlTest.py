from scrapy import Request

url = '''https://www.pixwox.com/id/profile/namita.official/'''

curlPosixcmd = '''curl 'https://www.pixwox.com/id/profile/namita.official/' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' -H 'Cache-Control: max-age=0' -H 'TE: Trailers\''''

curlWinCmd = '''curl "https://www.pixwox.com/id/profile/namita.official/" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0" -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8" -H "Accept-Language: en-US,en;q=0.5" --compressed -H "Connection: keep-alive" -H "Upgrade-Insecure-Requests: 1" -H "Cache-Control: max-age=0" -H "TE: Trailers"'''

# req = Request.from_curl(curlPosixcmd)
req = Request.from_curl(curlPosixcmd,ignore_unknown_options=False)
res = fetch(req)