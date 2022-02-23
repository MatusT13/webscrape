import scrapy


class PolSpider(scrapy.Spider):
    name = 'pol'
    allowed_domains = ['politico.com']
    start_urls = ['https://www.politico.com/search?q=technology']

    def parse(self, response):
        for pol in response.css("article.story-frag.format-ml"):
            yield{
                "Title": pol.css("img").attrib["alt"],
                "Link": pol.css("a").attrib["href"],
                "Intro": pol.css("div.tease").css("p::text").get(),
                "Category": pol.css("p.category::text").get(),
                "DateandTime": pol.css("time").attrib["datetime"],
                }
        for button in response.css("a.button"):
            if button.css("::text").get() == "Next page >>":
                next_page = button.attrib["href"]
                print(" \n Next Page :" + next_page + "\n")
                yield response.follow(next_page, callback=self.parse)

