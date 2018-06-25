#!/usr/bin/env python3
import urwid
from .timer_callbacks  import _header_hide_callback


class Header():

	def __init__(self, create_text_header = True, create_divider = False, palette_entry_name = "header_color", additional_widgets = []):
		# Create the list where to pile header widgets.
		widget_pile_list       = []
		# Allow space for the loop object.
		self.loop              = None
		# Timer handles.
		self.timerHandles      = []
		# Create the text widget, and add to list.
		if create_text_header:
			header_widget        = urwid.Text((palette_entry_name, ""), wrap=urwid.CLIP)
			widget_pile_list.append(header_widget)
			self.textWidget      = header_widget
		else:
			self.textWidget      = None
		if create_text_header and create_divider:
			# If necessary, create a divider widget, and add to list.
			divider_widget       = urwid.Divider()
			widget_pile_list.append(divider_widget)
			self.dividerWidget   = divider_widget
		else:
			self.dividerWidget   = None
		# Add additional widgets.
		widget_pile_list      += additional_widgets
		self.widget            = urwid.Pile(widget_pile_list)
		# Get screen object and screen's cols/rows
		self.screen            = urwid.raw_display.Screen()
		self.totalColumns      = self.screen.get_cols_rows()[0]
		self.totalRows         = self.screen.get_cols_rows()[1]
		# Save palette entry name for header text.
		self.textPaletteEntry  = palette_entry_name
		# Reset the text of the header.
		self.clearText()


	def setText(self, header_text):
		if self.textWidget:
			# Add spaces to make a text bar for the entire screen,
			# with the same background.
			total_spaces = self.totalColumns - len(header_text)
			final_header_text = header_text + (" " * total_spaces)
			# Change the text to the header bar.
			self.textWidget.set_text((self.textPaletteEntry, final_header_text))


	def clearText(self):
		if self.textWidget:
			self.setText("")


	def pushNotifier(self, notifier_text, seconds = 0):
		# Add spaces to make a text bar for the entire screen,
		# with the same background.
		total_spaces = self.totalColumns - len(notifier_text)
		final_notifier_text = notifier_text + (" " * total_spaces)
		# Create the new text widget.
		notifier_widget = urwid.Text(("notifier_color", final_notifier_text), wrap=urwid.CLIP)
		# Append the newly created text widget to the pile of
		# the header's widgets.
		self.widget.contents.append((notifier_widget, ("weight", 1)))
		# Save the last widget position in the list.
		last_header_index = len(self.widget.contents) - 1
		# If we have a loop and seconds is > 0, start a timer
		# to remove the widget in N seconds.
		if self.loop and seconds > 0:
			new_handle = self.loop.set_alarm_in(seconds, _header_hide_callback, user_data=(self, notifier_widget))
			self.timerHandles.append(new_handle)


	def popNotifier(self):
		total_headers = len(self.widget.contents) - 1
		self.widget.contents.pop(total_headers)



