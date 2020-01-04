# -*- coding: utf-8 -*-
import scrapy, json
from scrapy_base.items import ImageItem

class ImageSpider(scrapy.Spider):
    name = 'image'
    allowed_domains = ['mars.jpl.nasa.gov']

    def __init__(self, *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs.get('start_url')]
        self.filters = kwargs.get('filters')

    def parse(self, response):
        json_resp = json.loads(response.body)
        for image_json in json_resp['items']:
            if 'url' in image_json:
                if self.filters:
                    if image_json['instrument'] not in self.filters:
                        continue

                yield ImageItem(
                    id=image_json['imageid'],
                    url=image_json['url'])
