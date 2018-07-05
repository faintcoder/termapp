#!/usr/bin/env python3
import urwid
from .common              import *
from .dialog_base         import DialogBase


class DialogUserPass(DialogBase):

	def __init__(
		self,
		main_application,
		text   = "Enter username and password.",
		title  = "Login",
		tag    = "tag"
	):
		self.userWidget = urwid.Edit("User: ", "")
		self.passWidget = urwid.Edit("Pass: ", "", mask="*")
		super().__init__(
			main_application    = main_application,
			text                = text,
			title               = title,
			tag                 = tag,			
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
		if key == "enter" or key == "tab":
			if self.widget.get_focus() == "body":
				column_widget_in_focus = self.pile.focus_position
				if column_widget_in_focus == 1:
					self.pile.set_focus(2)
					return
				if column_widget_in_focus == 2:
					self.widget.set_focus("footer")
					return
		if key == "tab":
			if self.widget.get_focus() == "footer":
				self.widget.set_focus("body")
				self.pile.set_focus(1)
		super().keypress(size, key)


