#!/usr/bin/env python3
import urwid
import collections
from .common              import *
from .timer_callbacks     import _prompt_flash_callback


class Prompt(urwid.WidgetWrap):

	def __init__(self, prompt_caption = None):
		self.saveCommandHistory         = True
		self.tabCompletion              = True
		self.flashSeconds               = 0.25
		self.maxCommandHistory          = 0
		if prompt_caption:
			self.promptCaption            = prompt_caption
		else:
			self.promptCaption            = DEFAULT_PROMPT_CAPTION

		self.widget                     = urwid.Edit(self.promptCaption, "", multiline=False)
		self.loop                       = None
		self.style                      = "prompt_color6"
		self.styleFlash                 = "prompt_color_flash6"

		self._commandLines              = collections.deque()
		self._commandIndex              = -1

		self._autoCompleteWords         = []
		self._promptFlashTimerHandle    = None
		self._promptFlashActive         = False
		self._w                         = self.widget

	#
	# Internal Functions.
	#
	def _prompt_flash_on_off(self):
		self._promptFlashActive  = not self._promptFlashActive
		if self._promptFlashActive:
			self._prompt_flash_set_on()
		else:
			self._prompt_flash_set_off()


	def _prompt_flash_set_on(self):
		prompt_text = self.widget.caption
		self.widget.set_caption((self.styleFlash, prompt_text))


	def _prompt_flash_set_off(self):
		prompt_text = self.widget.caption
		self.widget.set_caption((self.style, prompt_text))


	def _prompt_flash_continue_timer(self):
		if self.loop:
			current_handle = self._promptFlashTimerHandle
			if current_handle:
				self.loop.remove_alarm(current_handle)
				new_handle = self.loop.set_alarm_in(self.flashSeconds, _prompt_flash_callback, user_data=self)
				self._promptFlashTimerHandle = new_handle

	#
	# Text Functions.
	#
	def getText(self):
		return self.widget.edit_text


	def setText(self, text):
		self.clearText()
		self.widget.insert_text(text)


	def appendText(self, text):
		self.widget.insert_text(text)


	def clearText(self):
		old_text = self.widget.edit_text
		self.widget.edit_text = ""


	def getLastWord(self):
		command_text = self.widget.edit_text
		if len(command_text) == 0:
			return ""
		command_text_list = command_text.split(" ")
		return command_text_list[-1]


	def completeLastWord(self):
		if len(self._autoCompleteWords) > 0:
			last_word = self.getLastWord()
			if last_word != "":
				completed_word_list = self.autocompletionCompleteWord(last_word)
				total_suggestions = len(completed_word_list)
				if total_suggestions == 1 and completed_word_list[0][1] > 0:
					suggested_word = completed_word_list[0][0]
					final_text_to_add = suggested_word[len(last_word):] + " "
					self.appendText(final_text_to_add)
				elif total_suggestions > 1:
					# TODO: implement this! display more choices
					return
				else:
					return

	#
	# Caption Functions.
	#
	def setCaption(self, caption):
		self.widget.set_caption(caption)


	def setCaptionWithStyle(self, caption, palette_entry_name):
		self.widget.set_caption((palette_entry_name, caption))


	def setCaptionStyle(self, palette_entry_name):
		caption = self.widget.caption
		self.widget.set_caption((palette_entry_name, caption))

	#
	# Flash Functions.
	#
	def startFlashing(self, loop):
		if loop and not self._promptFlashTimerHandle:
			self.loop = loop			
			self._promptFlashActive = True
			self._prompt_flash_on_off()
			new_handle = loop.set_alarm_in(self.flashSeconds, _prompt_flash_callback, user_data=self)
			self._promptFlashTimerHandle = new_handle


	def stopFlashing(self):
		if self.loop and self._promptFlashTimerHandle:
			self.loop.remove_alarm(self._promptFlashTimerHandle)
			self._promptFlashTimerHandle = None
			self._promptFlashActive = False
			self._prompt_flash_set_off()

	#
	# Auto-completion functions.
	#
	def autocompletionAddWord(self, word):
		if word and word != "":
			self._autoCompleteWords.append(str(word))


	def autocompletionAddWords(self, word_list):
		if word_list:
			for word in word_list:
				self.autocompletionAddWord(word)


	def autocompletionClearList(self):
		del self._autoCompleteWords[:]


	def autocompletionCompleteWord(self, incomplete_text):
		possible_completed = []
		for word in self._autoCompleteWords:
			if word.startswith(incomplete_text):
				possible_completed.append((word, len(word)))
		if len(possible_completed) > 0:
			possible_completed.sort(key=lambda tup: tup[1])
		return possible_completed

	#
	# Command History functions.
	#
	def commandHistoryGoToBegin(self):
		self._commandIndex = -1


	def commandHistoryGoUp(self):
		if len(self._commandLines) == 0:
			return
		self._commandIndex += 1
		if self._commandIndex > (len(self._commandLines) - 1):
			self._commandIndex = (len(self._commandLines) - 1)
		command_line_text = self._commandLines[self._commandIndex]
		self.setText(command_line_text)


	def commandHistoryGoDown(self):
		if len(self._commandLines) == 0 or self._commandIndex == -1:
			return		
		self._commandIndex -= 1
		if self._commandIndex == -1:
			self.clearText()
			return
		command_line_text = self._commandLines[self._commandIndex]
		self.setText(command_line_text)


	def commandHistoryClear(self):
		self._commandLines.clear()


	def commandHistorySaveToFile(self, file_path, append = True):
		if len(self._commandLines) == 0:
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
			hist_commands = "\n".join(self._commandLines)
			hist_command += "\n"
			with fd:
				fd.write(hist_commands)
		return True


	def saveCommandInHistory(self, command_text):
		# Check if the current command text is the same
		# as the last one inserted.
		total_command_lines = len(self._commandLines)
		if total_command_lines == 0 or command_text != self._commandLines[0]:
			# If the last command is not the same, let's
			# append the new command, and reset the command
			# index.
			self._commandLines.appendleft(command_text)
			self._commandIndex = -1
			# If we are dealing with a maximum numnber of
			# commands to save, let's pop the oldest one.
			if self.maxCommandHistory > 0 and total_command_lines > (self.maxCommandHistory):
				self._commandLines.pop()


