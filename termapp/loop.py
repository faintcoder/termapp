#!/usr/bin/env python3
from .timer_entry         import TimerEntry
from .timer_entry         import _timer_entry_main_callback
import urwid
import os


class Loop(urwid.MainLoop):
	
	def __init__(self, main_application, palette):
		super().__init__(main_application, palette=palette, pop_ups=True)
		self.mainApplication  = main_application
		self.pipefd           = None

	#
	# `urwid.MainLoop` Callback Functions
	#
	def entering_idle(self):
		super().entering_idle()
		self.mainApplication.onIdle()
		return True

	#
	# Local object Callback Functions.
	#
	def onWakeup(self, data):
		self.mainApplication.onIdle()
		return True


	def onDataArrival(self):
		self.mainApplication.onDataArrival()
		return True

	#
	# Init/Exit Functions
	#
	def init(self):
		if not self.pipefd:
			# Get a pipe write file descriptor.
			self.pipefd = self.watch_pipe(self.onWakeup)
		return True


	def gracefulExit(self):
		if self.pipefd:
			# Remove the pipe fd from the main loop.
			self.remove_watch_pipe(self.pipefd)
			# It is our responsibility to close the
			# pipe file descriptor.
			os.close(self.pipefd)
			self.pipefd = None
		self.exit()


	def exit(self):
		raise urwid.ExitMainLoop()

	#
	# Misc Functions.
	#
	def flush(self):
		self.draw_screen()


	def wakeup(self):
		# We can write to this file descriptor to
		# wake up the main loop.
		os.write(self.pipefd, b"wokeup")

	#
	# Timer Functions.
	#
	def startTimer(self, seconds, callback, user_data = None, repeats = 0):
		# Create the `TimerEntry` object.
		timer_entry = TimerEntry(
			seconds     = seconds,
			callback    = callback,
			user_data   = user_data,
			repeats     = repeats
		)
		# Start the timer.
		self.startTimerEntry(timer_entry)
		# Return the `TimerEntry` object to the user.
		return timer_entry


	def startTimerEntry(self, timer_entry):
		# If the `TimerEntry` object has a timer handle
		# already set, let's block this.
		if timer_entry.handle:
			return False
		# Create the tuple to pass as `user_data`
		# to the main system callback.
		user_data_tuple = (timer_entry, self)
		# Create the real timer.
		timer_entry.handle = self.set_alarm_in(
			sec        = timer_entry.seconds,
			callback   = _timer_entry_main_callback,
			user_data  = user_data_tuple
		)
		return timer_entry


	def cancelTimer(self, timer_entry):
		if timer_entry.handle:
			self.remove_alarm(timer_entry.handle)
			timer_entry.handle = None
			return True
		return False

	#
	# Files Functions.
	#
	def watchFd(self, fd):
		return self.watch_file(fd, self.onDataArrival)


	def removeFd(self, handle):
		return self.remove_watch_file(handle)


