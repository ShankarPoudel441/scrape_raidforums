import scrapy

class Postspider(scrapy.Spider):
    name = 'posts'
    # allowed_domains = ["https://raidforums.com"]
    start_urls = [
        'https://raidforums.com/Thread-Ransomware-links'
    ]
    base_url = 'https://raidforums.com/'

    def parse(self, response):
        name = 'posts'
        # allowed_domains = ["https://raidforums.com"]
        start_urls = [
            'https://raidforums.com/Thread-CSV-Gay-and-Lesbian-2-1-Million'
        ]


        actual_post = response.css('.post_body::text').get()
        print("actial post", actual_post)
        user_name = response.css('.largetext span::text').get()
        print("user_name" , user_name)
        user_status = response.css('.post__user-title::text').get()
        print("user_status", user_status)
        user_posts = response.css('.group:nth-child(1) .float_right ::text').get()
        print("user_posts", user_posts)
        user_threads = response.css('.group:nth-child(2) .float_right ::text').get()
        print("user_threads", user_threads)
        user_joined = response.css('.group:nth-child(3) .float_right ::text').get()
        print("user_joined",user_joined)
        user_reputation = response.css('.group:nth-child(4) .float_right').xpath('a/strong/text()').get()
        print("user_reputation",user_reputation)
        try:
            user_service = response.css('.user_service::text').get()
        except:
            user_service = "less than a year"
        print("user_service",user_service)

        thisdict = {
            'actual_post' : actual_post.strip(),
            'user_name' : user_name,
            'user_status' : user_status.strip(),
            'user_posts': user_posts.strip(),
            'user_reputation' : user_reputation,
            'user_joined' : user_joined,
            'user_threads' : user_threads,
            'user_service' :user_service
        }
        yield thisdict