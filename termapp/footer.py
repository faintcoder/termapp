#!/usr/bin/env python3
import urwid


class Footer():

	def __init__(self, prompt_widget, create_text_footer = True, palette_entry_name = "footer_color"):
		# Create the list where to pile footer widgets.
		widget_pile_list       = []
		# Allow space for the loop object.
		self.loop              = None
		# Create the text widget, and add to list.
		if create_text_footer:
			footer_widget        = urwid.Text((palette_entry_name, ""), wrap=urwid.CLIP)
			widget_pile_list.append(footer_widget)
			self.textWidget      = footer_widget
		else:
			self.textWidget      = None
		# Add prompt widget.
		widget_pile_list.append(prompt_widget)
		# Create the `urwid.Pile` object, setting focus to the,
		# prompt widget, or the last widget we have added to the
		# list.
		self.widget            = urwid.Pile(widget_pile_list, focus_item=(len(widget_pile_list)-1))
		# Get screen object and screen's cols/rows
		self.screen            = urwid.raw_display.Screen()
		self.totalColumns      = self.screen.get_cols_rows()[0]
		self.totalRows         = self.screen.get_cols_rows()[1]
		# Save palette entry name for header text.
		self.textPaletteEntry  = palette_entry_name
		# Reset the text of the header.
		self.clearText()


	def setText(self, footer_text):
		if self.textWidget:
			total_spaces = self.totalColumns - len(footer_text)
			final_footer_text = footer_text + (" " * total_spaces)
			self.textWidget.set_text((self.textPaletteEntry, final_footer_text))


	def clearText(self):
		if self.textWidget:
			self.setText("")


