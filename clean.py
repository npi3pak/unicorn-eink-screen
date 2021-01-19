#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import signal
import sys
import time

import logging
import time
from PIL import Image, ImageDraw, ImageFont
import traceback
from datetime import datetime
import schedule
import threading

logging.basicConfig(level=logging.DEBUG)

libdir = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'lib')

picdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'pic')


if os.path.exists(libdir):
    sys.path.append(libdir)
    from waveshare_epd import epd2in13b_V3

epd = epd2in13b_V3.EPD()
logging.info("init and Clear")
epd.init()
epd.Clear()
time.sleep(1)
blank_size_y = epd.width
blank_size_x = epd.height

blankBlack = Image.new('1', (blank_size_x, blank_size_y), 255)
blankRed = Image.new('1', (blank_size_x, blank_size_y), 255)

blackImage = Image.open(os.path.join(picdir, 'blackbox.bmp'))
blankBlack.paste(blackImage, (0, 0))
# redImage = Image.open(os.path.join(picdir, 'blackbox.bmp'))
# blankRed.paste(redImage, (0, 0))

epd.display(epd.getbuffer(blankBlack), epd.getbuffer(blankRed))
