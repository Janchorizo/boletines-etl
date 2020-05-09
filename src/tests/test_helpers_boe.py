from datetime import datetime
from helpers import boe

class TestSummaryUrlForDate:
	def test_date(self):
		date = datetime(2020, 5, 7)
		url = 'https://boe.es/diario_boe/xml.php?id=BOE-S-20200507'
		assert boe.summary_url_for_date(date) == url

	def test_none(self):
		assert boe.summary_url_for_date(None) == None

	def test_string(self):
		date = '2020-05-07'
		assert boe.summary_url_for_date(date) == None

class TestFileUrlForResource:
	def test_with_slash(self):
		resource = '/resource'
		url = 'https://www.boe.es/resource'
		assert boe.file_url_for_resource(resource) == url

	def test_without_slash(self):
		resource = '/resource'
		url = 'https://www.boe.es/resource'
		assert boe.file_url_for_resource(resource) == url

	def test_with_spaces(self):
		resource = '/reso urc e'
		assert boe.file_url_for_resource(resource) == None

	def test_none(self):
		assert boe.file_url_for_resource(None) == None

class TestIsValidDiaryEntryId:
	def test_none(self):
		assert boe.is_valid_diary_entry_id(None) == False

	def test_wrong_type(self):
		assert boe.is_valid_diary_entry_id(dict()) == False

	def test_valid(self):
		assert boe.is_valid_diary_entry_id('BOE-A-2020-4859') == True
		assert boe.is_valid_diary_entry_id('BOE-B-2020-13286') == True

	def test_invalid(self):
		assert boe.is_valid_diary_entry_id('BOCYL-A-2020-4859') == False
		assert boe.is_valid_diary_entry_id('BOE-B-2020') == False
		assert boe.is_valid_diary_entry_id('BOE-A-2020123') == False
		assert boe.is_valid_diary_entry_id('BOE-2-2020-13286') == False

	def test_with_spaces(self):
		assert boe.is_valid_diary_entry_id(' BOE-A-2020-4859') == False
		assert boe.is_valid_diary_entry_id('BOE-A-2020-4859 ') == False
		assert boe.is_valid_diary_entry_id('BOE- -2020-13286') == False