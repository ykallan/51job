# -*- coding: utf-8 -*-
import scrapy
from jobscrawler_qianchengwuyou.items import JobscrawlerQianchengwuyouItem
import re
import numpy as np


class QianchengSpiderSpider(scrapy.Spider):
    name = 'qiancheng_spider'
    allowed_domains = ['51job.com']
    start_urls = [
        'https://search.51job.com/list/000000,000000,0000,00,9,99,%25E5%25A4%25A7%25E6%2595%25B0%25E6%258D%25AE,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=',
                  ]
    job_types = '大数据'
    def open_spider(self):
        self.job_types = ''

    def parse(self, response):
        page_num = response.xpath('//div[@class="p_in"]/ul/li[@class="on"]/text()').extract_first()
        target = response.url
        el_urls = response.xpath('//p[@class="t1 "]/span/a/@href').extract()
        for el_url in el_urls:
            yield scrapy.Request(url=el_url, callback=self.detail_parse, meta={'job_typer': self.job_types,'page_num': page_num} )
        next_page = response.xpath('//li[@class="bk"][2]/a/@href').extract_first()
        yield scrapy.Request(url=next_page, callback=self.parse,meta={'job_type':self.job_types})

    def detail_parse(self,response):
        item = JobscrawlerQianchengwuyouItem()
        item['job_name'] = response.xpath('//div[@class="cn"]/h1/text()').extract_first()  # 1招聘名称
        item['job_type'] = response.meta['job_typer']
        page_num = response.meta['page_num']
        print(item['job_type']+'第'+page_num+'页')
        job_info = response.xpath('//div[@class="bmsg job_msg inbox"]//*/text()').extract()  # 10职位信息 岗位职责
        for idx, job in enumerate(job_info):
            job_info[idx] = job.strip()
            job_info[idx] = job_info[idx].replace("\'\\r\'",'').replace("\'\\n\'", '').replace("\'\\t\'", '').replace("\'\\b\'", '')
            if len(job_info[idx]) == 0:
                job_info.remove(job_info[idx])
        job_info_text = ''.join([content.strip() for content in job_info if content])
        item['job_info'] = job_info_text
        salary = response.xpath('//div[@class="cn"]/strong/text()').extract_first()  # 4 薪资
        if salary == '':
            salary = '面议'
        if '天' in salary:
            salary =salary.replace('元/天','')
            salary = int(salary)*30
        if '千/月' in salary:
            salary = salary.replace('千/月','')
            salarys = salary.split('-')
            salary = np.mean(salarys)
        if '万/月' in salary:
            salarys=salary.replace('万/月','')
            salarys = salarys.split('-')
            if len(salarys)==2:
                pass
                print(salarys)
        if '万/年' in salary:
            salarys=salary.replace('万/月','')

        item['job_sal'] =salary
        job_benefit = response.xpath('//span[@class="sp4"]/text()').extract()  # 9 职位福利
        if len(job_benefit) ==0:
            job_benefit='无'
        item['job_benefit'] = job_benefit
        exp_requires = response.xpath('//div[@class="cn"]/p[@class="msg ltype"]/text()').extract() # 5 经验要求 任职资格
        item['exp_require'] = exp_requires[1].strip() # 6 工作精验
        xuelis = response.xpath('//p[@class="msg ltype"]/text()').extract()  # 7 学历要求
        item['edu_require'] = '无要求'
        for xueli in xuelis:
            if '本科' in xueli:
                item['edu_require'] ='本科'
            if '专科' in xueli:
                item['edu_require'] = '专科'
            if '大专' in xueli:
                item['edu_require'] = '大专'
            if '中专' in xueli:
                item['edu_require'] = '中专'
            if '研究生' in xueli:
                item['edu_require'] = '硕士'
            if '硕士' in xueli:
                item['edu_require'] = '硕士'
            if '博士' in xueli:
                item['edu_require'] = '博士'
            if '博士后' in xueli:
                item['edu_require'] = '博士后'
        item['company_name'] = response.xpath('//p[@class="cname"]/a[1]/@title').extract_first()  # 2公司名称
        msg_ltype_list = response.xpath('//p[@class="msg ltype"]/text()').extract()
        for msg in msg_ltype_list:
            if re.search('招', msg):
                item['emp_wanted_num'] = msg.split()[0] # 8 需要人数
        releast_time = response.xpath('//p[@class="msg ltype"]/text()').extract()[-1][0:-2].strip().replace('-','月')   # 5发布时间
        item['releast_time']=releast_time
        item['job_loc'] = response.xpath('//p[@class="msg ltype"]/text()').extract_first()[0:2]  # 3工作地点
        yield item
        return item
