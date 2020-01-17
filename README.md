## Curiosity Timelapse Generator
#### Python script with CLI that scrapes images taken by the Curiosity rover and generates timelapses. Extracts image data from Nasa's Public Mars API.

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
  - start_date (yy-mm-dddd) : the start of the date range to scrape from
  - end_date (yy-mm-dddd) : the end of the date range to scrape from
  - cams : which cameras to scrape from
  - -s (optional) : only scrape images / don't generate video

Currently, cams can be:
 - front (front cameras)
 - rear (rear cameras)
 - lnav (left navcams)
 - rnav (right navcams)
