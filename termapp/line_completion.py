#!/usr/bin/env python3
import urwid
from .common              import *
from .line_base           import LineBase
from .timer_entry         import TimerEntry


class LineCompletion(LineBase):

	def __init__(
		self,
		loop,
		caption,
		caption_style           = "highlight_color",
		waiting_style           = "compl_waiting_color",
		waiting_flash_style     = "compl_waiting_fl_color",
		error_style             = "compl_error_color",
		success_style           = "compl_success_color",
		initial_status          = StatusWaiting,
		initial_status_text     = "WAITING",
		status_width            = 12,
		flash_waiting           = False,
		flash_seconds           = 0.66
	):
		super().__init__()
		# Create the caption text.
		self.loop               = loop
		self.captionWidget      = urwid.Text((caption_style, caption), "left")
		self.captionStyle       = caption_style
		# Save styles.
		self.waitingStyle       = waiting_style
		self.waitingFlashStyle  = waiting_flash_style
		self.errorStyle         = error_style
		self.successStyle       = success_style
		if initial_status      == StatusWaiting:
			initial_style         = waiting_style
		if initial_status      == StatusError:
			initial_style         = error_style
		if initial_status      == StatusSuccess:
			initial_style         = success_style
		# Create status widget.
		self.statusWidget       = urwid.Text((initial_style, initial_status_text), "center")
		self.attrWidget         = urwid.AttrMap(self.statusWidget, initial_style)
		# Check status width.
		if status_width < DEFAULT_LINE_COMPL_MIN_W:
			status_width = DEFAULT_LINE_COMPL_MIN_W
		# Create the final widget container.
		widget_list             = []
		widget_list.append(self.captionWidget)
		widget_list.append((status_width, self.attrWidget))
		self.widget             = urwid.Columns(widget_list, dividechars=1, min_width=20)
		# Set up flashing, if necessary.
		self.flashTimerEntry    = TimerEntry(seconds=flash_seconds, callback=self.onTimer)
		if flash_waiting       == True:
			self.startFlashing()

	#
	# Callbacks Functions.
	#
	def onTimer(self, timer_entry):
		waiting_text = self.statusWidget.get_text()
		if timer_entry.on:
			self.statusWidget.set_text((self.waitingFlashStyle, waiting_text[0]))
			self.attrWidget.set_attr_map({ None : self.waitingFlashStyle })
		else:
			self.statusWidget.set_text((self.waitingStyle, waiting_text[0]))
			self.attrWidget.set_attr_map({ None : self.waitingStyle })
		return True

	#
	# Inherited Functions.
	#
	def rows(self, visible_columns):
		return self.widget.rows((visible_columns,))

	#
	# Flashing Functions.
	#
	def startFlashing(self):
		return self.loop.startTimerEntry(self.flashTimerEntry)


	def stopFlashing(self):
		return self.loop.cancelTimer(self.flashTimerEntry)

	#
	# Main Functions.
	#
	def setText(self, text):
		self.captionWidget.set_text((self.captionStyle, text))


	def setWaiting(self, text = "WAITING"):
		self.statusWidget.set_text((self.waitingStyle, text))
		self.attrWidget.set_attr_map({ None : self.waitingStyle })


	def setError(self, text = "ERROR"):
		if self.flashTimerEntry.isActive():
			self.stopFlashing()
		self.statusWidget.set_text((self.errorStyle, text))
		self.attrWidget.set_attr_map({ None : self.errorStyle })


	def setSuccess(self, text = "SUCCESS"):
		if self.flashTimerEntry.isActive():
			self.stopFlashing()
		self.statusWidget.set_text((self.successStyle, text))
		self.attrWidget.set_attr_map({ None : self.successStyle })


