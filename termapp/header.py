#!/usr/bin/env python3
import urwid


class Header():

	def __init__(self, create_text_header = True, create_divider = False, palette_entry_name = "header_color", additional_widgets = []):
		# Create the list where to pile header widgets.
		widget_pile_list       = []
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
			total_spaces = self.totalColumns - len(header_text)
			final_header_text = header_text + (" " * total_spaces)
			self.textWidget.set_text((self.textPaletteEntry, final_header_text))


	def clearText(self):
		if self.textWidget:
			self.setText("")


