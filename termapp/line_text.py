#!/usr/bin/env python3
import urwid
from .line_base        import LineBase


class LineText(LineBase):

	def __init__(self, text_style, text):
		super().__init__()
		self.widget     = urwid.Text((text_style, text))


	def rows(self, visible_columns):
		return self.widget.rows((visible_columns,))


	def setStyle(self, style):
		pass


