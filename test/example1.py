#!/usr/bin/env python3
import sys
import time
import termapp


class MyTerminal(termapp.TermApp):
	
	def __init__(self):
		super().__init__(create_header=True, create_footer=True)
		self.prompt.autocompletionAddWords(['hello', 'howareyou?'])
		self.commandDispatcher.registerCommand("echo", self.echo, join_params=True)
		self.commandDispatcher.registerAlias("echo", "e")


	def echo(self, params):
		self.printSuccess("echo:  " + params)


	def onDialog(self, tag, result):
		self.header.setText(result)
		return True


	def onKeyPress(self, key):
		if key == "f2":
			self.switchToNextPage()
		if key == "f3":
			self.switchToPrevPage()
		if key == "f4":
			self.chapters.createNewPage()
		#if key == "f9":
		#	self.prompt.startFlashing(self.loop)
		#if key == "f8":
		#	self.prompt.stopFlashing()
		if key == "f5":
			self.startDialog("Are you sure?", buttons=1)
		if key == "f6":
			self.header.createNotifier(text="hello!!!!", seconds=2)
		if key == "f7":
			line_progress = termapp.LineProgress(self.loop, "f572d396fae9206628714fb2ce00f72e94f2258feee93389289s89", max_value=10000, initial_value=3344, display_value=True, progress_width=12, value_width=8)
			self.currentPageAppendLine(line_progress)
			self.startTimer(user_data=line_progress, callback=lambda user_data: user_data.setValue(8896), seconds=4)
		
		if key == "f9":
			line_copml = termapp.LineCompletion(self.loop, "Downloading stuff ...")
			self.currentPageAppendLine(line_copml)
			self.startTimer(user_data=line_copml, callback=lambda user_data: user_data.setError(), seconds=4)
		return True


my_term = MyTerminal()
if my_term.start():
	my_term.run()
sys.exit(0)

