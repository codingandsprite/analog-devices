from collections import namedtuple
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import json

STREAM = list()

Post = namedtuple('Post', ['link', 'title'])

LAST_PAGE = 1

url = "https://analogdevices.wd1.myworkdayjobs.com/wday/cxs/analogdevices/External/jobs"

headers = {
    'accept': 'application/json',
    'accept-language': 'en-US',
    'content-type': 'application/json',
    'origin': 'https://analogdevices.wd1.myworkdayjobs.com',
    'priority': 'u=1, i',
    'referer': 'https://analogdevices.wd1.myworkdayjobs.com/en-US/External/details/UI---Software-Engineer_R243497?locationCountry=bc33aa3152ec42d4995f4791a106ed09',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}

json_data = json.loads('{"appliedFacets":{"locationCountry":["bc33aa3152ec42d4995f4791a106ed09"]},"limit":20,"offset":0,"searchText":""}')

r = requests.post(url=url, headers=headers, json=json_data)

for jobPosting in dict(r.json())['jobPostings']:
    title = jobPosting['title']
    link = r"https://analogdevices.wd1.myworkdayjobs.com/en-US/External" + jobPosting['externalPath']
    STREAM.append(Post(link, title))

if __name__ == "__main__":

    NOW = datetime.now()
    XML = "\n".join([ r"""<?xml version="1.0" encoding="UTF-8" ?>""",
            r"""<rss version="2.0">""",
            r"""<channel>""",
            r"""<title>Analog Devices</title>""",
            r"""<link></link>""",
            r"""<description>Analog Devices</description>""",
            r"""<language>en-us</language>""",
            r"""<pubDate>"""+NOW.strftime("%a, %d %b %Y %H:%M:%S GMT")+r"""</pubDate>""",
            r"""<lastBuildDate>"""+NOW.strftime("%a, %d %b %Y %H:%M:%S GMT")+r"""</lastBuildDate>""",
            "\n".join([r"""<item><title><![CDATA["""+x.title+r"""]]></title><link>"""+x.link+r"""</link></item>""" for x in STREAM]),
            r"""</channel>""",
            r"""</rss>""",
    ])

    print(XML)
