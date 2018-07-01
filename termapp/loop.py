#!/usr/bin/env python3
import urwid


class Loop(urwid.MainLoop):
	
	def __init__(self, main_application, palette):
		super().__init__(main_application, palette=palette, pop_ups=True)
		self.mainApplication = main_application

	#
	# Callback Functions
	#
	def entering_idle(self):
		super().entering_idle()
		self.mainApplication.onIdle()
		return True

	#
	# Main Functions
	#
	def flush(self):
		self.draw_screen()


