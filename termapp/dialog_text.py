#!/usr/bin/env python3
import urwid
from .common              import *
from .dialog_base         import DialogBase


class DialogText(DialogBase):

	def __init__(
		self,
		main_application,
		text,
		title                 = "Warning!",
		tag                   = "tag",
		buttons               = 2,
		button_captions       = ["OK", "Cancel"]
	):
		super().__init__(
			main_application    = main_application,
			text                = text,
			title               = title,
			tag                 = tag,
			width               = 30,
			height              = 10,
			buttons             = buttons,
			button_captions     = button_captions
		)


	def keypress(self, size, key):
		super().keypress(size, key)


