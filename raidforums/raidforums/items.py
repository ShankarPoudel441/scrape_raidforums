# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RaidforumsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    post_name = scrapy.Field()
    post_by = scrapy.Field()
    post_date = scrapy.Field()
    post_views_no = scrapy.Field()
    post_replies_no = scrapy.Field()
    link_to_post = scrapy.Field()
    actual_post = scrapy.Field()
    user_name = scrapy.Field()
    user_status = scrapy.Field()
    user_posts = scrapy.Field()
    user_threads = scrapy.Field()
    user_joined = scrapy.Field()
    user_reputation = scrapy.Field()
    user_service = scrapy.Field()
    pass
