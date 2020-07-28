#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
import signal
import sys
import time
import threading
import subprocess

import logging
formatter = '%(asctime)s %(name)s %(levelname)s : %(message)s'
logging.basicConfig(filename='app.log', format=formatter, level=logging.INFO)
logger = logging.getLogger(__name__)

import RPi.GPIO as GPIO
pin = 18

from oled_ssd1306 import OledSsd1306
rst = None


def signal_handler(sig, frame):
	global th, tt
	global tt_quit, th_quit

	logger.info('signal_handler')
	GPIO.cleanup()
	if tt.isAlive():
		tt_quit = True
		tt.join()
	if th.isAlive():
		th_quit = True
		th.join()
	sys.exit(0)


def obtain_temp_worker():
	global obtain_temp_period
	global temp
	global tt_quit

	logger.info('obtain_temp_worker start')
	tt_quit = False
	while not tt_quit:
		t1 = time.time_ns()
		cmd = "python3 thermo.py | awk '{printf \"%.2f\", $1}'"
		res = subprocess.check_output(cmd, shell=True)
		temp = res.decode('UTF-8')
		t2 = time.time_ns() - t1
		logger.info('%d', t2/1000000)
		for _ in range(0, int(obtain_temp_period), 1):
			if tt_quit:
				break
			time.sleep(1.0)
		logger.info('obtain_temp_worker: %s', temp)
	logger.info('obtain_temp_worker end')


def display_worker():
	global display_period
	global temp
	global oled
	global th_quit

	logger.info('display_worker start')
	th_quit = False
	x = 0
	y = 12
	text = 'Temperature: ' + temp
	oled.drawtext(x, y, text)
	for _ in range(0, int(display_period), 1):
		if th_quit:
			break
		time.sleep(1.0)
	oled.clear()
	logger.info('display_worker end')


def push_button_callback(channel):
	global th

	logger.info('push_button_callback start')
	if not th.isAlive():
		th = threading.Thread(target=display_worker)
		th.start()
	logger.info('push_button_callback end')


if __name__ == '__main__':
	global oled
	global display_period
	global temp

	signal.signal(signal.SIGINT, signal_handler)

	display_period = 15
	oled = OledSsd1306(rst)
	oled.initialize()

	temp = ''
	obtain_temp_period = 60.0
	tt = threading.Thread(target=obtain_temp_worker)
	tt.start()

	time.sleep(3)

	th = threading.Thread(target=display_worker)
	th.start()

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(
		pin, GPIO.FALLING, callback=push_button_callback, bouncetime=300)

	signal.pause()
