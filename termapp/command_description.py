#!/usr/bin/env python3


class CommandDescription():

	def __init__(
		self,
		name,
		callback,
		params_ignore               = False,
		params_join                 = False,
		deferred                    = False,
		deferred_completion         = False,
		on_success                  = None,
		on_error                    = None,
		on_waiting                  = None,
		alias                       = None
	):
		# Command name.
		self.name                   = name
		# Main callback to call when this command
		# is typed.
		self.callback               = callback
		# If this option is true, callback() will
		# be called, instead of callback(command).
		self.paramsIgnore           = params_ignore
		# If this option is true, params will be
		# "a b c" instead of ["a", "b", "c"]
		self.paramsJoin             = params_join
		# If this option is true, the main callback
		# will be called by a secondary thread, and
		# not by the main thread.
		self.deferred               = deferred
		# If this option is true, the completion of the
		# command (e.g. calling success/error callbacks),
		# will be called by the secondary thread itself,
		# instead that the main thread.
		self.deferredCompletion     = deferred_completion
		# These are the callback that will be globally
		# called when the command will be success/error.
		# If the `Command` object has another callback
		# that one will be called, instead of this.
		self.callbackSuccess        = on_success
		self.callbackError          = on_error
		# This is the callback that will be called by
		# the main thread, before executing the main
		# callback (in both cases deferred, or not).
		# This is helpful to display some waiting
		# text, before the main callback will take
		# control of the cpu, maybe for a long time.
		# In such a case, another command will immediately
		# display a waiting string, even if the secondary
		# thread (or a threadpool) is busy executing
		# commands.
		# If the `Command` object has another callback
		# that one will be called, instead of this.
		self.callbackWaiting        = on_waiting
		# The alias of the command
		self.alias                  = alias



