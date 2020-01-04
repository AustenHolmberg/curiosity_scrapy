import os, requests, hashlib, subprocess, settings, urllib.request
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import SignalManager
from scrapy_base.spiders.image import ImageSpider
from utils import ext_from_url

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
    options = ['2019-12-10', '2019-12-31', settings.LEFT_NAV_CAMS, []]

    for DIR in [settings.IMAGES_DIR, settings.VIDEOS_DIR]:
        if not os.path.exists(DIR):
            os.mkdir(DIR)

    vid_name = ''.join([options[0], options[1], ''.join(options[2]), ''.join(options[3])])
    vid_hash = hashlib.md5(vid_name.encode('utf-8')).hexdigest()
    vid_name = vid_hash+'.mp4'
    list_file = vid_hash+'.txt'
    abs_vid_path = os.path.join(settings.VIDEOS_DIR, vid_name)
    abs_list_file = os.path.join(settings.VIDEOS_DIR, list_file)

    images = scrape_date_range(*options)
    if len(images) == 0:
        return "API gave no images"

    downloaded_images = os.listdir(settings.IMAGES_DIR)
    
    print(str("{} total images".format(len(images))))
    image_paths = []
    for image in images:
        filetype = ext_from_url(image['url'])
        filename = image['id'] + filetype
        abs_img_path = os.path.join(settings.IMAGES_DIR, filename)

        # Download the image if we haven't already done so.
        if filename not in downloaded_images:
            urllib.request.urlretrieve(image['url'], abs_img_path)
        image_paths.append(abs_img_path)

    with open(abs_list_file, 'w') as list_file_out:
        list_file_out.writelines(["file '{}'\n".format(path) for path in image_paths])
    os.chmod(abs_list_file, 0o775)

    subprocess.call(settings.FFMPEG_COMMAND.format(abs_list_file, abs_vid_path), shell=True)
    return "OK"

print(curiosity_scrapy())
