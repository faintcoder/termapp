#!/usr/bin/env python3
import urwid
from .common              import *
from .dialog_base         import DialogBase


class DialogText(DialogBase):

	def __init__(
		self,
		main_application,
		text,
		tag                   = "text",
		title                 = "Warning!",
		buttons               = 2,
		button_captions       = ["OK", "Cancel"]
	):
		super().__init__(
			main_application    = main_application,
			title               = title,
			text                = text,
			width               = 30,
			height              = 10,
			buttons             = buttons,
			button_captions     = button_captions
		)


	def keypress(self, size, key):
		super(DialogText, self).keypress(size, key)


