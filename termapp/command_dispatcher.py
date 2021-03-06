#!/usr/bin/env python3
from .command             import Command
from .worker_queue        import WorkerQueue
from .task_command        import TaskCommandCompleter
from threading            import Thread
import sys


class _CommandExecutor(WorkerQueue):

	def __init__(self, command_dispatcher):
		super().__init__()
		self.commandDispatcher = command_dispatcher


	def stop(self):
		# First, call parent's class `stop()` function, which will
		# end the infinite loop.
		super().stop()
		# Then,  we must enqueue a `None` object, which is the "kill pill"
		# for this thread: it will wake up the thread, and make it exits.
		self.enqueueTask(None)


	def onTask(self, task):
		# NOTE: Here `task` is a `Command` object.
		# If the `Command` object is `None`, it means that it is the
		# "kill pill", and that this thread must exit.
		if task == None:
			sys.exit(0)
		command = task
		# - Execute command! - 
		command.call()
		# Once the command has been executed, we have to complete it,
		# from this thread, if "deferred completion"  option has been
		# specified, or from the main thread.
		if command.commandDescription.deferredCompletion:
			command.complete()
		else:
			# If we have to complete the command from the main thread,
			# we will enqueue a new `TaskCommandCompleter` object to the
			# main application.
			task = TaskCommandCompleter(
				main_application  = self.commandDispatcher.mainApplication,
				command           = command
			)
			self.commandDispatcher.mainApplication.enqueueTaskAndWakeup(task)


class CommandDispatcher():

	def __init__(self, main_application, on_command_error = None):
		self.mainApplication  =  main_application
		self.onCommandError   =  on_command_error
		self.commands         =  {}
		self.commandExecutor  = _CommandExecutor(self)


	def start(self):
		# Initialize the queues.
		self.commandExecutor.start()
		# Start the secondary thread that
		# will execute deferred commands.
		self._secondaryThread = Thread(target=self.commandExecutor.run)
		self._secondaryThread.setDaemon(True)
		self._secondaryThread.start()
		return True


	def stop(self):
		self.commandExecutor.stop()
		self._secondaryThread.join()


	def registerCommand(self, command_description):
		command_name = command_description.name
		# Check if command name is valid.
		if len(command_name) == 0:
			return False
		if " " in command_name:
			return False
		# Map the command name to the `CommandDescription`
		# object.
		self.commands[command_name] = command_description
		if command_description.alias:
			alias = command_description.alias
			# Check if the command has an alias, and store
			# the alias too.
			if alias not in self.commands and alias != command_name:
				self.commands[alias] = command_description
		return True


	def registerCommandList(self, command_list):
		for command_description in command_list:
			result = self.registerCommand(command_description)
			if not result:
				return False
		return True


	def unregisterCommand(self, command_name):
		if command_name in self.commands:
			# Check if the command has an alias.
			alias = self.commands[command_name].alias
			if alias:
				# Remove the alias
				self.commands.pop(alias, None)
			# Remove the command itself.
			self.commands.pop(command, None)
			return True
		return False


	def commandIsRegistered(self, command_name):
		if command_name in self.commands:
			return True
		return False


	def dispatch(self, command_line):
		# -- Parse the command line --
		# First of all, let's split the command line
		# into tokens delimited by spaces.
		params = command_line.split(" ")
		# The command is the first token, obviously.
		command_name = params[0]
		# Remove the command from the params.
		params.pop(0)
		# If the command is not registered, an unknown
		# command has been typed, let's signal this to
		# the user.
		if command_name not in self.commands:
			if self.onCommandError:
				self.onCommandError(command_name)
			return False
		# Load the `CommandDescription` object.
		command_description   = self.commands[command_name]
		# -- Parse command options --
		if command_description.paramsParseOptions:
			real_params         = []
			options             = []
			opt_delim           = command_description.optionsDelimiter
			opt_delim_len       = len(opt_delim)
			for token in params:
				if token.startswith(opt_delim):
					option = token[opt_delim_len:]
					options.append(option)
				else:
					real_params.append(token)
		else:
			real_params         = params
			options             = []
		# Create a `Command` object.
		command = Command(
								command             = command_name,
								command_description = command_description,
								params              = real_params,
								options             = options
							)
		# -- Execute command! --
		# First start the `Command` object.
		# It means that it will call the "waiting"
		# callback, if necessary.
		result = command.start()
		if not result:
			return False
		if command_description.deferred == False:
			# If the command hasn't `deferred` flag set,
			# it means that we can execute it from here,
			# the main thread.
			result = command.call()
			# Once we have executed the command, we must
			# complete it.
			# It means that "on success" or "on error"
			# callbacks will be called.
			command.complete()
		else:
			# If, otherwise, the command has `deferred` flag
			# set, we have to execute it from a secondary
			# thread, or threadpool, so enqueue the `Command`
			# object to the secondary thread's queue.
			self.commandExecutor.enqueueTask(command)
		return True



