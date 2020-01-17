import os, logging, requests, hashlib, subprocess
import argparse, progressbar, settings, urllib.request
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import SignalManager, dispatcher
from scrapy_base.spiders.image import ImageSpider
from utils import ext_from_url

class CuriosityScrapy:
    def __init__(self):
        self.crawler_results = []
        dispatcher.connect(self.process_item, signal=signals.item_passed)

    def process_item(self, signal, sender, item, response, spider):
        '''  Item scraped event handler, allows for collecting scraped results in a list.'''
        self.crawler_results.append(item)

    def crawl(self, start_date, end_date, cams, filters=[]):
        ''' Scrapes the images from the given date range and returns download links.
            Cams is either FRONT_CAMS, REAR_CAMS, OR NAV_CAMS from settings.py.
            If filters is non-empty, only scrape images from that list of cam codes.
        '''
        self.crawler_results = []
        start_url = settings.BASE_API_URL.format(
            start_date=start_date,
            end_date=end_date,
            filter_str='%7C'.join(cams)
        )
        process = CrawlerProcess(get_project_settings())
        process.crawl(ImageSpider, start_url=start_url, filters=filters)
        process.start()
        return self.crawler_results

    def run(self, start_date, end_date, cams, scrape_only):
        vid_name = ''.join([start_date, end_date, ''.join(cams)])
        vid_hash = hashlib.md5(vid_name.encode('utf-8')).hexdigest()
        vid_name = '{}.mp4'.format(vid_hash)
        list_file = '{}.txt'.format(vid_hash)
        abs_vid_path = os.path.join(settings.VIDEOS_DIR, vid_name)
        abs_list_file = os.path.join(settings.VIDEOS_DIR, list_file)

        images = self.crawl(start_date, end_date, cams)
        num_images = len(images)
        logging.info("Nasa API returned {} image links".format(num_images))
        if num_images == 0:
            return "OK"

        # Download the images we need that we don't already have
        image_paths = []
        downloaded_images = os.listdir(settings.IMAGES_DIR)
        logging.info("Downloading {} images to {}".format(len(images), settings.IMAGES_DIR))
        with progressbar.ProgressBar(max_value=len(images)) as bar:
            i = 0
            for image in images:
                filetype = ext_from_url(image['url'])
                filename = image['id'] + filetype
                abs_img_path = os.path.join(settings.IMAGES_DIR, filename)

                if filename not in downloaded_images:
                    urllib.request.urlretrieve(image['url'], abs_img_path)
                image_paths.append(abs_img_path)
                i += 1
                bar.update(i)

        if scrape_only == False:
            # Need to write a text file containing a list of input files for FFmpeg concat
            with open(abs_list_file, 'w') as list_file_out:
                list_file_out.writelines(["file '{}'\n".format(path) for path in image_paths])
            os.chmod(abs_list_file, 0o775)

            logging.info("Compiling video...")
            subprocess.call(settings.FFMPEG_COMMAND.format(abs_list_file, abs_vid_path), shell=True)
            logging.info("Saved video as {}".format(abs_vid_path))

parser = argparse.ArgumentParser(description='Curiosity image scraper and timelapse generator')
parser.add_argument('start_date', action="store")
parser.add_argument('end_date', action="store")
parser.add_argument('cams', action="store")
parser.add_argument('-s', action="store_true", default=False)

args = parser.parse_args()
args = [args.start_date, args.end_date, args.cams, args.s]
args[2] = settings.CAM_MAP[args[2]]
curiosity = CuriosityScrapy()
curiosity.run(*args)
