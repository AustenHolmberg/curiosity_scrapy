## Curiosity Timelapse Generator
#### Every day, the Curiosity rover on Mars sends back images of what it sees. 
#### This is a Python script with CLI that selectively scrapes the images from Nasa's public Mars API and generates timelapses.

+<img src="sample.gif?raw=true" width="200px">

#### Technologies:
- Pipenv (Python 3.6)
- FFmpeg
- Scrapy

#### Setup:
`
pipenv install
`
#### Example Usage:
`
pipenv run python manage.py 12-1-2019 12-20-2019 front
`

Positional arguments:
  - start_date : the start of the date range to scrape from
  - end_date : the end of the date range to scrape from
  - cams : which cameras to scrape from
  -s (optional) : only scrape images / don't generate video

Currently, cams can be:
 - front (front cameras)
 - rear (rear cameras)
 - lnav (left navcams)
 - rnav (right navcams)
