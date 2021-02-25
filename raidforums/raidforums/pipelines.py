# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


import sqlite3
from random import seed
from random import randint
from time import time



class RaidforumsPipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("raidforums_database.db")
        self.conn.execute("""PRAGMA foreign_keys = 1""")
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""drop table if exists post_table""")
        self.curr.execute("""drop table if exists details_post""")
        self.curr.execute("""drop table if exists user_table""")
        self.curr.execute("""create table if not exists detail_post_tb(
                                            id text primary key ,
                                            link_to_post text,
                                            actual_post text
                                            )""")
        self.curr.execute("""create table if not exists user_tb(
                                            id text primary key,
                                            user_status text,
                                            user_posts smallint,
                                            user_threads smallint,
                                            user_joined text,
                                            user_reputation text,
                                            user_service text
                                            )""")
        self.curr.execute("""create table if not exists post_tb(
                                            id text primary key,
                                            post_name text,
                                            post_details text,
                                            post_creator text,
                                            post_date text,
                                            post_views_no smallint,
                                            post_replies_no smallint,
                                            link_to_post text,
                                            foreign key (post_details) references post_tb(id),
                                            foreign key (post_creator) references user_table(id)
                                            )""")

    def process_item(self, item, spider):
        print("in pipeline")
        self.store_db(item)
        self.close_db()
        return item

    def create_unique_id(self):
        unique_id = str(randint(1, 1000000)) + str(time())
        return unique_id

    def store_db(self,item):          #modifications required about foreign_keys and id generation

        detail_post_id = self.create_unique_id()
        user_id = self.create_unique_id()
        post_id = self.create_unique_id()

        self.curr.execute("""insert into detail_post_tb values(?,?,?)""", (
            detail_post_id,
            item['post_link'],
            item['actual_post']
        ))
        self.curr.execute("""insert into user_tb values(?,?,?,?,?,?,?)""", (
            user_id,
            item['user_status'],
            item['user_posts'],
            item['user_threads'],
            item['user_joined'],
            item['user_reputation'],
            item['user_service']
        ))
        self.curr.execute("""insert into post_tb values(?,?,?,?,?,?,?,?)""", (
            post_id,
            item['post_name'],
            detail_post_id,
            user_id,
            item['post_date'],
            item['post_views_no'],
            item['post_replies_no'],
            item['link_to_post']
        ))

        self.conn.commit()


    def close_db(self):
        self.curr.close()
        self.conn.close()
