# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class JobscrawlerQianchengwuyouItem(scrapy.Item):
    job_type = scrapy.Field()  # 大数据
    job_name = scrapy.Field()  # 1招聘名称 ok
    job_info = scrapy.Field()  # 2职位信息 ok
    job_sal = scrapy.Field()  # 3薪资 ok
    job_benefit = scrapy.Field()  # 4职位福利 ok
    exp_require = scrapy.Field()  # 5经验要求 ok
    edu_require = scrapy.Field()  # 6学历要求 ok
    company_name = scrapy.Field()  # 7公司名称 ok
    emp_wanted_num= scrapy.Field()  # 12招聘人数 ok
    releast_time = scrapy.Field()  # 13发布时间 ok
    job_loc = scrapy.Field()  # 15工作地址 ok


