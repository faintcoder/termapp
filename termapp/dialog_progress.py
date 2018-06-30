#!/usr/bin/env python3
import urwid
from .common              import *
from .dialog_base         import DialogBase


class DialogProgress(DialogBase):

	def __init__(
		self,
		main_application,
		text               = "",
		title              = "",
		initial_value      = 0,
		max_value          = 100,
		tag                = "progress",
		completed_style    = "completed_progressbar",
		uncompleted_style  = "uncompleted_progressbar",
		cancelButton       = False,
		width              = 50,
		height             = 8
	):
		self.progressWidget = urwid.ProgressBar(
															complete  = completed_style,
															normal    = uncompleted_style,
															current   = initial_value,
															done      = max_value
													  )
		if cancelButton:
			buttons = 1
			button_captions = ["Cancel"]
		else:
			buttons = 0
			button_captions = []
		super().__init__(
			main_application    = main_application,
			title               = title,
			text                = text,
			width               = 50,
			height              = 8,
			buttons             = buttons,
			button_captions     = button_captions,
			additional_widgets  = [self.progressWidget],
			focus               = "footer"
		)


	def setValue(self, value):
		self.progressWidget.set_completion(value)


