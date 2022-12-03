import scrapy
from scrapy.selector import Selector
import pathlib
import json
import os
import re
# import js2xml
# import lxml.etree
from inline_requests import inline_requests
import time
from scrapy.crawler import CrawlerProcess
import js2py
import pandas as pd

json_path = r"C:\Users\User\Desktop\jd_watch.json"
if os.path.exists(json_path):
    os.remove(json_path)

p = pathlib.PurePath(json_path)
uri = p.as_uri()

headers = {
    'authority': 'item.m.jd.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8,fa;q=0.7',
    'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
}
cookies = {
    'ip_cityCode': '19',
    'ipLoc-djd': '19_1601_3633_0'
}

cookies_list = {
    'shshshfpb': 'uPBXujcOiHB9k3uDVjWQjVQ',
    'shshshfpa': '0ac1498d-6a54-f8e4-bcd1-6fba8ee09067-1652508312',
    '__jdu': '16576212820221415266873',
    'areaId': '31',
    'ipLoc-djd': '31-4110-4122-0',
    'user-key': '171c53b5-80cb-46de-954c-6da70d1d9402',
    '__jdv': '122270672|direct|-|none|-|1667117262287',
    'visitkey': '51038773082734184',
    'cid': '9',
    'webp': '1',
    'sc_width': '1920',
    'deviceOS': '',
    'deviceOSVersion': '',
    'deviceName': 'Chrome',
    'retina': '0',
    '3AB9D23F7A4B3C9B': 'X322JTJZZU565IQRGJTDRSMXGMAQLBX2EZGZAVLXCU4CAHCJOEW4UZHISRITMRW3ES6LMUPRMWCZBRQGZNFSZ3KG2Q',
    'equipmentId': 'X322JTJZZU565IQRGJTDRSMXGMAQLBX2EZGZAVLXCU4CAHCJOEW4UZHISRITMRW3ES6LMUPRMWCZBRQGZNFSZ3KG2Q',
    'unpl': 'JF8EALBnNSttXRxXUB0KHBIUSV4AW1QKG0cKZ2MBXFsITVUDHQcfRUR7XlVdXhRLFx9uZxRXXVNLUw4aCisSFHteVV5dD0oTCmllNWRVUCVUSBtPVl8gSF1kX20ITBMFaGQFV1RbSlcGGwcbFhNMWl1YXzhKJwNpVwVVXFtJVAQYChkRFENdZG5cOEonAl8ma1RcWktWAh4EVhIXT1tTXV0LQhQCbGQFUV1cSFMCEgQZIhF7Xg',
    '_gia_s_local_fingerprint': '816c760ef8c0a696b269d71a8f050e38',
    'fingerprint': '816c760ef8c0a696b269d71a8f050e38',
    'deviceVersion': '107.0.0.0',
    'wxa_level': '1',
    'jxsid': '16682510773291101137',
    'jsavif': '1',
    'jsavif': '1',
    '__jdc': '122270672',
    'share_cpin': '',
    'share_open_id': '',
    'share_gpin': '',
    'shareChannel': '',
    'source_module': '',
    'erp': '',
    'appCode': 'ms0ca95114',
    'jxsid_s_t': '1668328037240',
    'jxsid_s_u': 'https%3A//wqs.jd.com/portal/wx/seckill_m/branddetail.shtml',
    'avif': '1',
    '__jda': '122270672.16576212820221415266873.1657621282.1668327886.1668330569.95',
    'wqmnx1': 'MDEyNjM2M3B0ai9jMjdoNTczby9XczBpeHBiMygsICltLiBpMzNmZjI1VkVJVShS',
    '__wga': '1668330594420.1668327185960.1668264918261.1667121003449.7.22',
    'PPRD_P': 'UUID.16576212820221415266873-LOGID.1668330594429.1378728676',
    'shshshfp': '35c238a2b6e77460e7d29767544c1346',
    'wlfstk_smdl': 'ez1fgnhx8yabb79imjj89mpdrzcuj1yx',
    '__jdb': '122270672.4.16576212820221415266873|95.1668330569',
    'shshshsID': '47fffd64d26e1a3880e82b9604a12c4f_12_1668333478217',
}

