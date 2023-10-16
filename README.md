## Curiosity Timelapse Generator
#### A Python script with CLI that scrapes curiosity images from Nasa's public Mars API and generates timelapses as MP4.

<p align="center">
  <img src="sample.gif?raw=true" width="320px">
</p>

#### Prerequisites:
- Pipenv (Python 3.6)
- FFmpeg

#### Setup:
`
pipenv install
`
#### Example Usage:
`
pipenv run python manage.py 12-1-2019 12-20-2019 front
`

Positional arguments:
  - start_date (dd-mm-yyyy) : the start of the date range to scrape from
  - end_date (dd-mm-yyyy) : the end of the date range to scrape from
  - cams {front|rear|lnav|rnav} : which cameras to scrape from
  - -s (optional) : only scrape images / don't generate video

Currently, cams can be:
 - front (front cameras)
 - rear (rear cameras)
 - lnav (left navcams)
 - rnav (right navcams)
