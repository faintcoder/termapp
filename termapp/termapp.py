#!/usr/bin/env python3
import urwid
from .common              import *
from .loop                import Loop
from .prompt              import Prompt
from .line_base           import LineBase
from .line_text           import LineText
from .line_progress       import LineProgress
from .page_base           import PageBase
from .page                import Page
from .header              import Header
from .footer              import Footer
from .geometry            import Geometry
from .chapter             import Chapter
from .chapter_manager     import ChapterManager
from .command             import Command
from .command_description import CommandDescription
from .command_dispatcher  import CommandDispatcher
from .dialog_base         import DialogBase
from .dialog_progress     import DialogProgress
from .dialog_text         import DialogText
from .dialog_user_pass    import DialogUserPass
from .worker_queue        import WorkerQueue
from .task_command        import TaskCommand
from .task_dialog         import TaskDialog
from .task_misc           import TaskExit
from .timer_entry         import TimerEntry


class TermApp(urwid.WidgetWrap):

	def __init__(
		self,
		prompt_caption                    = DEFAULT_PROMPT_CAPTION,
		create_header                     = True,
		create_footer                     = True,
		create_header_divider             = False
	):
		# Public properties.
		self.wheelScrollLines             = 1
		self.showPageDescription          = True
		self.pageDescriptionSeconds       = DEFAULT_PAGE_NOTIFIER_SECS
		self.quitOnESC                    = False
		self.quitDialogYesNo              = True
		self.commandSplitter              = ";"
		self.logger                       = None
		self.loop                         = None
		self.screen                       = None
		# Main application task queue.
		self.taskQueue                    = WorkerQueue()
		# Create the command dispatcher.
		self.commandDispatcher            = CommandDispatcher(self)
		# Register basic commands.
		quit_description                  = CommandDescription(name="quit", callback=self.quit, alias="q", params_ignore=True)
		self.commandDispatcher.registerCommand(quit_description)
		# Create prompt object
		self.prompt                       = Prompt(prompt_caption=prompt_caption)
		# Create chapters and pages.
		self.chapters                     = ChapterManager()
		# Get screen object and screen's cols/rows
		self.screen                       = urwid.raw_display.Screen()
		self.totalColumns                 = self.screen.get_cols_rows()[0]
		self.totalRows                    = self.screen.get_cols_rows()[1]
		# Create the header object.
		self.header                       = Header(create_text_header=create_header, 
																							create_divider=create_header_divider)
		# Create the footer object.
		self.footer                       = Footer(self.prompt.widget, create_text_footer=create_footer)
		#Get the current page `urwid.ListBox` object.
		self.body                         = self.chapters.getCurrentPage().widgetListBox
		# Create the main application window, the `urwid.Frame` object,
		# and assign it to the `urwid.WidgetWrap` internal `_w` variable,
		# so we can receive keyboard/mouse events.
		self.frame                        = urwid.Frame(
																										header      = self.header.widget,
																										body        = self.body,
																										footer      = self.footer.widget,
																										focus_part  = "footer"
																								 )
		self._w = self.frame
		# Get data to calculate urwid.Frame's body columns and rows,
		# and store the results in a `Geometry` object.
		# This is needed for the scrolling system.
		frame_padding                     = self._w.frame_top_bottom((1000,1000), True)[0]
		header_rows                       = frame_padding[0]
		footer_rows                       = frame_padding[1]
		body_rows                         = self.totalRows - (header_rows + footer_rows)
		body_columns                      = self.totalColumns
		self.geometry                     = Geometry(body_rows, body_columns, header_rows, footer_rows)
		# Create color palette.        foreground         background
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
				("highlight_color"        , "white"        , "black"          ),
				("error_color"            , "dark red"     , "black"          ),
				("notifier_color"         , "black"        , "yellow"         ),
				("warning_color"          , "yellow"       , "black"          ),
				("success_color"          , "light green"  , "black"          ),
				("fatal_color"            , "white"        , "light red"      ),
				("dialog_banner"          , "white"        , "dark red"       ),
				("dialog_background"      , "white"        , "dark gray"      ),
				("dialog_buttons"         , "black"        , "yellow"         ),
				("page_descriptor"        , "yellow"       , "dark gray"      ),
				("completed_progressbar"  , "black"        , "light magenta"  ),
				("uncompleted_progressbar", "white"        , "dark magenta"   ),
				("compl_waiting_color"    , "black"        , "yellow"         ),
				("compl_waiting_fl_color" , "white"        , "brown"          ),
				("compl_error_color"      , "white"        , "dark red"       ),
				("compl_success_color"    , "black"        , "light green"    ),
    ]
		# Private data
		self._pageNotifier     = None
		self._currentDialog    = None
		self._shownDialog      = False

	#
	# Urwid events callbacks.
	#
	def keypress(self, size, key):
		""" Urwid callback.
				This will be called for each keyboard event.
		"""
		# If a dialog is shown, send keyboard
		# input only to the dialog window.
		if self._shownDialog:
			self._currentDialog.keypress(size, key)
			return
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
			super().keypress(size, key)


	def mouse_event(self, size, event, button, col, row, focus):
		""" Urwid callback.
				This will be called for each mouse event.
		"""
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
		""" Termapp callback.
				This will be called for each keyboard event.
				Return `True` to pass through, or `False` to block the event.
		"""
		return True


	def onText(self, command_text):
		""" Termapp callback.
				This will be called every time the user types a command in the
				command line and presses return.
				Return `True` to pass through, or `False` to block the event.
		"""
		return True


	def onCommandError(self, command_name):
		""" Termapp callback.
				This will be called every time the user types a command in the
				command line and presses return, and the command is not a valid
				registered command.
				Return `True` to pass through, or `False` to block the event.
		"""
		self.printErr("ERR: Unknown command: %s." % (command_name))
		return True


	def onStart(self):
		""" Termapp callback.
				This will be called when the application is starting.
				This is the ideal time to register commands, and initialize
				stuff.
		"""
		return True


	def onExit(self):
		return True


	def onIdle(self):
		""" Termapp callback.
				This will be called when the application is doing nothing,
				and the loop is idling.
		"""
		# Execute all pending `Task` objects.
		self.processTasks()
		return True


	def onTask(self, task):
		""" Termapp callback.
				This will be called when the application has a `Task` object
				to execute.
		"""
		# Execute `Task` object.
		if not task.cancel:
			task.execute()
			# Refresh screen.
			self.flush()
		return True


	def onDataArrival(self):
		return True


	def onDialogResult(self, dialog):
		""" Termapp callback.
				This will be called when the user interacted with a dialog.
		"""
		must_exit = False
		# Implementing the Yes/No dialog that asks the user
		# to really quit or not.
		if (self.quitDialogYesNo == True 
				and dialog.tag == "_internal_quit_dialog"
				and dialog.result["button_caption"] == "Yes"):
			self.enqueueTask(TaskExit(main_application=self))
		return True


	def onPageChanged(self):
		""" Termapp callback.
				This will be called when the user changed the current page.
		"""
		if self.showPageDescription:
			current_page_string = self.chapters.getCurrentChapterString()
			if not self._pageNotifier or self._pageNotifier.expired:
				self._pageNotifier = self.header.createNotifier(
					text=current_page_string,
					seconds=self.pageDescriptionSeconds,
					style="page_descriptor"
				)
			else:
				self._pageNotifier.setText(current_page_string)
				self._pageNotifier.autoDestroy(seconds=self.pageDescriptionSeconds)
		return True

	#
	# Main Functions.
	#
	def start(self):
		""" Termapp function.
				This function will create the `urwid.Loop` object,
				and initialize everything.
		"""
		# Create the loop object.
		loop = Loop(main_application=self, palette=self._palette)
		# Set the loop object to the objects which needs it.
		if loop:
			if not loop.init():
				return False
			self.loop        = loop
			self.header.loop = loop
			self.footer.loop = loop
			self.prompt.loop = loop
		else:
			return False
		# Start CommandDispatcher object's stuff, like the
		# secondary thread where to run deferred commands.
		result = self.commandDispatcher.start()
		if not result:
			return False
		# Register on command error callback within the
		# CommandDispatcher object.
		self.commandDispatcher.onCommandError = self.onCommandError
		# Now that we have started all the facilities,
		# let's call user callback. If it will return
		# true, system will start.
		if self.onStart():
			return True
		return False


	def run(self):
		""" Termapp function.
				Start running the main loop.
		"""
		if self.loop:
			return self.loop.run()
		return False


	def quit(self):
		""" Termapp function.
				Quit gracefully the application.
				The main function to quit the application is `self.exit()`,
				but the user should call this to gracefully exit.
				E.g. display quit Yes/No dialog.
		"""
		if self.quitDialogYesNo:
			self.startDialogText(
				text             = "Are you sure to quit?",
				title            = "Quit?",
				tag              = "_internal_quit_dialog",
				buttons          = 2,
				button_captions  = ["No", "Yes"]
			)
		else:
			self.exit()


	def exit(self):
		""" Termapp function.
				Unload things, exit from the `urwid.Loop` and close the application.
		"""
		# Stop prompt from flashing, if necessary.
		if self.prompt.isFlashing():
			self.prompt.stopFlashing()
		# Call the `onExit` callback.
		self.onExit()
		# Stop the `CommandDispatcher` secondary
		# thread.
		self.commandDispatcher.stop()
		# Let the `Loop` object to do a graceful
		# exit.
		self.loop.gracefulExit()


	def flush(self):
		""" Termapp function.
				Flush the screen.
		"""
		self.loop.flush()


	def wakeup(self):
		""" Termapp function.
				If the `urwid.Loop` is sleeping, wake up it.
		"""
		self.loop.wakeup()


	def sendCommand(self, command_text):
		""" Termapp function.
				Calling this function is like typing a command to the command
				line and press enter.
				This function supports also multiple commands at once, with
				command splitting.
		"""
		# If null text specified as a command, return False.
		if len(command_text) == 0:
			return False
		# Create the final list of commands.
		command_list = []
		# Save the command in the prompt history.
		self.prompt.saveCommandInHistory(command_text)		
		# First of all, split the command line into ';'
		# tokens, so we can specify multiple commands
		# into a single line.
		if len(self.commandSplitter) != 1 or self.commandSplitter == " ":
			splitter = ";"
		else:
			splitter = self.commandSplitter
		command_text = command_text.split(splitter)
		# Add splitted commands to the final list.
		for command_line in command_text:
			if command_line == "":
				continue
			command_line = command_line.strip()
			command_list.append(command_line)
		# Then, for each command specified, let's have
		# command,params and enqueue that tuple into the
		# "commands to process" deque.
		for command_line in command_list:
			# Call the `onText` callback, and if it returns
			# true, we can process the command.
			if self.onText(command_line):
				# Create and append a `Task` object to the
				# main application task queue, that will
				# give the command line to the dispatcher.
				task = TaskCommand(
					main_application  = self,
					command_line      = command_line
				)
				self.enqueueTask(task)
		return True

	#
	# Task Functions.
	#
	def enqueueTask(self, task):
		""" Termapp function.
				Enqueue a `Task` object to be executed.
		"""
		self.taskQueue.enqueueTask(task)
		return True


	def enqueueTaskAndWakeup(self, task):
		""" Termapp function.
				Enqueue a `Task` object to be executed and wake up the main loop.
		"""
		self.enqueueTask(task)
		self.wakeup()
		return True


	def processTasks(self):
		""" Termapp function.
				Complete tasks execution.
				Each enqueue task will be completed and 'sent' to the callback
				of this app: `self.onTask()`.
		"""
		self.taskQueue.completeTasks(callback=self.onTask)
		return True

	#
	# Dialog Functions.
	#
	def startDialog(self, dialog):
		""" Termapp function.
				Start a new `Dialog` object that will overlay the application.
				Dialogs will "steal" mouse and keyboard input, until they won't
				be canceled.
		"""
		if self._shownDialog == True:
			return
		self._w.body = dialog.overlay
		self._w.set_focus("body")
		self._shownDialog      = True
		self._currentDialog    = dialog


	def startDialogText(
		""" Termapp function.
				Useful wrapper: start a `Dialog` object containing only text.
		"""
		self,
		text,		
		title            = "Warning!",
		tag              = "tag",
		buttons          = 2,
		button_captions  = ["OK", "Cancel"]
	):
		if self._shownDialog == True:
			return
		dialog = DialogText(
				self,
				text               = text,				
				title              = title,
				tag                = tag,
				buttons            = buttons,
				button_captions    = button_captions
			)
		self.startDialog(dialog)


	def startDialogUserPass(self, tag = "tag"):
		""" Termapp function.
				Useful wrapper: start a `Dialog` object containing user/pass input.
		"""
		if self._shownDialog == True:
			return
		dialog = DialogUserPass(self, tag=tag)
		self.startDialog(dialog)


	def cancelDialog(self):
		""" Termapp function.
				Cancel the `Dialog` object.
				User keyboard and mouse input will come back to the 'normal' application.
		"""
		if self._shownDialog == False:
			return
		self._w.body = self.body
		self._w.set_focus("footer")
		self._shownDialog      = False
		self._currentDialog    = None

	#
	# Palette Functions
	#
	def addPaletteColorEntry(self, palette_entry):
		""" Termapp function.
				Add a new palette color entry.
		"""
		self._palette.append(palette_entry)

	#
	# Page function.
	#
	def switchToNextPage(self):
		""" Termapp function.
				Switch to the next page of the current chapter.
		"""
		if self._shownDialog == True:
			return 
		result = self.chapters.currentChapter.switchToNextPage()
		if result:
			current_page = self.chapters.getCurrentPage()
			self._w.body = current_page.widgetListBox
		self.onPageChanged()


	def switchToPrevPage(self):
		""" Termapp function.
				Switch to the previous page of the current chapter.
		"""
		if self._shownDialog == True:
			return
		result = self.chapters.currentChapter.switchToPrevPage()
		if result:
			current_page = self.chapters.getCurrentPage()
			self._w.body = current_page.widgetListBox
		self.onPageChanged()


	def switchToNthPage(self, page_index):
		""" Termapp function.
				Switch to the Nth page of the current chapter.
		"""
		if self._shownDialog == True:
			return
		result = self.chapters.currentChapter.switchToNthPage(page_index)
		if result:
			current_page = self.chapters.getCurrentPage()
			self._w.body = current_page.widgetListBox
		self.onPageChanged()


	def switchToChapter(self, chapter_name):
		""" Termapp function.
				Switch to another chapter.
		"""
		if self._shownDialog == True:
			return 
		self.chapters.switchToChapter(chapter_name)
		self.onPageChanged()

	#
	# Print Functions.
	#
	def print(self, text, style = "normal_color"):
		""" Termapp function.
				Useful wrapper: add a line to the current page with the
				text and style specified as parameters.
				This function will also split multiple lines passed with
				the `\n` character.
		"""
		text_string = str(text)
		splitted_text = text_string.split("\n")
		for line in splitted_text:
			self.currentPageAppendText(line, style)


	def printHighlight(self, text):
		""" Termapp function.
				Useful wrapper: like print, but will add text with
				highlight style.
		"""
		self.print(text, "highlight_color")


	def printErr(self, text):
		""" Termapp function.
				Useful wrapper: like print, but will add text with
				error style.
		"""
		self.print(text, "error_color")


	def printWarn(self, text):
		""" Termapp function.
				Useful wrapper: like print, but will add text with
				warning style.
		"""
		self.print(text, "warning_color")


	def printSuccess(self, text):
		""" Termapp function.
				Useful wrapper: like print, but will add text with
				success style.
		"""
		self.print(text, "success_color")


	def currentPageAppendLine(self, line):
		""" Termapp function.
				Append a new `Line` object to the current page of the current chapter.
		"""
		current_page = self.chapters.getCurrentPage()
		current_page.bufferAddLine(line)
		current_page.setFocusToLastLine()


	def currentPageAppendText(self, text, style = "normal_color"):
		""" Termapp function.
				Append a new line of text to the current page.
		"""
		current_page = self.chapters.getCurrentPage()
		current_page.bufferAddLineText(text, style)
		current_page.setFocusToLastLine()


	def pageAppendText(self, page_index, text, style = "normal_color"):
		""" Termapp function.
				Append a new line of text to a certain page within the current chapter.
		"""
		chapter = self.chapters.getCurrentChapter()
		if chapter:
			page = chapter.getPageFromIndex(page_index)
			if page:
				page.bufferAddLineText(text, style)
				current_page = self.chapters.getCurrentPage()
				if page == current_page:
					page.setFocusToLastLine()


	def appendText(self, chapter_name, page_index, text, style = "normal_color"):
		""" Termapp function.
				Append a new line of text to a page of a chapter.
		"""
		chapter = self.chapters.getChapter(chapter_name)
		if chapter:
			page = chapter.getPageFromIndex(page_index)
			if page:
				page.bufferAddLineText(text, style)
				current_page = self.chapters.getCurrentPage()
				if page == current_page:
					page.setFocusToLastLine()