headers_list = {
    'authority': 'list.jd.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8,fa;q=0.7',
    'cache-control': 'max-age=0',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'shshshfpb=uPBXujcOiHB9k3uDVjWQjVQ; shshshfpa=0ac1498d-6a54-f8e4-bcd1-6fba8ee09067-1652508312; __jdu=16576212820221415266873; areaId=31; ipLoc-djd=31-4110-4122-0; user-key=171c53b5-80cb-46de-954c-6da70d1d9402; __jdv=122270672|direct|-|none|-|1667117262287; visitkey=51038773082734184; cid=9; webp=1; sc_width=1920; deviceOS=; deviceOSVersion=; deviceName=Chrome; retina=0; 3AB9D23F7A4B3C9B=X322JTJZZU565IQRGJTDRSMXGMAQLBX2EZGZAVLXCU4CAHCJOEW4UZHISRITMRW3ES6LMUPRMWCZBRQGZNFSZ3KG2Q; equipmentId=X322JTJZZU565IQRGJTDRSMXGMAQLBX2EZGZAVLXCU4CAHCJOEW4UZHISRITMRW3ES6LMUPRMWCZBRQGZNFSZ3KG2Q; unpl=JF8EALBnNSttXRxXUB0KHBIUSV4AW1QKG0cKZ2MBXFsITVUDHQcfRUR7XlVdXhRLFx9uZxRXXVNLUw4aCisSFHteVV5dD0oTCmllNWRVUCVUSBtPVl8gSF1kX20ITBMFaGQFV1RbSlcGGwcbFhNMWl1YXzhKJwNpVwVVXFtJVAQYChkRFENdZG5cOEonAl8ma1RcWktWAh4EVhIXT1tTXV0LQhQCbGQFUV1cSFMCEgQZIhF7Xg; _gia_s_local_fingerprint=816c760ef8c0a696b269d71a8f050e38; fingerprint=816c760ef8c0a696b269d71a8f050e38; deviceVersion=107.0.0.0; wxa_level=1; jxsid=16682510773291101137; jsavif=1; jsavif=1; __jdc=122270672; share_cpin=; share_open_id=; share_gpin=; shareChannel=; source_module=; erp=; appCode=ms0ca95114; jxsid_s_t=1668328037240; jxsid_s_u=https%3A//wqs.jd.com/portal/wx/seckill_m/branddetail.shtml; avif=1; __jda=122270672.16576212820221415266873.1657621282.1668327886.1668330569.95; wqmnx1=MDEyNjM2M3B0ai9jMjdoNTczby9XczBpeHBiMygsICltLiBpMzNmZjI1VkVJVShS; __wga=1668330594420.1668327185960.1668264918261.1667121003449.7.22; PPRD_P=UUID.16576212820221415266873-LOGID.1668330594429.1378728676; shshshfp=35c238a2b6e77460e7d29767544c1346; wlfstk_smdl=ez1fgnhx8yabb79imjj89mpdrzcuj1yx; __jdb=122270672.4.16576212820221415266873|95.1668330569; shshshsID=47fffd64d26e1a3880e82b9604a12c4f_12_1668333478217',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}
