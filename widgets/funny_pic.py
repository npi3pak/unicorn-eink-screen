import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

picdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'pic')



class FunnyPic:
    def __init__(self, x, y, renderer):
        self.x = x
        self.y = y
        self.renderer = renderer
        self.renderer.append(self)

    def draw(self):
        blankBlack = self.renderer.getBlankBlack()
        blankRed = self.renderer.getBlankRed()
        blackImage = Image.open(os.path.join(picdir, 'unicorn.png'))
        redImage = Image.open(os.path.join(picdir, 'unicornblood2.png'))
        blankBlack.paste(blackImage, (self.x, self.y))
        blankRed.paste(redImage, (self.x, self.y))
