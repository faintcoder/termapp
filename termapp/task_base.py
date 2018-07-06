#!/usr/bin/env python3


class TaskBase():

	def __init__(self, main_application):
		self.mainApplication  = main_application
		self.cancel           = False


	def execute(self):
		pass


