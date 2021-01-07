import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import requests

picdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'pic')

# font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 13)
font = ImageFont.truetype(os.path.join(picdir, 'OpenSans-SemiBold.ttf'), 15)



class CovidStat:
    deltaSicked = ''

    def __init__(self, x, y, renderer, req_url):
        self.x = x
        self.y = y
        self.renderer = renderer
        self.req_url = req_url
        self.renderer.append(self)

        self.deltaSicked = self.getValue()

    def getValue(self):
        res = requests.get(self.req_url)
        if res.ok:
            today = res.json()[0]['sick']
            yesterday = res.json()[1]['sick']
            delta = int(today) - int(yesterday)
            print('covid '+str(delta))
        return delta

    def update(self):
        delta = self.getValue()
        if(self.deltaSicked != delta):
            print('set covid')
            self.deltaSicked = delta
            self.renderer.render()

    def draw(self):
        blankBlack = self.renderer.getBlankBlack()

        blackImage = Image.open(os.path.join(
            picdir, 'covid.bmp'))


        blankBlack.paste(blackImage, (self.x, self.y+4))

        drawblack = ImageDraw.Draw(blankBlack)
        drawblack.text((self.x + 20, self.y), '+'+str(
            self.deltaSicked) + '', font=font, fill=0)
