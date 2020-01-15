## Curiosity Timelapse Generator
#### Python script with CLI that scrapes images taken by the Curiosity rover's cameras and generates timelapses. Extracts image data from Nasa's Public Mars API.

#### Technologies:
- Pipenv (Python 3.6)
- FFmpeg
- Scrapy

#### Setup:
`
pipenv install
`
#### Usage:
##### Example:
`
pipenv run python manage.py 12-1-2019 12-20-2019 front
`

Positional arguments:
  - start_date : the start of the date range to scrape from
  - end_date : the end of the date range to scrape from
  - cams : which cameras to scrape from

Currently, cams can be:
 - front (front cameras)
 - rear (rear cameras)
 - lnav (left navcams)
 - rnav (right navcams)
