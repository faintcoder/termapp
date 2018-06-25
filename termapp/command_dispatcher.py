#!/usr/bin/env python3
from inspect import signature


class CommandDispatcher():

	def __init__(self):
		self.commands = {}


	def registerCommand(self, command, fn, pass_params = True, positional_params = True, join_params = False):
		if len(command) == 0:
			return False
		if " " in command:
			return False
		self.commands[command] = {}
		self.commands[command]["function"]           = fn
		self.commands[command]["pass_params"]        = pass_params
		self.commands[command]["positional_params"]  = positional_params
		self.commands[command]["join_params"]        = join_params
		return True


	def unregisterCommand(self, command):
		if command in self.commands:
			self.commands.pop(command, None)
			return True
		return False


	def registerAlias(self, command, alias):
		if command not in self.commands:
			return False
		if command == alias:
			return False
		self.commands[alias] = self.commands[command]
		return True


	def unregisterAlias(self, alias):
		if alias in self.commands:
			self.commands.pop(alias, None)
			return True
		return False


	def commandExists(self, command_name):
		if command_name in self.commands:
			return True
		return False


	def dispatch(self, command, params):
		if command not in self.commands:
			return False
		fn                 = self.commands[command]["function"]
		pass_params        = self.commands[command]["pass_params"]
		positional_params  = self.commands[command]["positional_params"]
		join_params        = self.commands[command]["join_params"]
		if pass_params:
			if positional_params and not join_params:
				fn(*params)
			else:
				if join_params:
					joined_params = " ".join(params)
					fn(joined_params)
				else:
					fn(params)
		else:
			fn()
		return True


