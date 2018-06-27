#!/usr/bin/env python3
from .common import *
import urwid


class Dialog():

	def __init__(self, main_application, text, tag="tag", title="Warning!", buttons=2, button1_text="Ok", button2_text="Cancel"):
		# Save main app instance
		self.mainApplication     = main_application
		# Set dialog tag
		self.tag                 = tag
		# Header
		header_text              = urwid.Text(("dialog_banner", title), align="center")
		header                   = urwid.AttrMap(header_text, "dialog_banner")
		# Body
		body_text                = urwid.Text(("dialog_background", text), align="center")
		body_filler              = urwid.Filler(body_text, valign = "top")
		body_padding             = urwid.Padding(body_filler, left = 1, right = 1)
		body_line_box            = urwid.LineBox(body_padding)
		body                     = urwid.AttrMap(body_line_box, "dialog_background")
		# Create buttons
		button_list = []
		button1                  = urwid.Button(button1_text, self._on_result)
		button_list.append(button1)
		if buttons > 1:
			button2                = urwid.Button(button2_text, self._on_result)
			button_list.append(button2)
		# Create footer
		footer_grid              = urwid.GridFlow(button_list, 12, 1, 1, "center")
		footer                   = urwid.AttrMap(footer_grid, "dialog_buttons")
		# Dialog widget
		layout = urwid.Frame(
			body,
			header=header,
			footer=footer,
			focus_part="footer"
		)
		# Calc dialog size
		if len(text) > DEFAULT_DIALOG_MIN_WIDTH:
			visible_columns = main_application.geometry.bodyColumns
			visible_columns -= 8
			if len(text) > visible_columns:
				dialog_w = visible_columns
			else:
				dialog_w = len(text)
			dialog_h = DEFAULT_DIALOG_MIN_HEIGHT
		else:
			dialog_w = DEFAULT_DIALOG_MIN_WIDTH
			dialog_h = 7
		# Overlay widget
		overlay = urwid.Overlay(
			layout,
			self.mainApplication.body,
			align   = "center",
			valign  = "middle",
			width   = dialog_w,
			height  = dialog_h
		)
		self.widget = layout
		self.overlay = overlay


	def _on_result(self, result):		
		result = self.mainApplication.onDialog(self.tag, result.get_label())
		if result:
			self.mainApplication.cancelDialog()


