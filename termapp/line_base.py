#!/usr/bin/env python3
import urwid
import datetime


class LineBase():

	def __init__(self):
		self.widget     = None
		self.timestamp  = datetime.datetime.now()


	def rows(self, visible_columns):
		return 0


	def setStyle(self, style):
		pass


