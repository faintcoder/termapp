#!/usr/bin/env python3
import sys
import termapp


class MyTerminal(termapp.TermApp):
	
	def __init__(self):
		super().__init__(create_header=True, create_footer=True)
		self.prompt.autocompletionAddWords(['hello', 'howareyou?'])
		self.commandDispatcher.registerCommand("echo", self.echo, join_params=True)
		self.commandDispatcher.registerAlias("echo", "e")


	def echo(self, params):
		self.printSuccess("echo:  " + params)


	def onKeyPress(self, key):
		if key == "f2":
			self.switchToNextPage()
		if key == "f3":
			self.switchToPrevPage()
		if key == "f4":
			self.chapters.createNewPage()
		if key == "f9":
			self.prompt.startFlashing(self.loop)
		if key == "f8":
			self.prompt.stopFlashing()
		if key == "f5":
			self.header.pushNotifier("Hello! Long wait", 5)
		if key == "f6":
			self.header.pushNotifier("Hello! Short wait", 1)
		return True


my_term = MyTerminal()
if my_term.start():
	my_term.run()
sys.exit(0)

