#!/usr/bin/env python3

def _prompt_flash_callback(_loop, _data):
		_data._prompt_flash_on_off()
		_data._prompt_flash_continue_timer()


def _header_hide_callback(_loop, _data):
		header_object, text_widget = _data
		new_list = []
		for entry in header_object.widget.contents:
			if entry[0] != text_widget:
				new_list.append(entry)
		header_object.widget.contents = new_list


