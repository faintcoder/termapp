#!/usr/bin/env python3


class Command():

	def __init__(
		self,
		success                     = True,
		command                     = None,
		command_description         = None,
		params                      = None,
		on_success                  = None,
		on_error                    = None,
		on_waiting                  = None,
		error_message               = None,
		user_data                   = None
	):
		self.success                = success
		self.command                = command
		self.commandDescription     = command_description
		self.params                 = params
		self.callbackWaiting        = on_waiting
		self.callbackSuccess        = on_success
		self.callbackError          = on_error
		self.errorMessage           = error_message
		self.userData               = user_data


	def start(self):
		# Starting a command means call 
		callback_global_waiting     = self.commandDescription.callbackWaiting
		callback_local_waiting      = self.callbackWaiting
		result                      = True
		if callback_local_waiting:
			result = callback_local_waiting(self)
		elif callback_global_waiting:
			result = callback_global_waiting(self)
		return result


	def call(self):
		result                      = None
		params                      = self.params		
		params_ignore               = self.commandDescription.paramsIgnore
		params_join                 = self.commandDescription.paramsJoin
		callback                    = self.commandDescription.callback
		if params_ignore:
			# If flag "params_ignore" is set, let's call
			# the callback ignoring all parameters.
			result = callback()
		else:
			if params_join:
				# If the flag "params join" is set, let's
				# join all params into an unique string.
				joined_params = " ".join(params)
				self.params = joined_params
			# - Call the command callback! -
			result = callback(self)
		return result


	def complete(self):
		# To complete a command, we have just to call the "on success"
		# or "on error" callbacks, if they are present.
		# Callbacks from this very `Command` object have priority from
		# those globally specified in the `CommandDescriptor` object. 
		if self.success:
			callback_global_success   = self.commandDescription.callbackSuccess
			callback_local_success    = self.callbackSuccess
			if callback_local_success:
				callback_local_success(self)
			elif callback_global_success:
				callback_global_success(self)
		else:
			callback_global_error     = self.commandDescription.callbackError
			callback_local_error      = self.callbackError
			if callback_local_error:
				callback_local_error(self)
			elif callback_global_error:
				callback_global_error(self)


