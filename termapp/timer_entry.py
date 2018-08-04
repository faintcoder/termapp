#!/usr/bin/env python3


def _timer_entry_main_callback(_loop, _data):
	# Get the `TimerEntry` and the `Loop` objects.
	timer_entry    = _data[0]
	termapp_loop   = _data[1]
	# Increment timer repeats.
	timer_entry.times += 1
	# Switch the `on` parameter. This is useful to
	# implement flashing effects.
	timer_entry.on = not timer_entry.on
	# Remove the previous timer handle.
	termapp_loop.cancelTimer(timer_entry)
	# Call the timer callback.
	fn = timer_entry.callback
	fn(timer_entry)
	# Check if the
	# If the timer outmatched the repeats, do not start
	# it again.
	if timer_entry.repeats > 0 and timer_entry.times >= timer_entry.repeats:
		return
	# If the timer hasn't canceled, callback returned True,
	# and repeats are 0 or <= times, we will fire again
	# the timer.
	if not timer_entry.cancel:
		termapp_loop.startTimerEntry(timer_entry)


class TimerEntry():
	
	def __init__(
		self,
		seconds,
		callback,
		user_data       = None,
		repeats         = 0,
		tag             = "tag"
	):
		self.handle     = None       # The real handle of the timer, returned by `urwid.MainLoop`
		self.userData   = user_data  # User data
		self.tag        = tag        # Something that lets user to differentiate between same objects.
		self.seconds    = seconds    # Seconds timer will repeat
		self.callback   = callback   # User callback to call
		self.times      = 0          # Number of times the timer has been fired
		self.repeats    = repeats    # Total number of repeats timer must be repeated (0==infinite)
		self.cancel     = False      # Set this to True, if the timer will be canceled at the next fire
		self.on         = False      # Parameter that will be on/off/on/off... whenever the timer is fired. 


	def isActive(self):
		return (self.handle != None)