start_url = 'https://list.jd.com/list.html?cat=5025,5026,13669&ev=exbrand_卡西欧（CASIO）||西铁城（CITIZEN）||精工（SEIKO）||东方（ORIENT）||天梭（TISSOT）||化石（Fossil）||斯沃琪（Swatch）^exprice_100-500^3497_70696^&psort=3&click=0'
class JdCrawlUrlMobile(scrapy.Spider):
    name = 'JdCrawlUrlMobile'
    custom_settings = {
        "FEEDS": {uri: {"format": "json"}},
        # "AUTOTHROTTLE_ENABLED" : True,
        # "AUTOTHROTTLE_START_DELAY" : 3,
        # "AUTOTHROTTLE_MAX_DELAY" : 10,
        # "DOWNLOAD_DELAY" : 3,
        # 'CONCURRENT_REQUESTS':4,
        # "HTTPCACHE_ENABLED" : True,
    }

    def start_requests(self):
        yield scrapy.Request(url=start_url,callback=self.parse,headers=headers_list,cookies=cookies_list)

    def parse(self, response):
        products = response.css('#J_goodsList li[data-sku] ::attr(data-sku)').getall()
        products = list(set(products))
        for id in products:
            jd_mobile_url = f"https://item.m.jd.com/product/{id}.html"
            yield scrapy.Request(jd_mobile_url,callback=self.product,headers=headers,cookies=cookies)

        for i in range(2,7):
            yield scrapy.Request(url=f'{start_url}&page={i}',callback=self.parse,headers=headers_list,cookies=cookies_list)

    @inline_requests
    def product(self, response):
        html = response.text
        url = response.url
        name = response.css('title ::text').get()
        scripts = response.css('*::text').getall()
        for i in scripts:
            if 'window._itemOnly = ({' in i:
                product_script = i.strip().split(';')[0]
                product_json = js2py.eval_js(product_script).to_dict()
                variation = product_json['item']['Color'][0]
                keys = list(product_json['item']['expandAttrDesc'].keys())
                values = [", ".join(product_json['item']['expandAttrDesc'][i]) for i in keys]
                key_values_dict = dict(zip(keys, values))
                brand = product_json['item']['brandName']
                sku = url.split('/')[4].replace('.html', '')
                main_sku = product_json['item']['description'].replace('d', '')
                ############################################description_images##############################################
                description_url = f'https://cd.jd.com/description/channel?skuId={sku}&mainSkuId={main_sku}'
                description_response = yield scrapy.Request(description_url, headers=headers)
                description_response = description_response.json()
                description_images_content = description_response['content']
                description_images = re.findall('(//img\d*.360buyimg.com/\w*/jfs/t1/\d*/\d*/\d*/\d*/\S*.jpg)',
                                                description_images_content, flags=re.DOTALL)
                description_images = [f'https:{i.replace(".avif", "")}' for i in description_images]
                images = product_json['item']['image']
                main_images = [
                    f"https://m.360buyimg.com/mobilecms{i.replace('jfs/', '/s1200x1200_jfs/').replace('/s54x54_jfs/', '/s1200x1200_jfs/')}"
                    for i in images]
                ############################################bullet##########################################################
                try:
                    response_key_values = yield scrapy.Request(f'https://yx.3.cn/service/info.action?k=g{sku}',
                                                               headers=headers)
                    response_key_values = response_key_values.text
                    bullet_df = pd.read_html(response_key_values)[0]
                    bullet_df = bullet_df.dropna(axis=0, how='all')
                    bullet_keys = bullet_df[bullet_df.columns[0]].values.tolist()
                    bullet_values = bullet_df[bullet_df.columns[1]].values.tolist()
                except:
                    bullet_keys = []
                    bullet_values = []

                bullet_keys.append('sku ')
                bullet_values.append(sku)
                ############################################price############################################################
                try:
                    discounted_price = float(re.findall('p":"(\d*\.\d*)', html, flags=re.DOTALL)[0])
                    original_price = float(re.findall('op":"(\d*\.\d)*', html, flags=re.DOTALL)[0])
                    stockstate = int(re.findall('StockState":(\d*)', html, flags=re.DOTALL)[0])
                except:
                    discounted_price = 0
                    original_price = 0
                    stockstate = 34

                if stockstate == 34:
                    stock = 0
                else:
                    stock = 5

                if original_price == discounted_price:
                    discounted_price = 0

                if original_price == 0:
                    stock = 0
                    discounted_price = 0

                variations = product_json['item']['ColorSize']
                variations = [i['SkuId'] for i in variations]
                ##########################################################################################################
                yield {
                    'url': url,
                    'name': name,
                    'Variation': variation,
                    'sku': sku,
                    'main_sku': main_sku,
                    'color': variation,
                    'Brand': brand,
                    "price": original_price,
                    "discounted_price": discounted_price,
                    "stock": stock,
                    'product_images': main_images,
                    'description_images': description_images,
                    'key_values': key_values_dict,
                    'bullet_keys': bullet_keys,
                    'bullet_values': bullet_values,
                }

                for id in variations:
                    jd_mobile_url = f"https://item.m.jd.com/product/{id}.html"
                    yield scrapy.Request(jd_mobile_url, callback=self.product)

process = CrawlerProcess()
process.crawl(JdCrawlUrlMobile)
process.start()
