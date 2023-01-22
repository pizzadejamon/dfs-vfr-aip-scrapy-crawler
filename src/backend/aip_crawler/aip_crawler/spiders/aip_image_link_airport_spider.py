from pathlib import Path
import random
from aip_crawler.items import AIPPageItem
import scrapy
import re

class APIImageLinkAirportSpider(scrapy.Spider):
    name = "aip_image_link_airport_spider"
    baseurl = "https://aip.dfs.de/basicVFR/"
    #baseurl = "https://aip.dfs.de/BasicVFR/2023JAN16/3557c53472aaea57b7ebb7d8f996342a.html"
    aipfolder = None

    def __init__(self, aip_result_folder=None, *args, **kwargs):
        super(APIImageLinkAirportSpider, self).__init__(*args, **kwargs)
    
        if not Path(aip_result_folder).resolve().exists():
            raise FileNotFoundError("Specified result folder for the AIP images does not exist")

        self.aipfolder = str(Path(aip_result_folder).resolve())

    def start_requests(self):
        yield scrapy.Request(url=self.baseurl, callback=self.parse, headers={"User-Agent": self.random_ua()})

    def random_ua(self, k=1):
        ua_pct = {'ua': {'0': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', '1': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76', '2': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0', '3': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54', '4': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', '5': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15', '6': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.46', '7': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15', '8': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67', '9': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0', '10': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0', '11': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', '12': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26', '13': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0', '14': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0', '15': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62', '16': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', '17': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', '18': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.5.715 Yowser/2.5 Safari/537.36', '19': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36', '20': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', '21': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0', '22': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0', '23': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', '24': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362', '25': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko', '26': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36', '27': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76', '28': 'Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0', '29': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0', '30': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52', '31': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36', '32': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52', '33': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.70', '34': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42', '35': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0', '36': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.66', '37': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; Touch; rv:11.0) like Gecko'}, 'pct': {'0': 36.8341859765, '1': 20.4935299428, '2': 7.7640686127, '3': 7.1020162504, '4': 6.74089678, '5': 2.8889557629, '6': 1.9259705086, '7': 1.9259705086, '8': 1.2037315679, '9': 1.2037315679, '10': 0.8426120975, '11': 0.8426120975, '12': 0.7222389407, '13': 0.7222389407, '14': 0.7222389407, '15': 0.6018657839, '16': 0.6018657839, '17': 0.4814926271, '18': 0.4814926271, '19': 0.4814926271, '20': 0.4814926271, '21': 0.4814926271, '22': 0.3611194704, '23': 0.3611194704, '24': 0.3611194704, '25': 0.3611194704, '26': 0.3611194704, '27': 0.2407463136, '28': 0.2407463136, '29': 0.2407463136, '30': 0.2407463136, '31': 0.2407463136, '32': 0.2407463136, '33': 0.2407463136, '34': 0.2407463136, '35': 0.2407463136, '36': 0.2407463136, '37': 0.2407463136}}
        return random.choices(list(ua_pct['ua'].values()), list(ua_pct['pct'].values()), k=k)

    def parse(self, response):
        url = "/".join(response.url.split('/')[:-1]) + "/"
        
        title = response.selector.xpath("//div[contains(@class,'headlineText')]/descendant-or-self::*/text()").getall()[0].strip()
        self.log("Scraping " + title)

        if title == "Aeronautical Information Publication VFR":
            next = response.selector.xpath("//a[@class='folder-link' and .//*[text() = 'AD Aerodromes']]/@href").get()
            yield scrapy.Request(url=url + next, callback=self.parse, headers={"User-Agent": self.random_ua()})
        elif title == "AD Aerodromes":
            next = response.selector.xpath("//a[@class='folder-link' and .//*[re:match(text(), '([A-Z]-[A-Z])|^[A-Z]\s+$')]]/@href").getall()
            for letterPage in next:
                yield scrapy.Request(url=url + letterPage, callback=self.parse, headers={"User-Agent": self.random_ua()})
        elif bool(re.match('^([A-Z]-[A-Z])$|^[A-Z]$', title)):
            next = response.selector.xpath("//a[@class='folder-link']/@href").getall()
            for aerodromePage in next:
                yield scrapy.Request(url=url + aerodromePage, callback=self.parse, headers={"User-Agent": self.random_ua()})
        elif bool(re.match('^.*\sED[A-Z]{2,}$', title)):
            next = response.selector.xpath("//a[@class='document-link']/@href").getall()
            for imagePage in next:
                request =scrapy.Request(url=url + imagePage, callback=self.parseImagePafe, headers={"User-Agent": self.random_ua()}, priority=-1)
                request.meta['airport'] = re.match('^.*\s(ED[A-Z]{2,})$', title).group(1)
                yield request
        else:
            self.log("Could not identified the currently crawled page")

    def parseImagePafe(self, response):
        filename = response.selector.xpath("//div[contains(@class,'headlineText')]/descendant-or-self::*/text()").getall()[0].strip()
        self.log("Scraping " + filename)
        aipentryitem = AIPPageItem()
        aipentryitem['airport'] = response.meta['airport']
        aipentryitem['filename'] = self.aipfolder + "\\" + response.meta['airport'] + "\\"  + filename + ".png"
        aipentryitem['src'] = response.selector.xpath("//*[@class='pageImage']/@src").getall()[0]
        yield aipentryitem
   


        





        