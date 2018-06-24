#!/usr/bin/env python3
from .common           import *
from termapp.page      import Page


class Chapter():

	def __init__(self, chapter_name):
		self.pageList           = []
		self.currentPage        = Page()
		self.currentPageIndex   = 0
		self.name               = chapter_name
		self.pageList.append(self.currentPage)


	def totalPages(self):
		return len(self.pageList)


	def getPageFromIndex(self, page_index):
		if index < 0:
			return None
		if index >= len(self.pageList):
			return None
		return self.pageList[page_index]


	def createNewPage(self, page_title = DEFAULT_PAGE_TITLE, max_lines = DEFAULT_PAGE_MAX_LINES):
		page = Page(page_title, max_lines)
		self.pageList.append(page)
		return page


	def appendPage(self, page):
		self.pageList.append(page)


	def switchToNextPage(self):
		next_index = self.currentPageIndex + 1
		if next_index >= len(self.pageList):
			return False
		self.currentPageIndex = next_index
		self.currentPage = self.pageList[next_index]
		return True


	def switchToPrevPage(self):
		if self.currentPageIndex == 0:
			return False
		prev_index = self.currentPageIndex - 1
		self.currentPageIndex = prev_index
		self.currentPage = self.pageList[prev_index]
		return True


	def switchToNthPage(self, page_index):
		if page_index < 0:
			return False
		if page_index >= len(self.pageList):
			return False
		self.currentPageIndex = page_index
		self.currentPage = self.pageList[page_index]
		return True


