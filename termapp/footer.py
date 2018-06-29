#!/usr/bin/env python3
import urwid


class Footer():

	def __init__(self, prompt_widget, create_text_footer = True, style = "footer_color"):
		# Create the list where to pile footer widgets.
		widget_pile_list      = []
		# Allow space for the loop object.
		self.loop             = None
		# Create the text widget, and add to list.
		if create_text_footer:
			self.textWidget     = urwid.Text((style, ""), wrap=urwid.CLIP)
			self.footerWidget   = urwid.AttrMap(self.textWidget, style)			
			widget_pile_list.append(self.footerWidget)
		else:
			self.textWidget     = None
		# Add prompt widget.
		widget_pile_list.append(prompt_widget)
		# Create the `urwid.Pile` object, setting focus to the,
		# prompt widget, which is the last widget we have added
		# to the list.
		prompt_position       = len(widget_pile_list) - 1
		self.widget           = urwid.Pile(widget_pile_list, focus_item=prompt_position)
		# Get screen object and screen's cols/rows
		self.screen           = urwid.raw_display.Screen()
		self.totalColumns     = self.screen.get_cols_rows()[0]
		self.totalRows        = self.screen.get_cols_rows()[1]


	def setText(self, text):
		self.textWidget.set_text(text)


	def clearText(self):
		if self.textWidget:
			self.setText("")


