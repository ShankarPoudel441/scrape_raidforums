import scrapy
from scrapy import  Request
import re
from ..items import RaidforumsItem


class Quotespider(scrapy.Spider):
    name = 'raid'
    # allowed_domains = ["https://raidforums.com"]
    start_urls = [
        'https://raidforums.com/Forum-Anime-Manga'
    ]
    base_url = 'https://raidforums.com/'

    def parse(self, response):
        items = RaidforumsItem()

        post_div = response.xpath('/html/body/div[1]/main/section[2]/table//tr')
        length = len(post_div)

        counter=0

        for post in post_div[10:length-1]:
            counter += 1
            print("counter", counter)
            items["post_name"] = post.css(".forum-display__thread-subject::text").extract()
            items["post_by"] = post.xpath("td[2]/div/span[1]/a/span/text()").extract()
            print("post_by",items['post_by'])

            items["post_views_no"] = post.css(".hidden-sm:nth-child(4)::text").extract()
            items["post_replies_no"] = post.css(".hidden-sm > a::text").extract()

            next_page = post.xpath('td[2]/div/div[1]/span/a/@href').get()
            print("next page ", next_page)

            items["link_to_post"] = self.base_url + str(next_page)
            print("next page", items["link_to_post"])

            try:
                post_date = post.xpath('td[2]/div/span[2]/span/@title').extract
                possibility = post.css('.forum-display__thread-date::text').extract()
                if (re.search("ago$", str(possibility)) == None):
                    items["post_date"] = post_date + possibility[-12:]
            except:
                items["post_date"] = post.css('.forum-display__thread-date::text').extract()
                print("post date2", items["post_date"])


            # yield items

            yield Request(items['link_to_post'],
                            meta={'items': items},
                            callback=self.parse_post)


    def parse_post(self,response):
        items = response.request.meta['items']

        actual_post = response.css('.post_body::text').get()
        user_name = response.css('.largetext span::text').get()
        user_status = response.css('.post__user-title::text').get()
        user_posts = response.css('.group:nth-child(1) .float_right ::text').get()
        user_threads = response.css('.group:nth-child(2) .float_right ::text').get()
        user_joined = response.css('.group:nth-child(3) .float_right ::text').get()
        user_reputation = response.css('.group:nth-child(4) .float_right').xpath('a/strong/text()').get()
        try:
            user_service = response.css('.user_service::text').get()
        except:
            user_service = "less than a year"
        print("user_service", user_service)

        items['actual_post']= actual_post.strip()
        items['user_name']= user_name
        items['user_status']= user_status.strip()
        items['user_posts']= user_posts.strip()
        items['user_reputation']= user_reputation
        items['user_joined']= user_joined
        items['user_threads']= user_threads
        items['user_service']= user_service


        yield items




