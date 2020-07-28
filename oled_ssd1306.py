#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import time


class OledSsd1306:

	def __init__(self, reset):
		self.reset = reset
		self.disp = Adafruit_SSD1306.SSD1306_128_32(rst=self.reset)

	def initialize(self):
		self.fontsize = 12
		self.fontstyle = 'fonts-japanese-gothic.ttf'
		self.disp.begin()
		self.clear()
		self.image = Image.new('1', (self.disp.width, self.disp.height))
		self.draw = ImageDraw.Draw(self.image)
		self.font = ImageFont.truetype(self.fontstyle, self.fontsize)

	def clear(self):
		self.disp.clear()
		self.disp.display()
		time.sleep(0.3)

	def drawtext(self, x, y, text):
		self.draw.rectangle(
			(0, 0, self.disp.width, self.disp.height), outline=0, fill=0)
		self.draw.text((x, y), text, font=self.font, fill=255)
		self.disp.image(self.image)
		self.disp.display()
		time.sleep(0.3)
