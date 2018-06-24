#!/usr/bin/env python3
import urwid
from .common           import *
from .line_base        import LineBase
from .line_text        import LineText
from .page_base        import PageBase


class Page(PageBase):

	def __init__(self, page_title = DEFAULT_PAGE_TITLE, max_lines = DEFAULT_PAGE_MAX_LINES):
		self.chapter           = None
		self.widgetLinesList   = urwid.SimpleFocusListWalker([])
		self.widgetListBox     = urwid.ListBox(self.widgetLinesList)
		self.title             = page_title
		self.maxLines          = max_lines
		self.addDateTime       = True
		self.currentVisible    = False
		self.scrollable        = True
		self._scrollOffset     = 0
		self._scrollDir        = SCROLL_NONE
		self.widgetListBox.set_focus_valign("bottom")
		super().__init__()

	#
	# Private Functions.
	#
	def _scroll_up(self, n, scroll_dir):
		self._scrollOffset += n
		self._scrollDir     = scroll_dir
		self._adjust_scroll_offset()
		self.updateFocus(self._scrollOffset, self._scrollDir)


	def _scroll_down(self, n, scroll_dir):
		self._scrollOffset -= n
		self._scrollDir     = scroll_dir
		self._adjust_scroll_offset()
		self.updateFocus(self._scrollOffset, self._scrollDir)


	def _first_non_visible_line_pos(self, scroll_dir, geometry):
		visible_rows = geometry.bodyRows
		visible_columns = geometry.bodyColumns
		if self.totalLines() == 0 or self.totalLines() <= visible_rows:
			return (0, False)
		if scroll_dir == SCROLL_UP and self._scrollOffset == (self.totalLines() - 1):
			return (0, False)
		if scroll_dir == SCROLL_DOWN and self._scrollOffset == 0:
			return (0, False)
		total  = 0
		turn   = False
		u      = 0
		v      = self.totalLines() - 1 - self._scrollOffset
		while True:
			if total == visible_rows:
				break
			if total > visible_rows:
				turn = True
				break
			if v > (self.totalLines() - 1):
				break
			total += self.widgetLinesList[v].rows((visible_columns,))
			u     += 1			
			if scroll_dir == SCROLL_UP:
				v   -= 1
				if v == 0:
					break
			if scroll_dir == SCROLL_DOWN:
				v   += 1
		return (u, turn)


	def _get_date_time(self):
		date_time_str = str(datetime.datetime.now())
		final_str = (date_time_str + "  ")
		return final_str


	def _adjust_scroll_offset(self):
		if self._scrollOffset < 0:
			self._scrollOffset = 0
		if self._scrollOffset > len(self.widgetLinesList) - 1:
			self._scrollOffset = len(self.widgetLinesList) - 1

	#
	# Public Functions.
	#
	def totalLines(self):
		return len(self.widgetLinesList)


	def updateFocus(self, offset, scroll_direction = SCROLL_DOWN):
		# Set the direction of the scroll.
		if scroll_direction == SCROLL_UP:
			scroll_dir="below"
		elif scroll_direction == SCROLL_DOWN:
			scroll_dir="above"
		else:
			scroll_dir="above"
		# Take the correct line to focus, according to
		# the scroll offset.
		focus_pos = self.totalLines() - 1 - offset
		# Adjust the focus position.
		if focus_pos < 0:
			focus_pos = 0
		if focus_pos >= self.totalLines():
			focus_pos = self.totalLines() - 1		
		if len(self.widgetLinesList) > 0:
			# Set the focus to the selected line.
			self.widgetListBox.set_focus(focus_pos, coming_from=scroll_dir)


	def setFocusToLastLine(self):
		self.updateFocus(0, SCROLL_DOWN)


	def setFocusToFirstLine(self):
		self.updateFocus(self.totalLines() - 1, SCROLL_UP)


	def scrollPageStart(self):
		self.setFocusToFirstLine()
		self._scrollOffset = (self.totalLines() - 1)


	def scrollPageFinish(self):
		self.setFocusToLastLine()
		self._scrollOffset = 0


	def scrollUp(self, incr, geometry):
		if self._scrollOffset == 0:
			added_incr = self._first_non_visible_line_pos(SCROLL_UP, geometry)[0]
		else:
			added_incr = 0		
		self._scroll_up(incr + added_incr, SCROLL_UP)


	def scrollDown(self, incr, geometry):
		if self._scrollOffset == (self.totalLines() - 1):
			added_incr = self._first_non_visible_line_pos(SCROLL_DOWN, geometry)[0]
		else:
			added_incr = 0		
		self._scroll_down(incr + added_incr, SCROLL_UP)


	def scrollPageUp(self, geometry):
		result     = self._first_non_visible_line_pos(SCROLL_UP, geometry)
		increment  = result[0]
		turn       = result[1]
		self._scroll_up(increment, SCROLL_DOWN)
		if turn:
			self._scroll_down(1, SCROLL_DOWN)


	def scrollPageDown(self, geometry):
		result     = self._first_non_visible_line_pos(SCROLL_DOWN, geometry)
		increment  = result[0]
		turn       = result[1]
		self._scroll_down(increment, SCROLL_UP)
		if turn:
			self._scroll_up(1, SCROLL_DOWN)


	def bufferAddLineText(self, text, text_style = "normal_color"):
		# Create a new urwid.Text widget, with the text
		# we want to add.
		new_text_line = LineText(text_style, text)
		# If we have more lines than we want it, let's cut it.
		if self.maxLines > 0 and len(self.widgetLinesList) > self.maxLines:
			del cur_page_text_list[0]
		# Append the newly created widget object
		self.widgetLinesList.append(new_text_line.widget)


	def bufferClear(self):
		while True:
			if len(self._widgetLinesList) == 0:
				return
			self._widgetLinesList.pop()


	def bufferSaveToFile(self, file_path, append = True):
		if len(self._widgetLinesList) == 0:
			return False
		if append:
			mode = "a"
		else:
			mode = "w"
		try:
			fd = open(file_path, mode)
		except IOError:
			return False
		else:
			buffer_lines = []
			for text_widget in self._widgetLinesList:
				buffer_lines.append(text_widget.text)
			final_buffer = "\n".join(buffer_lines)
			final_buffer += "\n"
			with fd:
				fd.write(final_buffer)
		return True


