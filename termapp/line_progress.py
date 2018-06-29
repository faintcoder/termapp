#!/usr/bin/env python3
import urwid
from .line_base           import LineBase


class LineProgress(LineBase):

	def __init__(
		self,
		loop,
		caption,
		initial_value         = 0,
		max_value             = 100,
		caption_style         = "normal_color",
		value_style           = "normal_color",
		completed_style       = "completed_progressbar",
		uncompleted_style     = "uncompleted_progressbar",
		display_value         = True,
		display_value_first   = True,
		progress_width        = 0,
		value_width           = 0
	):
		super().__init__()
		# Create widget list.
		widget_list           = []
		# Set up properties.
		self.loop             = loop
		self.value            = initial_value
		self.max              = max_value
		# Create the caption text.
		self.captionWidget    = urwid.Text((caption_style, caption))
		self.captionStyle     = caption_style
		# Create the progressbar.
		self.progressWidget   = urwid.ProgressBar(
														complete=completed_style,
														normal=uncompleted_style,
														current=initial_value,
														done=max_value
													)
		# Add widgets to the list.
		widget_list.append(self.captionWidget)
		if progress_width > 0:
			widget_list.append((progress_width, self.progressWidget))
		else:
			widget_list.append(self.progressWidget)
		# Create the value text, if necessary.
		if display_value:
			self.valueWidget    = urwid.Text((value_style, str(initial_value)))
			self.valueStyle     = value_style
			if value_width > 0:
				widget_list.append((value_width, self.valueWidget))
			else:
				widget_list.append(self.valueWidget)
		else:
			self.valueWidget    = None
			self.valueStyle     = None
		# Check if we have to insert value text before
		# of the progress widget.
		if display_value_first:
			widget_list[1], widget_list[2] = widget_list[2], widget_list[1]
		# Create the final `urwid.Column` widget.
		self.widget           = urwid.Columns(widget_list, dividechars=1, min_width=20)


	def rows(self, visible_columns):
		return self.widget.rows((visible_columns,))


	def setValue(self, value):
		self.value = value
		self.progressWidget.set_completion(value)
		if self.valueWidget:
			self.valueWidget.set_text((self.valueStyle, str(value)))


