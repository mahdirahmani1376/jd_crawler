import os
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
from PIL import Image
from scrapy.exporters import JsonItemExporter

save_path = r"C:\Users\User\Desktop\Defacto\feature_options"


class Per_category_name_JsonExportPipeline:
    """Distribute items across multiple Json files according to their 'category_name' field"""

    def open_spider(self, spider):
        self.category_name_to_exporter = {}

    def close_spider(self, spider):
        for exporter, Json_file in self.category_name_to_exporter.values():
            exporter.finish_exporting()
            Json_file.close()

    def _exporter_for_item(self, item):
        adapter = ItemAdapter(item)
        category_name = adapter["category_name"]
        if category_name not in self.category_name_to_exporter:
            Json_file = open(os.path.join(save_path,f'{category_name}.json'), 'wb')
            exporter = JsonItemExporter(Json_file)
            exporter.start_exporting()
            self.category_name_to_exporter[category_name] = (exporter, Json_file)

        return self.category_name_to_exporter[category_name][0]

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item

class DefactoJsonExportFeatures:
    """Distribute items across multiple Json files according to their 'category_name' field"""

    def open_spider(self, spider):
        self.category_name_to_exporter = {}

    def close_spider(self, spider):
        for exporter, Json_file in self.category_name_to_exporter.values():
            exporter.finish_exporting()
            Json_file.close()

    def _exporter_for_item(self, item):
        adapter = ItemAdapter(item)
        category_name = adapter["defacto_category"]
        # base_category = adapter['base_category']
        # json_path = os.path.join(save_path, base_category)
        # if not os.path.exists(json_path):
        #     os.makedirs(json_path)
        if category_name not in self.category_name_to_exporter:
            # Json_file = open(os.path.join(save_path,base_category,f'{category_name}.json'), 'wb')
            Json_file = open(os.path.join(save_path,f'{category_name}.json'), 'wb')
            exporter = JsonItemExporter(Json_file)
            exporter.start_exporting()
            self.category_name_to_exporter[category_name] = (exporter, Json_file)

        return self.category_name_to_exporter[category_name][0]

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item

class CustomImageNamePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *,item=None):
        return '{}/{}/{}.jpg'.format(item["excel_name"],item["url_index"],item['number'])

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url)

    def item_completed(self, results, item, info):
        for result, image_info in results:
            if result:
                image_path = image_info['path']
                img = Image.open(image_path)
                # resized_image = img.resize((1200, 1200), Image.LANCZOS)
                # resized_image.save(image_path)
                img.save(image_path)
        return item

class CustomImageNamePipelineOneExcell(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *,item=None):
        # if item['extension'] == 'webp':
        #     return f'{item["url_index"]}/{item["number"]}.webp'
        # else:
        return f'{item["url_index"]}/{item["number"]}.jpg'

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url)

    def item_completed(self, results, item, info):
        for result, image_info in results:
            if result:
                image_path = image_info['path']
                img = Image.open(image_path)
        #         resized_image = img.resize((1200, 1200), Image.LANCZOS)
                img.save(image_path)
        return item

class JDImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *,item=None):

        return f'{item["excel_name"]}/{item["sku"]}/{item["folder_source"]}/{item["number"]}.jpg'

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url)

    def item_completed(self, results, item, info):
        for result, image_info in results:
            if result:
                image_path = image_info['path']
                img = Image.open(image_path)
        #         resized_image = img.resize((1200, 1200), Image.LANCZOS)
                img.save(image_path)
        return item

class JdUniqueImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *,item=None):

        if item["folder_source"] == 'description_images':
            return f'{item["excel_name"]}/{item["main_sku"]}/{item["folder_source"]}/{item["number"]}.jpg'

        elif item["folder_source"] == 'main_images':
            if item['type'] == 'product_images':
                return f'{item["excel_name"]}/{item["main_sku"]}/{item["folder_source"]}/product_images/{item["number"]}.jpg'

            if item['type'] == 'unique_images':
                return f'{item["excel_name"]}/{item["main_sku"]}/{item["folder_source"]}/{item["sku"]}/{item["number"]}.jpg'

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url)

    def item_completed(self, results, item, info):
        for result, image_info in results:
            if result:
                image_path = image_info['path']
                img = Image.open(image_path)
        #         resized_image = img.resize((1200, 1200), Image.LANCZOS)
                img.save(image_path)
        return item

class KotonImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *,item=None):

        return f'{item["excel_name"]}/{item["sku"]}/main_images/{item["number"]}.jpg'
        # return f'{item["photo_id"]}/{item["number"]}.jpg'

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url)

    def item_completed(self, results, item, info):
        background_image = Image.open(r"C:\Users\User\Desktop\sample_grey.jpg")
        for result, image_info in results:
            if result:
                image_path = image_info['path']
                image = Image.open(image_path)
                image.thumbnail((1200, 1200))

                image_2_height = image.size[1]
                image_2_weight = image.size[0]

                image_2_height_location = int((1200 - image_2_height) / 2)
                image_2_weight_location = int((1200 - image_2_weight) / 2)

                background_image.paste(image, (image_2_weight_location, image_2_height_location))

                background_image.save(image_path)
        return item

class JDDescriptionImages(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *,item=None):

        return f'{item["excel_name"]}/{item["main_sku"]}/{item["number"]}.jpg'

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url)

    def item_completed(self, results, item, info):
        for result, image_info in results:
            if result:
                image_path = image_info['path']
                img = Image.open(image_path)
        #         resized_image = img.resize((1200, 1200), Image.LANCZOS)
                img.save(image_path)
        return item

class DefactoImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *,item=None):

        return f'{item["excel_name"]}/{item["photo_id"]}/main_images/{item["number"]}.jpg'

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url)

    def item_completed(self, results, item, info):
        background_image = Image.open(r"C:\Users\User\Desktop\sample_grey.jpg")
        for result, image_info in results:
            if result:
                image_path = image_info['path']
                image = Image.open(image_path)
                image.thumbnail((1200, 1200))

                image_2_height = image.size[1]
                image_2_weight = image.size[0]

                image_2_height_location = int((1200 - image_2_height) / 2)
                image_2_weight_location = int((1200 - image_2_weight) / 2)

                background_image.paste(image, (image_2_weight_location, image_2_height_location))

                background_image.save(image_path)
        return item
