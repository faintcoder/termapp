#!/usr/bin/env python3
import sys
import termapp


class TerminalDialogExample(termapp.TermApp):
	
	def __init__(self):
		super().__init__(create_header=True, create_footer=True)
		self.quitOnESC = True


	def echo(self, command):
		self.printSuccess("echo:  " + command.params)


	def onDialogResult(self, dialog):
		self.print(str(dialog.result))
		return super().onDialogResult(dialog)


	def onStart(self):
		self.print("Press F4, F5, F6, F7, to create examples of dialogs")
		self.print("Press F8 to cancel the dialog")
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
		return True


	def onKeyPress(self, key):
		if key == "f4":
			# Start an example of user/pass input dialog.
			self.startDialogUserPass()
		if key == "f5":
			# Start an example of Yes/Cancel dialog.
			self.startDialogText("Are you sure?", buttons=2)
		if key == "f6":
			# Start an example of progress dialog: a timer will
			# change progressbar position.
			dialog = termapp.DialogProgress(self, initial_value=33, text="Downloading . . .", title="Download")
			self.startDialog(dialog)
			self.loop.startTimer(user_data=dialog, callback=lambda timer_entry: timer_entry.userData.setValue(89), seconds=2)
			self.loop.startTimer(user_data=dialog, callback=lambda timer_entry: timer_entry.userData.setValue(100), seconds=4)
			self.loop.startTimer(user_data=dialog, callback=lambda timer_entry: self.cancelDialog(), seconds=5)
		if key == "f7":
			# Start a smarter example of progress dialog: the timer
			# will set progressbar position by checking it's `times`
			# property.
			dialog = termapp.DialogProgress(self, initial_value=0, text="Downloading . . .", title="Download")
			self.startDialog(dialog)
			self.loop.startTimer(user_data=dialog, callback=lambda timer_entry: timer_entry.userData.setValue(timer_entry.times), seconds=0.05, repeats=100)
			self.loop.startTimer(user_data=dialog, callback=lambda timer_entry: self.cancelDialog(), seconds=6)
		if key == "f8":
			self.cancelDialog()
		return True


my_term = TerminalDialogExample()
if my_term.start():
	my_term.run()
sys.exit(0)

