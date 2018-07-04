#!/usr/bin/env python3
import sys
import termapp


class TerminalDialogExample(termapp.TermApp):
	
	def __init__(self):
		super().__init__(create_header=True, create_footer=True)
		# Register some example word completions
		self.prompt.autocompletionAddWords(['hello', 'howareyou?'])
		# Register some basic commands
		command_list = []
		command_list.append(termapp.CommandDescription(
			name         = "echo",
			alias        = "e",
			callback     = self.echo,
			params_join  = True
		))
		self.commandDispatcher.registerCommandList(command_list)


	def echo(self, command):
		self.printSuccess("echo:  " + command.params)


	def onDialogResult(self, result):
		self.header.setText(str(result))
		return True


	def onStart(self):
		self.print("Press F4, F5, F6, create example of dialogs")
		return True


	def onKeyPress(self, key):
		if key == "f4":
			self.startDialogUserPass()
		if key == "f5":
			self.startDialogText("Are you sure?", buttons=2)
		if key == "f6":
			dialog = termapp.DialogProgress(self, initial_value=33, text="Downloading . . .", title="Download")
			self.startDialog(dialog)
			self.startTimer(user_data=dialog, callback=lambda user_data: user_data.setValue(89), seconds=2)
			self.startTimer(user_data=dialog, callback=lambda user_data: user_data.setValue(100), seconds=4)
			self.startTimer(user_data=dialog, callback=lambda user_data: self.cancelDialog(), seconds=5)
		return True


my_term = TerminalDialogExample()
if my_term.start():
	my_term.run()
sys.exit(0)

