#!/usr/bin/env python3
import urwid
from .common              import *
from .overlay_event       import OverlayEvent
from .task_dialog         import TaskDialog


class DialogBase(urwid.WidgetWrap):

	def __init__(
		self,
		main_application,
		title               = "untitled",
		tag                 = "tag",
		buttons             = 2,
		button_captions     = ["OK", "Cancel"],
		button_width        = 12,
		text                = "Hello!",
		additional_widgets  = [],
		width               = 30,
		height              = 15,
		focus               = "footer"
	):
		# This is the dialog cancel switch.
		# If this will be set to True, dialog
		# will cancel, after reporting result.
		self.cancel              = True
		# Dialog tag.
		self.tag                 = tag
		# Create dialog result dictionary.
		self.result              = { }
		# Save main app instance
		self.mainApplication     = main_application
		# Header
		header_text              = urwid.Text(("dialog_banner", title), align="center")
		header                   = urwid.AttrMap(header_text, "dialog_banner")
		# Body
		body_text                = urwid.Text(("dialog_background", text + "\n"), align="center")
		pile                     = urwid.Pile([body_text] + additional_widgets)
		body_filler              = urwid.Filler(pile, valign = "top")
		body_padding             = urwid.Padding(body_filler, left = 1, right = 1)
		body_line_box            = urwid.LineBox(body_padding)
		body                     = urwid.AttrMap(body_line_box, "dialog_background")
		# Create buttons
		button_list              = []
		for i in range(0, buttons):
			button_caption         = button_captions[i]
			button_tuple           = (i, button_caption)
			button                 = urwid.Button(button_caption, lambda x, button_tuple=button_tuple: self.onResult(button_tuple))
			button_list.append(button)
		# Create footer
		footer_grid              = urwid.GridFlow(button_list, button_width, 1, 1, "center")
		footer                   = urwid.AttrMap(footer_grid, "dialog_buttons")
		# Dialog widget
		frame = urwid.Frame(
			body                   = body,
			header                 = header,
			footer                 = footer,
			focus_part             = focus
		)
		# Create overlay widget to overlay the dialog object
		# to the main screen body.
		overlay = OverlayEvent(
			first_widget           = frame,
			second_widget          = self.mainApplication.body,
			width                  = width,
			height                 = height,
			horizontal_align       = "center",
			vertical_align         = "middle"
		)
		# Save widgets for rapid access.
		self.body                = body
		self.pile                = pile
		self.overlay             = overlay
		self.widget              = frame
		self._w                  = frame


	def onResult(self, button_tuple):
		button_id                      = button_tuple[0]
		button_caption                 = button_tuple[1]
		self.result["button_id"]       = button_id
		self.result["button_caption"]  = button_caption
		task = TaskDialog(
			main_application  = self.mainApplication,
			dialog            = self
		)
		self.mainApplication.enqueueTask(task)


	def keypress(self, size, key):
		return super().keypress(size, key)


