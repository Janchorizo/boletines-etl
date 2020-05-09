import pytest
import lxml
from helpers import helpers

class TestPipe:
	def test_pipe(self):
		initial_value = 9
		functions = (
			lambda x: x+1,
			lambda x: x*2,
		)
		assert helpers.pipe(initial_value, *functions) == 20

	def test_none_initial_value(self):
		initial_value = None
		functions = (
			lambda x: x+1,
			lambda x: x*2,
		)

		with pytest.raises(TypeError):
			helpers.pipe(initial_value, *functions)

	def test_none_initial_value_2(self):
		initial_value = None
		functions = (
			lambda x: x,
		)

		assert helpers.pipe(initial_value, *functions) == None

	def test_no_arguments(self):
		assert helpers.pipe() == None

	def test_just_initial_value(self):
		initial_value = 10

		assert helpers.pipe(initial_value) == 10

	def test_just_initial_value_2(self):
		initial_value = None

		assert helpers.pipe(initial_value) == None

class TestResponse:
	def test_instantiation(self):
		helpers.Response(headers='', content='')

class TestFetchPage:
	def test_null_url(self):
		with pytest.raises(ValueError):
			helpers.fetch_page(None)

	def test_invalid_max_tries(self):
		with pytest.raises(ValueError):
			helpers.fetch_page('', 0)

	def test_null_url_and_max_tries(self):
		with pytest.raises(ValueError):
			helpers.fetch_page(None, -1)

class TestPrintResponseContent:
	def test_none_response(self):
		assert helpers.print_reponse_content(None) == None

	def test_wrong_response_type(self):
		with pytest.raises(TypeError):
			helpers.print_reponse_content('')

class TestTreeFromResponse:
	def test_tree(self):
		response = helpers.Response('', '<xml></xml>'.encode('UTF-8'))
		node = helpers.tree_from_response(response)
		assert type(node) is lxml.etree._Element

	def test_none_response(self):
		assert helpers.tree_from_response(None) == None

	def test_wrong_response_type(self):
		with pytest.raises(TypeError):
			helpers.tree_from_response('')

class TestUseTreeForSearch:
	def test_tree(self):
		node = lxml.etree.fromstring('<xml></xml>'.encode('UTF-8'))
		search = helpers.use_tree_for_search(node)
		assert callable(search) is True

	def test_none_response(self):
		assert helpers.use_tree_for_search(None) == None

	def test_wrong_response_type(self):
		with pytest.raises(TypeError):
			helpers.use_tree_for_search(dict())

class TestUseXpathForSearch:
	def test_tree(self):
		search = helpers.use_xpath_for_search('')
		assert callable(search) is True

	def test_none_response(self):
		assert helpers.use_xpath_for_search(None) == None

	def test_wrong_response_type(self):
		with pytest.raises(TypeError):
			helpers.use_xpath_for_search(dict())
