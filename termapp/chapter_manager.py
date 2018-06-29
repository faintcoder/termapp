#!/usr/bin/env python3
from .common              import *
from .chapter             import Chapter


class ChapterManager():

	def __init__(self, main_chapter_name = DEFAULT_MAIN_CHAPTER_NAME):
		self.chapters                        = {}
		self.mainChapterName                 = main_chapter_name
		self.chapters[main_chapter_name]     = Chapter(main_chapter_name)
		self.currentChapter                  = self.chapters[main_chapter_name]


	def createChapter(self, chapter_name):
		if chapter_name in self.chapters:
			return False
		self.chapters[chapter_name] = Chapter(chapter_name)
		return True


	def getCurrentPage(self):
		return self.currentChapter.currentPage


	def getChapter(self, chapter_name):
		if chapter_name not in self.chapters:
			return None
		return self.chapters[chapter_name]


	def createNewPage(self, page_title = DEFAULT_PAGE_TITLE, max_lines = DEFAULT_PAGE_MAX_LINES):
		new_page = self.currentChapter.createNewPage(page_title, max_lines)
		return new_page


	def appendPage(self, page):
		self.currentChapter.appendPage(page)


	def switchToChapter(self, chapter_name):
		if chapter_name not in self.chapters:
			return False
		self.currentChapter = self.chapters[chapter_name]


	def getCurrentChapterString(self):
		current_string        = "Chapters: {}, Current: {}"
		number_of_chapters    = str(len(self.chapters))
		page_string           = self.currentChapter.getCurrentPageString()
		return current_string.format(number_of_chapters, page_string)


