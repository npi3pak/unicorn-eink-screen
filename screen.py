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
import argparse
from abc import ABC, abstractmethod
from decouple import config
from widgets.update_time import UpdateTime
from widgets.covid_stat import CovidStat
from widgets.funny_pic import FunnyPic
from widgets.temperature import Temperature

# get config vars from .env
API_URL_WEATHER = config('API_URL_WEATHER')
API_URL_COVID = config('API_URL_COVID')

run_loop = True
LOOP_SECONDS = 2
LOOP_HOURS = 1
blank_size_x = 218
blank_size_y = 105

logging.basicConfig(level=logging.DEBUG)

libdir = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'lib')

parser = argparse.ArgumentParser(description='eInk screen image processor')
parser.add_argument(
    '-t',
    '--target',
    type=str,
    default='screen',
    help='select render targer picture or screen (default: screen)'
)
args = parser.parse_args()
target = args.target


class Renderer():
    widgets = []

    def __init__(self, blank_size_x, blank_size_y, render_target='screen'):
        self.blank_size_x = blank_size_x
        self.blank_size_y = blank_size_y
        self.render_target = render_target

        if(self.render_target == 'screen'):
            if os.path.exists(libdir):
                sys.path.append(libdir)
                from waveshare_epd import epd2in13b_V3

                self.epd = epd2in13b_V3.EPD()
                logging.info("init and Clear")
                self.epd.init()
                self.epd.Clear()
                time.sleep(1)
                self.blank_size_y = self.epd.width
                self.blank_size_x = self.epd.height

        if(self.render_target == 'image'):
            self.blank_size_x = blank_size_x
            self.blank_size_y = blank_size_y

        self.createNewBlank()

    def createNewBlank(self):
        self.blankBlack = Image.new(
            '1', (self.blank_size_x, self.blank_size_y), 255)
        self.blankRed = Image.new(
            '1', (self.blank_size_x, self.blank_size_y), 255)

    def getBlankBlack(self):
        return self.blankBlack

    def getBlankRed(self):
        return self.blankRed

    def append(self, widget):
        self.widgets.append(widget)

    def render(self):
        self.createNewBlank()
        if(self.render_target == 'screen'):
            return self.renderToScreen()

        return self.renderToPic()

    def renderToPic(self):
        for w in self.widgets:
            w.draw()

        self.blankBlack.save("imgage.png", "PNG")

    def renderToScreen(self):
        for w in self.widgets:
            w.draw()

        self.epd.display(self.epd.getbuffer(self.blankBlack),
                         self.epd.getbuffer(self.blankRed))


def signal_handler(signal, frame):
    global run_loop
    run_loop = False


signal.signal(signal.SIGINT, signal_handler)

renderer = Renderer(blank_size_x, blank_size_y, target)

temperature = Temperature(20, 10, renderer, API_URL_WEATHER)
funnyPic = FunnyPic(140, 0, renderer)
updateTime = UpdateTime(100, 90, renderer)
covidStat = CovidStat(10, 78, renderer, API_URL_COVID)
renderer.render()

schedule.every(LOOP_SECONDS).seconds.do(temperature.update)
schedule.every(LOOP_HOURS).hour.do(covidStat.update)

while run_loop:
    schedule.run_pending()
    time.sleep(1)
