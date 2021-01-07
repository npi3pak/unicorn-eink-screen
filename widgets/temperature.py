import os
import logging
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import requests

picdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'pic')

font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 58)
# font = ImageFont.truetype(os.path.join(picdir, 'OpenSans-Regular.ttf'), 50)



class Temperature():
    currentTempature = ''

    def __init__(self, x, y, renderer, req_url):
        self.x = x
        self.y = y
        self.renderer = renderer
        self.req_url = req_url
        self.renderer.append(self)

        self.currentTempature = self.getValue()

    def getValue(self):
        res = requests.get(self.req_url)
        if res.ok:
            temp_k = res.json()['main']['temp']
            temp_c = str(round(temp_k - 273))
            logging.info("temp = " + temp_c)
            return temp_c

    def update(self):
        newTemp = self.getValue()
        if(self.currentTempature != newTemp):
            print('set temp')
            self.currentTempature = newTemp
            self.renderer.render()

    def draw(self):
        blankBlack = self.renderer.getBlankBlack()
        drawblack = ImageDraw.Draw(blankBlack)
        drawblack.text((self.x, self.y), self.currentTempature +
                       ' °', font=font, fill=0)
        # drawblack.text((self.x, self.y), '-20 °', font=font, fill=0)
