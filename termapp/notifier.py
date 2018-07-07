#!/usr/bin/env python3
import urwid
from .common              import *
from .timer_entry         import TimerEntry


class Notifier():

	def __init__(self, loop, pile, text, style="notifier_color"):		
		self.loop             = loop
		self.pile             = pile
		self.expired          = False
		self.textWidget       = urwid.Text((style, text), wrap=urwid.CLIP)
		self.widget           = urwid.AttrMap(self.textWidget, style)
		self.timerEntry       = TimerEntry(seconds=4, callback=self.onTimer)

	#
	# Callback Functions.
	#
	def onTimer(self, timer_entry):
		self.remove()
		return False

	#
	# Remove Functions.
	#
	def removeInSeconds(self, seconds):
		# Start a timer that will call `self.remove()`
		# to let this `Notifier` to remove itself from
		# the `Pile` object.
		if seconds > 0:
			self.timerEntry.seconds = seconds
			return self.loop.startTimerEntry(self.timerEntry)
		return False


	def remove(self):
		# Mark this notifier as expired.
		self.expired = True
		# To remove itself from the urwid.Pile object,
		# we have to create a new list, and add in this
		# new list ALL Pile's object, except this one.
		# Then, we substitute this new list with the
		# old one.
		new_list = []
		for entry in self.pile.contents:
			if entry[0] != self.widget:
				new_list.append(entry)
		self.pile.contents = new_list

	#
	# Text, show Functions.
	#
	def setText(self, text):
		self.textWidget.set_text(text)


	def show(self):
		# Append the notifier's text widget to
		# the urwid.Pile object.
		self.pile.contents.append((self.widget, ("weight", 1)))


