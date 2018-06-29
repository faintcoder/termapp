#!/usr/bin/env python3
import urwid
from .common              import *
from .dialog_base         import DialogBase


class DialogUserPass(DialogBase):

	def __init__(
		self,
		main_application,
		tag    = "user_pass",
		title  = "Login",
		text   = "Enter username and password."
	):
		self.userWidget = urwid.Edit("User: ", "")
		self.passWidget = urwid.Edit("Pass: ", "", mask="*")
		super().__init__(
			main_application    = main_application,
			title               = title,
			text                = text,
			width               = 40,
			height              = 15,
			buttons             = 2,
			button_captions     = ["Enter", "Cancel"],
			additional_widgets  = [self.userWidget, self.passWidget],
			focus               = "body"
		)


	def onResult(self, button_tuple):
		self.result["username"] = self.userWidget.get_edit_text()
		self.result["password"] = self.passWidget.get_edit_text()
		super().onResult(button_tuple)


	def keypress(self, size, key):
		if key == "enter" and self.widget.get_focus() == "body":
			column_widget_in_focus = self.pile.focus_position
			if column_widget_in_focus == 1:
				self.pile.set_focus(2)
				return
			if column_widget_in_focus == 2:
				self.widget.set_focus("footer")
				return
		super(DialogUserPass, self).keypress(size, key)


