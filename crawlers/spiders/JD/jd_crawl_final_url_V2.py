import scrapy
from scrapy.selector import Selector
import pathlib
import json
import os
import re
import js2xml
import lxml.etree
from inline_requests import inline_requests
import time

json_path = r"C:\Users\User\Desktop\jd_hari_clipper.json"
if os.path.exists(json_path):
    os.remove(json_path)

p = pathlib.PurePath(json_path)
uri = p.as_uri()

start_url = 'https://list.jd.com/list.html?cat=737%2C1276%2C1287&ev=exprice_0-350%5E&psort=3&click=0'
class JdCrawlUrl(scrapy.Spider):
    name = 'JdCrawlUrl'
    custom_settings = {
        "FEEDS": {uri: {"format": "json"}},
        # "AUTOTHROTTLE_ENABLED" : True,
        # "AUTOTHROTTLE_START_DELAY" : 3,
        # "AUTOTHROTTLE_MAX_DELAY" : 10,
        # "DOWNLOAD_DELAY" : 3,
        # 'CONCURRENT_REQUESTS':4,
        "HTTPCACHE_ENABLED" : True,
    }

    def start_requests(self):
        yield scrapy.Request(url=start_url,callback=self.parse,)

    def parse(self, response):
        products = response.css('div.p-name.p-name-type-3 a ::attr(href)').getall()
        products = list(set(products))
        for url in products:
            yield response.follow(
                url, callback=self.product,
                                  )


        for i in range(2, 10):
            yield response.follow(
                url=f'{start_url}&page={i}',
                callback=self.parse
                )

    @inline_requests
    def product(self, response):
        url = response.url
        name = response.css('div.p-name ::text').getall()
        name = " ".join(name)
        name = " ".join(name.split())
        main_sku = re.search("mainSkuId:'(\d*)'", response.text, flags=re.DOTALL).groups()[0]
        if response.url:
            sku = re.search('https://item.jd.com/(.*).html', response.url).groups()[0]
        key_values = response.css('div.p-parameter  ul.parameter2.p-parameter-list  li ::text').getall()
        keys = []
        values = []
        for i in key_values:
            if ('：') in i:
                keys.append(i.split('：')[0])
                values.append(i.split('：')[1])
        key_values_dict = dict(zip(keys, values))
        brand = response.css('ul#parameter-brand > li ::attr(title)').get()
        product_images = response.css('div.spec-list ul li img ::attr(src)').getall()
        product_images = [i.replace('/jfs/', '/s1200x1200_jfs/').replace('/s54x54_jfs/', '/s1200x1200_jfs/') for i in
                          product_images]
        product_images = ['https:' + i for i in product_images]
        product_images = [i.replace('.avif', '') for i in product_images]
        product_short_name = response.css('.selected i ::text').get()
        bullet_keys = response.css('div.Ptable dl.clearfix dt ::text').getall()
        bullet_values = response.css('div.Ptable dl.clearfix dd ::text').getall()
        bullet_values = [i for i in bullet_values if not i.isspace()]
        package_list_keys = response.css('div.package-list > h3 ::text').get()
        package_list_values = response.css('div.package-list > p ::text').get()
        bullet_keys.append(package_list_keys)
        bullet_values.append(package_list_values)
        ##############################################################################################################
        urls = response.css('#choose-attrs div.dd div.item ::attr(data-sku)').getall()
        urls = ['https://item.jd.com/' + str(i) + '.html' for i in urls]
        group_id = urls.copy()
        group_id.append(response.url)
        group_id = list(set(group_id))
        group_id = list(map(lambda x: x.replace('https://item.jd.com/',"").replace(".html","").replace('https://npcitem.jd.hk/',''),group_id))
        sum_group_id = 0
        for i in group_id:
            try:
                sum_group_id += int(i)
            except:
                sum_group_id +=1
        set_1 = set([response.url])
        set_2 = set(urls)
        diff = list(set_2.difference(set_1))

        ##############################################################################################################
        # price_url = f'https://item-soa.jd.com/getWareBusiness?skuId={sku}&area=19_1601_3633_0'
        # price_response = yield scrapy.Request(price_url)
        # price_json = json.loads(price_response.text)
        # original_price = price_json['price']['op']
        # discounted_price = price_json['price']['p']
        # stock = price_json['stockInfo']['isStock']
        # if original_price == discounted_price:
        #     discounted_price = 0
        ##############################################################################################################
        description_url = f'https://cd.jd.com/description/channel?skuId={sku}&mainSkuId={main_sku}&charset=utf-8&cdn=2&callback=showdesc'
        description_response = yield scrapy.Request(description_url)
        description_images = re.findall('(//img\d*.360buyimg.com/\w*/jfs/t1/\d*/\d*/\d*/\d*/\S*.jpg)',description_response.text, flags=re.DOTALL)
        description_images = [f'https:{i.replace(".avif", "")}' for i in description_images]
        ##############################################################################################################


        yield {
            'url': url,
            'name': name,
            'Variation': product_short_name,
            'sku': sku,
            'jd_group_id': sum_group_id,
            # "price": original_price,
            # "discounted_price": discounted_price,
            # "stock": stock,
            'Brand': brand,
            'product_images': product_images,
            'description_images': description_images,
            'key_values': key_values_dict,
            'bullet_keys':bullet_keys,
            'bullet_values': bullet_values,
        }

        for url in diff:
            yield scrapy.Request(url, callback=self.product)


