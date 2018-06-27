#!/usr/bin/env python3
import urwid
from .line_base        import LineBase


class LineProgress(LineBase):

	def __init__(
		self,
		caption,
		initial_value       = 50,
		max_value           = 100,
		caption_style       = "normal_color",
		completed_style     = "completed_progressbar",
		uncompleted_style   = "uncompleted_progressbar"
	):
		super().__init__()
		widget_list         = []
		self.value          = initial_value
		self.max            = max_value
		self.captionWidget  = urwid.Text((caption_style, str(initial_value)))
		self.valueWidget    = urwid.Text((caption_style, caption))
		self.progressWidget = urwid.ProgressBar(
														complete=completed_style,
														normal=uncompleted_style,
														current=initial_value,
														done=max_value
													)
		widget_list.append(self.valueWidget)
		widget_list.append(self.progressWidget)
		widget_list.append(self.captionWidget)		
		self.widget         = urwid.GridFlow(widget_list, 15, 1, 1, "right")


	def rows(self, visible_columns):
		return self.widget.rows((visible_columns,))


	def setValue(self, value):
		self.value = value
		self.progressWidget.set_completion(value)


