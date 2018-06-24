#!/usr/bin/env python3
import urwid
from .common           import *
from .prompt           import Prompt
from .line_base        import LineBase
from .line_text        import LineText
from .page_base        import PageBase
from .page             import Page
from .header           import Header
from .footer           import Footer
from .geometry         import Geometry
from .chapter          import Chapter
from .chapter_manager  import ChapterManager


class TermApp(urwid.WidgetWrap):

	def __init__(self, create_header = True, create_footer = True, create_header_divider = False):
		# Public properties.
		self.wheelScrollLines           = 1
		self.quitOnESC                  = True
		self.logger                     = None
		self.loop                       = None
		self.screen                     = None
		# Create prompt object
		self.prompt                     = Prompt()
		# Create chapters and pages.
		self.chapters                   = ChapterManager()
		# Get screen object and screen's cols/rows
		self.screen                     = urwid.raw_display.Screen()
		self.totalColumns               = self.screen.get_cols_rows()[0]
		self.totalRows                  = self.screen.get_cols_rows()[1]
		# Create the header object.
		self.header                     = Header(create_text_header=create_header, 
																							create_divider=create_header_divider)
		# Create the footer object.
		self.footer                     = Footer(self.prompt.widget, create_text_footer=create_footer)
		#Get the current page `urwid.ListBox` object.
		current_page_listbox = self.chapters.getCurrentPage().widgetListBox
		# Create the main application window, or the `urwid.Frame` object.
		self._w = urwid.Frame(header=self.header.widget,
                             body=current_page_listbox,
                             footer=self.footer.widget,
                             focus_part="footer")
		# Get data to calculate urwid.Frame's body columns and rows,
		# and store the results in a `Geometry` object.
		# This is needed for the scrolling system.
		frame_padding                   = self._w.frame_top_bottom((1000,1000), True)[0]
		header_rows                     = frame_padding[0]
		footer_rows                     = frame_padding[1]
		body_rows                       = self.totalRows - (header_rows + footer_rows)
		body_columns                    = self.totalColumns
		self.geometry                   = Geometry(body_rows, body_columns, header_rows, footer_rows)
		# Create color palette.
		self._palette = [
        ("prompt_color_flash"     , "black"        , "yellow"         ),
				("prompt_color"           , "light gray"   , "black"          ),
				("prompt_color_flash2"    , "black"        , "light blue"     ),
				("prompt_color2"          , "white"        , "dark blue"      ),
				("prompt_color_flash3"    , "black"        , "light red"      ),
				("prompt_color3"          , "white"        , "dark red"       ),
				("prompt_color_flash4"    , "black"        , "light green"    ),	
				("prompt_color4"          , "white"        , "dark green"     ),
				("prompt_color_flash5"    , "black"        , "light cyan"     ),	
				("prompt_color5"          , "white"        , "dark cyan"      ),
				("prompt_color_flash6"    , "black"        , "light magenta"  ),	
				("prompt_color6"          , "white"        , "dark magenta"   ),
        ("header_color"           , "light gray"   , "dark blue"      ),
				("footer_color"           , "white"        , "dark blue"      ),
        ("normal_color"           , "light gray"   , "black"          ),
				("error_color"            , "dark red"     , "black"          ),
				("warning_color"          , "yellow"       , "black"          ),
				("success_color"          , "light green"  , "black"          ),
				("fatal_color"            , "white"        , "light red"      )
    ]

	#
	# Urwid events callbacks.
	#
	def keypress(self, size, key):
		# Quit on ESC
		if key is "esc":
			if self.quitOnESC:
				self.quit()
		# Tab completion
		if key is "tab":
			self.prompt.completeLastWord()
		# Command entered
		if key == "enter":
			command_text = self.prompt.getText()
			self.prompt.clearText()			
			self.sendCommand(command_text)
		# Implement page up and dow.
		if key == "page up":
			page = self.chapters.getCurrentPage()
			page.scrollPageUp(self.geometry)
		if key == "page down":
			page = self.chapters.getCurrentPage()
			page.scrollPageDown(self.geometry)
		if key == "home":
			page = self.chapters.getCurrentPage()
			page.scrollPageStart()
		if key == "end":
			page = self.chapters.getCurrentPage()
			page.scrollPageFinish()
		# Address command line list.
		if key == "up":
			self.prompt.commandHistoryGoUp()
		if key == "down":
			self.prompt.commandHistoryGoDown()
		# If we are not pressing up or down arrow,
		# let's reset the command history to the
		# begin.
		if key not in ("up", "down"):
			self.prompt.commandHistoryGoToBegin()
		if self.onKeyPress(key):
			super(TermApp, self).keypress(size, key)


	def mouse_event(self, size, event, button, col, row, focus):
		if button in (4, 5):
			page = self.chapters.getCurrentPage()
			# Mousewheel has been rotated. Let's scroll.
			if button == 4:
				page.scrollUp(self.wheelScrollLines, self.geometry)
			if button == 5:
				page.scrollDown(self.wheelScrollLines, self.geometry) 
		else:
			# We need this function to be implemented like this, otherwise
			# if we click on the terminal screen, the `urwid.Edit` object
			# for command prompt, will lose focus, and the cursor will
			# disappear. We have to click on the edit to make it appear again.
			pass

	#
	# Local events callbacks.
	#
	def onKeyPress(self, key):
		return True


	def onCommand(self, command_text):
		self.bufferAppendLineTextToCurrentPage(command_text, "normal_color") # REMOVE THIS!
		return True


	def onStart(self, loop):
		return True

	#
	# Main functions.
	#
	def start(self):
		# Create the loop object.
		self.loop = urwid.MainLoop(self, palette = self._palette)
		if self.loop:
			if self.onStart(self.loop):
				return True
		return False


	def run(self):
		if self.loop:
			return self.loop.run()
		return False


	def quit(self):
		raise urwid.ExitMainLoop()


	def sendCommand(self, command_text):
		# If null text specified as a command, return False.
		if len(command_text) == 0:
			return False
		self.prompt.saveCommandInHistory(command_text)
		self.onCommand(command_text)
		return True

	#
	# Palette functions
	#
	def addPaletteColorEntry(self, palette_entry):
		self._palette.append(palette_entry)

	#
	# Page function.
	#
	def switchToNextPage(self):
		result = self.chapters.currentChapter.switchToNextPage()
		if result:
			current_page = self.chapters.getCurrentPage()
			self._w.body = current_page.widgetListBox


	def switchToPrevPage(self):
		result = self.chapters.currentChapter.switchToPrevPage()
		if result:
			current_page = self.chapters.getCurrentPage()
			self._w.body = current_page.widgetListBox


	def switchToNthPage(self, page_index):
		result = self.chapters.currentChapter.switchToNthPage(page_index)
		if result:
			current_page = self.chapters.getCurrentPage()
			self._w.body = current_page.widgetListBox


	def switchToChapter(self, chapter_name):
		self.chapters.switchToChapter(chapter_name)

	#
	# Buffer functions.
	#
	def currentPageAppendText(self, line_text, text_style = "normal_color"):
		current_page = self.chapters.getCurrentPage()
		current_page.bufferAddLineText(line_text, text_style)
		current_page.setFocusToLastLine()


	def pageAppendText(self, page_index, line_text, text_style = "normal_color"):
		chapter = self.chapters.getCurrentChapter()
		if chapter:
			page = chapter.getPageFromIndex(page_index)
			if page:
				page.bufferAddLineText(line_text, text_style)
				current_page = self.chapters.getCurrentPage()
				if page == current_page:
					page.setFocusToLastLine()


	def appendText(self, chapter_name, page_index, line_text, text_style = "normal_color"):
		chapter = self.chapters.getChapter(chapter_name)
		if chapter:
			page = chapter.getPageFromIndex(page_index)
			if page:
				page.bufferAddLineText(line_text, text_style)
				current_page = self.chapters.getCurrentPage()
				if page == current_page:
					page.setFocusToLastLine()


