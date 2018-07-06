#!/usr/bin/env python3
from queue                import Queue


class WorkerQueue():

	def __init__(self):
		self.queue   = Queue()
		self.active  = True


	def run(self, callback = None):
		while self.active:
			task = self.queue.get()
			if callback:
				callback(task)
			else:
				self.onTask(task)
			self.queue.task_done()


	def completeTasks(self, callback = None):
		while not self.queue.empty():
			task = self.queue.get()
			if callback:
				callback(task)
			else:
				self.onTask(task)
			self.queue.task_done()


	def enqueueTask(self, task):
		self.queue.put(task)


	def start(self):
		self.active = True


	def stop(self):
		self.active = False
		self.queue.join()


	def onTask(self, task):
		pass


