#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
import sys
import os
import subprocess
import time


device_dir = '/sys/bus/w1/devices/'
w1_data = '/w1_slave'
temperature_device = '28-'


def get_device(dtype):
	devices = os.listdir(device_dir)
	for d in devices:
		if dtype in d:
			return d
	return None


def read_temp(d):
	catdata = subprocess.Popen(
		['cat', device_dir + d + w1_data],
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE
	)
	out, err = catdata.communicate()
	decoded = out.decode('UTF-8')
	lines = decoded.split('\n')
	if lines[0][-3:] == 'YES':
		col = lines[1].find('t=')
		if col != -1:
			deg_c = int(lines[1][col+2:]) / 1000.0
			deg_f = deg_c * 9.0 / 5.0 + 32.0
			return deg_c, deg_f
	return None, None


def main():
	status = 0
	d = get_device(temperature_device)
	if d is None:
		status += 1
		return status

	deg_c, deg_f = read_temp(d)
	if deg_c is None:
		status += 1
		return status

	print('{0}, {1}'.format(deg_c, deg_f))
	return status


if __name__ == '__main__':
	s = main()
	sys.exit(s)
