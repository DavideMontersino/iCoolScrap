from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import Selector

from iCoolScrap.items import IcoolhuntItem

class ICoolSpider(Spider):
    """
    Defines a spider for icoolhunt website
    """

    name = "icoolhunt"
    max_preys = 20 #max number of preys we want to parse
    allowed_domains = ["icoolhunt.com"]
    parsed_preys = 0
    start_urls = [
        "http://www.icoolhunt.com/explore"
    ]

    def __init__(self, maxpreys=None, *args, **kwargs):
        """
        Inits the spider and reads arguments from command line 
        """
        super(ICoolSpider, self).__init__(*args, **kwargs)
        if maxpreys != None:
            self.max_preys = int(maxpreys) #we read maxpreys from command line



    def parse(self, response): 
        """
        Spider's parse method definition; parses 'explore' page and 
        """
        print 'will parse a maximum of ' + str(self.max_preys) + ' preys'
        sel = Selector(response)
        preys = sel.css('div.explore.stream div.item.prey')
        items = []
        if 'items' in response.meta:
            print 'inside second'
            items = response.meta['items']
        for prey, last in self.lookahead(preys): #we need to know whether we have reached the last prey in page
            item = IcoolhuntItem()
            item['data_stream_id'] = prey.css ('::attr(data-stream-id)').extract()
            item['description'] = prey.css('div.description::text').extract()
            item['image'] = prey.css('a.prey-link img::attr(src)').extract()[0][:-8]
            item['user_link'] = prey.css('div.hunter > a::attr(href)').extract()
            item['user_name'] = prey.css('div.hunter > a div.nickname::text').extract()
            item['prey_link'] = prey.css('a.prey-link::attr(href)').extract()
            item['last'] = last
            request = Request("https://www.icoolhunt.com/wep" + item['prey_link'][0], callback=self.parse_prey_page) #we read tags from the prey's page
            request.meta['item'] = item
            self.parsed_preys = self.parsed_preys + 1
            items.append(request)
            if self.parsed_preys >= self.max_preys:
                return items
            if last:
                next_page_request = Request("https://www.icoolhunt.com/explore?f.refid=" + item['data_stream_id'][0], callback = self.parse) #recursively call itself if last prey has been reached - and maxPrey has not been reached
                request.meta['items'] = items
                items.append(next_page_request)
        return items

    def parse_prey_page(self, response):
        sel = Selector(response)
        item = response.meta['item']
        item['tag_name'] = sel.css('ul.tags li a::text').extract() #no need to scrap the url too; tags urls are just a query with the tag name.
        return item


    def lookahead(self, iterable):
        it = iter(iterable)
        last = it.next() 
        for val in it:
            yield last, False
            last = val
        yield last, True

    def first_or_none (self, list):
        return list[0] if list else ''