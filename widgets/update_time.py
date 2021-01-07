import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

picdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'pic')
font10 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 10)

class UpdateTime:
    def __init__(self, x, y, renderer):
        self.x = x
        self.y = y
        self.renderer = renderer
        self.renderer.append(self)

    def draw(self):
        blankBlack = self.renderer.getBlankBlack()
        drawblack = ImageDraw.Draw(blankBlack)
        drawblack.text((self.x, self.y), datetime.now().strftime(
            '%H:%M:%S'), font=font10, fill=0)
