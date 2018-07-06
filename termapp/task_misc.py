#!/usr/bin/env python3
from .task_base           import TaskBase


class TaskExit(TaskBase):

	def __init__(self, main_application):
		super().__init__(main_application=main_application)
		

	def execute(self):
		self.mainApplication.exit()
		return True


