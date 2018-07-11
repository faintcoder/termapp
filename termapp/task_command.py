#!/usr/bin/env python3
from .task_base           import TaskBase


class TaskCommand(TaskBase):

	def __init__(self, main_application, command_line):
		super().__init__(main_application=main_application)
		self.command_line  = command_line
		

	def execute(self):
		# Ignore empty strings
		if self.command_line == "" or self.command_line == " ":
			return False
		# Then we pass command and parameters to
		# the command dispatcher object.
		command_dispatcher = self.mainApplication.commandDispatcher
		return command_dispatcher.dispatch(self.command_line)


class TaskCommandCompleter(TaskBase):

	def __init__(self, main_application, command):
		super().__init__(main_application=main_application)
		self.command = command
		

	def execute(self):
		self.command.complete()
		return True


