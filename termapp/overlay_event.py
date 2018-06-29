#!/usr/bin/env python3
import urwid


class OverlayEvent(urwid.WidgetWrap):

	def __init__(
		self,
		first_widget,
		second_widget,
		width                    = 15,
		height                   = 10,
		vertical_align           = "middle",
		horizontal_align         = "center"
	):
		# Create widget overlay
		overlay = urwid.Overlay(
			first_widget,
			second_widget,
			align                  = horizontal_align,
			valign                 = vertical_align,
			width                  = width,
			height                 = height
		)
		# Set properties
		self.foregroundWidget    = first_widget
		self.backgroundWidget    = second_widget
		self._w                  = overlay


	def keypress(self, size, key):
		pass


