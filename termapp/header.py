#!/usr/bin/env python3
import urwid
from .notifier            import Notifier


class Header():

	def __init__(
		self,
		create_text_header    = True,
		create_divider        = False,
		style                 = "header_color",
		additional_widgets    = []
	):
		# Create the list to keep all `Notifier` objects.
		self.notifiers        = []
		# Create the list to keep all header widgets.
		self.pile             = []
		# Allow space for the loop object.
		self.loop             = None
		# Create the text widget, and add to list.
		if create_text_header:
			self.textWidget     = urwid.Text((style, ""), wrap=urwid.CLIP)
			self.headerWidget   = urwid.AttrMap(self.textWidget, style)
			self.pile.append(self.headerWidget)
		else:
			self.textWidget     = None
		if create_text_header and create_divider:
			# If necessary, create a divider widget, and add to list.
			self.dividerWidget  = urwid.Divider()
			self.pile.append(self.dividerWidget)
		else:
			self.dividerWidget  = None
		# Add additional widgets.
		self.pile            += additional_widgets
		self.widget           = urwid.Pile(self.pile)
		# Get screen object and screen's cols/rows
		self.screen           = urwid.raw_display.Screen()
		self.totalColumns     = self.screen.get_cols_rows()[0]
		self.totalRows        = self.screen.get_cols_rows()[1]


	def setText(self, text):
		# Change the text to the header bar.
		self.textWidget.set_text(text)


	def clearText(self):
		if self.textWidget:
			self.setText("")


	def createNotifier(self, text, seconds=0, style="notifier_color"):
		# Create a new `Notifier` object.
		notifier = Notifier(loop=self.loop, pile=self.widget, text=text, style=style)
		# Add to the internal list.
		self.notifiers.append(notifier)
		# Make Notifier object visible.
		notifier.show()
		# Check if we have start a self-destruction timer
		# for the Notifier object.
		if seconds > 0:
			notifier.removeInSeconds(seconds)
		# Refresh the screen.
		self.loop.flush()
		# Return the notifier to the user.
		return notifier


	def resetNotifiers(self):
		# Erase all notifiers.
		for notifier in self.notifiers:
			notifier.remove()
		# Refresh the screen.
		self.loop.flush()


