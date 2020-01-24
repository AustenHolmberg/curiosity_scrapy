import argparse, settings
from scraper import CuriosityScrapy

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
