#!/usr/bin/env python3
import urwid
from .line_base           import LineBase


class LineText(LineBase):

	def __init__(self, text, full_line = True, style = "normal_color"):
		super().__init__()
		self.style            = style
		if full_line:
			self.textWidget     = urwid.Text((style, text))
			self.attrWidget     = urwid.AttrMap(self.textWidget, style)
			self.widget         = self.attrWidget
		else:
			self.textWidget     = urwid.Text((style, text))
			self.widget         = self.textWidget
			self.attrWidget     = None


	def rows(self, visible_columns):
		return self.widget.rows((visible_columns,))


	def setText(self, text):
		self.textWidget.set_text(text)


	def setStyle(self, style):
		if self.attrWidget:
			self.attrWidget.set_attr_map({ None : style })
		else:
			line_text = self.textWidget.get_text()
			self.textWidget.set_text((style, line_text))


