#!/usr/bin/env python3
from .task_base           import TaskBase


class TaskCommand(TaskBase):

	def __init__(self, main_application, command_name, params):
		super().__init__(main_application=main_application)
		self.command_name  = command_name
		self.params        = params
		

	def execute(self):
		# Ignore empty strings
		if self.command_name == "" or self.command_name == " ":
			return False
		# Then we pass command and parameters to
		# the command dispatcher object.
		result = self.mainApplication.commandDispatcher.dispatch(self.command_name, self.params)
		success = result[0]
		message = result[1]
		if not success:
			self.mainApplication.onCommandError(message, self.command_name, self.params)
			return False
		return True


class TaskCommandCompleter(TaskBase):

	def __init__(self, main_application, command):
		super().__init__(main_application=main_application)
		self.command = command
		

	def execute(self):
		self.command.complete()
		return True


