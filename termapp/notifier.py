#!/usr/bin/env python3
import urwid
from .common              import *
from .timer_callbacks     import _notifier_remove_callback


class Notifier():

	def __init__(self, loop, pile, text, style="notifier_color"):		
		self.loop             = loop
		self.pile             = pile
		self.seconds          = None				
		self.expired          = False
		self.textWidget       = urwid.Text((style, text), wrap=urwid.CLIP)
		self.widget           = urwid.AttrMap(self.textWidget, style)
		# Private data
		self._timerHandle     = None


	def setText(self, text):
		self.textWidget.set_text(text)


	def autoDestroy(self, seconds):
		# Start a timer that will call `self.remove()`
		# to let this Notifier to remove itself from
		# the Pile object.
		if seconds > 0:
			if self._timerHandle:
				self.loop.remove_alarm(self._timerHandle)
			self._timerHandle   = self.loop.set_alarm_in(seconds, _notifier_remove_callback, user_data=self)
			self.seconds        = seconds


	def show(self):
		# Append the notifier's text widget to
		# the urwid.Pile object.
		self.pile.contents.append((self.widget, ("weight", 1)))


	def remove(self):
		# Mark this notifier as expired.
		self.expired = True
		# If there is a pending timer, remove it.
		if self._timerHandle:
			self.loop.remove_alarm(self._timerHandle)
			self._timerHandle = None
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


