import scrapy

class DiscussionForumSpider(scrapy.Spider):
    name = 'forum'
    page_number = 2
    c =0

    allowed_domains = ["forums.hardwarezone.com.sg"]
    myBaseUrl = ''
    start_urls = []
    def __init__(self, category='', **kwargs): # The category variable will have the input URL.
        self.myBaseUrl = category
        self.start_urls.append(self.myBaseUrl)
        super().__init__(**kwargs)

    #custom_settings = {'FEED_URI': 'discussionforum/outputfile.json', 'CLOSESPIDER_TIMEOUT' : 15} # This will tell scrapy to store the scraped data to outputfile.csv and for how long the spider should run.


    def parse(self, response):
        all_div = response.xpath("//*[@class='post-wrapper']")
        author = response.css('#content-header::text').extract_first()
        title = response.css('.header-gray::text').extract_first().strip()
        like = response.css('.vbseo-likes-count span::text').extract_first()
        link = response.url

        for div in all_div:
            sequence = div.css('.thead strong::text').extract()
            date = div.css('.thead:nth-child(1)::text')[2:-1].extract()
            user = div.css('.bigusername::text').extract()
            comment = div.css('.post_message::text').extract()
            if (DiscussionForumSpider.c==0):
                      DiscussionForumSpider.c = DiscussionForumSpider.c + 1
                      yield {'author' : author,
                          'title' : title,
                          'like' : like,
                          'Link' : link,
                          'Sequence' : sequence[0],
                          'Date' : [dt.strip() for dt in date][0],
                          'User' : user[0],
                          'Comment' : [com.strip() for com in comment][0]

                          }
            else:
                      yield {
                             'Link' : link,
                             'Sequence' : sequence[0],
                             'Date' : [dt.strip() for dt in date][0],
                             'User' : user[0],
                             'Comment' : [com.strip() for com in comment][0]
                              }
        next_url_path = response.css("li+ .prevnext a").xpath('@href').extract_first()
        if next_url_path:
            yield scrapy.Request(
                response.urljoin(next_url_path),
                callback=self.parse
            )
