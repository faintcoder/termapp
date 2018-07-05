#!/usr/bin/env python3
import urwid
import os


class Loop(urwid.MainLoop):
	
	def __init__(self, main_application, palette):
		super().__init__(main_application, palette=palette, pop_ups=True)
		self.mainApplication  = main_application
		self.pipefd           = None

	#
	# Callback Functions
	#
	def entering_idle(self):
		super().entering_idle()
		self.mainApplication.onIdle()
		return True

	#
	# Main Functions
	#
	def flush(self):
		self.draw_screen()


	def init(self):
		if not self.pipefd:
			# Get a pipe write file descriptor.
			self.pipefd = self.watch_pipe(self.onWakeup)
		return True


	def clean(self):
		if self.pipefd:
			# Remove the pipe fd from the main loop.
			self.remove_watch_pipe(self.pipefd)
			# It is our responsibility to close the
			# pipe file descriptor.
			os.close(self.pipefd)
			self.pipefd = None


	def exit(self):
		raise urwid.ExitMainLoop()


	def wakeup(self):
		# We can write to this file descriptor to
		# wake up the main loop.
		os.write(self.pipefd, b"wokeup")

	#
	# Callback Functions.
	#
	def onWakeup(self, data):
		self.mainApplication.onIdle()
		return True


