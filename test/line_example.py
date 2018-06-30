#!/usr/bin/env python3
import sys
import termapp


class MyTerminal(termapp.TermApp):
	
	def __init__(self):
		super().__init__(create_header=True, create_footer=True)
		# Register some example word completions
		self.prompt.autocompletionAddWords(['hello', 'howareyou?'])
		# Register some basic commands
		self.commandDispatcher.registerCommand("echo", self.echo, join_params=True)
		self.commandDispatcher.registerAlias("echo", "e")


	def echo(self, params):
		self.printSuccess("echo:  " + params)


	def onDialogResult(self, result):
		self.header.setText(str(result))
		return True


	def onStart(self):
		self.print("Press F7, F8, F9, to create example of different kinds of lines.")
		return True


	def onKeyPress(self, key):
		if key == "f7":
			line_progress = termapp.LineProgress(self.loop, "f572d396fae9206628714fb2ce00f72e94f2258f", max_value=10000, initial_value=3344, display_value=True, progress_width=12, value_width=8)
			self.currentPageAppendLine(line_progress)
			self.startTimer(user_data=line_progress, callback=lambda user_data: user_data.setValue(8896), seconds=4)
		if key == "f8":
			line_copml = termapp.LineCompletion(self.loop, "Downloading emails ...")
			self.currentPageAppendLine(line_copml)
			self.startTimer(user_data=line_copml, callback=lambda user_data: user_data.setError(), seconds=2)
		if key == "f9":
			line_copml = termapp.LineCompletion(self.loop, "Downloading archives ...")
			self.currentPageAppendLine(line_copml)
			self.startTimer(user_data=line_copml, callback=lambda user_data: user_data.setSuccess(), seconds=2)
		return True


my_term = MyTerminal()
if my_term.start():
	my_term.run()
sys.exit(0)

