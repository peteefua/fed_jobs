import scrapy


def jobs_from_response(response):
    pass

def get_jobfield1(response, category):
    pass

class QuotesSpider(scrapy.Spider):
    name = "fed_reserve_jobs"
    start_urls = [
        'https://www.federalreserve.gov/start-job-search.htm',
    ]

    def parse(self, response):
        search_page = response.css('div.embed-responsive iframe.embed-responsive-item').xpath('@src').extract_first()
        yield scrapy.Request(search_page, callback=self.start_search)

    def start_search(self, response):
        keywords = getattr(self, 'keywords', None)
        jobfield1 = getattr(self, 'category', None)

        if jobfield1 != None:
            jobfield1 = get_jobfield1(response, jobfield1)

        yield scrapy.FormRequest.from_response(
            response,
            formdata={'keyword': keywords, 'jobfield1': jobfield1},
            callback=self.after_search
        )

    def after_search(self, response):
        result = response.css('td#response').extract_first()
        with open('search_out.txt', 'wb') as f:
            f.write(response.headers)
