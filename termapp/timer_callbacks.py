#!/usr/bin/env python3

def _prompt_flash_callback(_loop, _data):
	_data._prompt_flash_on_off()
	_data._prompt_flash_continue_timer()


def _notifier_remove_callback(_loop, _data):
	_data.remove()


def _mainapp_call_timer_callback(_loop, _data):
	callback  =   _data[0]
	user_data =   _data[1]
	callback(user_data)


