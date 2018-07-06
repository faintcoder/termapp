#!/usr/bin/env python3
from .task_base           import TaskBase


class TaskDialog(TaskBase):

	def __init__(self, main_application, dialog):
		super().__init__(main_application=main_application)
		self.dialog  = dialog
		

	def execute(self):
		self.mainApplication.onDialogResult(self.dialog)
		if self.dialog.cancel:
			self.mainApplication.cancelDialog()
		return True


