import os

ROOT_NASA_URL = 'https://mars.nasa.gov'
BASE_API_URL = 'https://mars.nasa.gov/api/v1/raw_image_items/?order=sol+asc%2Cinstrument_sort+desc%2Csample_type_sort+desc%2C+date_taken+asc&per_page=99999&page=0&condition_1=msl%3Amission&condition_2={start_date}%3Adate_taken%3Agte&condition_3={end_date}%3Adate_taken%3Alt&search={filter_str}&extended=full%3A%3Asample_type'
FFMPEG_COMMAND = 'ffmpeg -hide_banner -loglevel panic -f concat -safe 0 -i {} -filter:v setpts=5.5*PTS {}'
FONT_FILE = "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf"
CAMS = [
    'FHAZ_RIGHT_A',
    'FHAZ_LEFT_A',
    'FHAZ_RIGHT_B',
    'FHAZ_LEFT_B',
    'RHAZ_RIGHT_A',
    'RHAZ_LEFT_A',
    'RHAZ_RIGHT_B',
    'RHAZ_LEFT_B',
    'NAV_LEFT_A',
    'NAV_LEFT_B',
    'NAV_RIGHT_A',
    'NAV_RIGHT_B',
]
FRONT_CAMS = CAMS[:4]
REAR_CAMS = CAMS[4:8]
LEFT_NAV_CAMS = CAMS[8:10]
RIGHT_NAV_CAMS = CAMS[10:12]

CAM_MAP = {
    'front': FRONT_CAMS,
    'rear': FRONT_CAMS,
    'lnav': LEFT_NAV_CAMS,
    'rnav': RIGHT_NAV_CAMS
}

IMAGES_DIR = os.path.join(os.getcwd(), 'images')
VIDEOS_DIR = os.path.join(os.getcwd(), 'videos')
