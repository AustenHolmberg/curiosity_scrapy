import os, requests, hashlib, ffmpy, settings, urllib.request
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import SignalManager
from scrapy_base.spiders.image import ImageSpider

results = []
class ImagePipeline:
    def process_item(self, item, spider):
        results.append(item)

proj_settings = get_project_settings()
proj_settings['ITEM_PIPELINES'] = {'__main__.ImagePipeline': 1}

def scrape_date_range(start_date, end_date, cams, filters=[]):
    ''' Scrapes the images from the given date range and returns download links.
        Cams is either FRONT_CAMS, REAR_CAMS, OR NAV_CAMS from settings.py.
        If filters is non-empty, only scrape images from that list of cam codes.
    '''
    global results
    results = []
    start_url = settings.BASE_API_URL.format(
        start_date=start_date,
        end_date=end_date,
        filter_str='%7C'.join(cams)
    )
    process = CrawlerProcess(proj_settings)
    process.crawl(ImageSpider, start_url=start_url, filters=filters)
    process.start()
    return results

def curiosity_scrapy():
    options = ['2019-12-01', '2019-12-05', settings.FRONT_CAMS, ['FHAZ_RIGHT_B']]
    img_dir = ''.join([options[0], options[1], ''.join(options[2]), ''.join(options[3])])
    img_dir = hashlib.md5(img_dir.encode('utf-8')).hexdigest()
    abs_img_dir = os.path.join(settings.IMG_DIR, img_dir)
    if not os.path.exists(abs_img_dir):
        os.mkdir(abs_img_dir)

    images = scrape_date_range(*options)
    existing_images = os.listdir(settings.IMG_DIR)
    for image in images:
        if image['id'] not in existing_images:
            urllib.request.urlretrieve(image['link'], os.path.join(abs_img_dir, image['id'] + '.jpg'))

    ff = ffmpy.FFmpeg(
        inputs={abs_img_dir+'/*.jpg': None},
        outputs={'output.mp4': '-pattern_type glob'}
    )
    ff.run()

curiosity_scrapy()
