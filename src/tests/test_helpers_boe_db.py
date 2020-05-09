import pytest
from helpers import boe_db

class TestBoeDiaryEntryQuery:
    def test_dict(self):
        item = {
            'id': 'a',
            'date': 'b',
            'title': 'c',
            'section': 'd',
            'department': 'e',
            'epigraph': 'f',
            'pdf_url': 'g',
            'xml_url': 'h',
            'htm_url': 'i'
        }

        query = "INSERT INTO boe_diary_entry" \
            "(id, date, title, section, department, epigraph, pdf_url, xml_url, htm_url)" \
            "VALUES ('a', 'b', 'c'," \
            "        'd', 'e', 'f'," \
            "        'g', 'h', 'i');"

        assert boe_db.boe_diary_entry_query(item) == query

    def test_just_id_and_section(self):
        item = {
            'id': 'a',
            'date': '',
            'title': '',
            'section': 'd',
            'department': '',
            'epigraph': '',
            'pdf_url': '',
            'xml_url': '',
            'htm_url': ''
        }

        query = "INSERT INTO boe_diary_entry" \
            "(id, date, title, section, department, epigraph, pdf_url, xml_url, htm_url)" \
            "VALUES ('a', '', ''," \
            "        'd', '', ''," \
            "        '', '', '');"

        assert boe_db.boe_diary_entry_query(item) == query

    def test_just_id(self):
        item = {
            'id': 'a',
            'date': '',
            'title': '',
            'section': '',
            'department': '',
            'epigraph': '',
            'pdf_url': '',
            'xml_url': '',
            'htm_url': ''
        }

        with pytest.raises(ValueError):
            boe_db.boe_diary_entry_query(item)

    def test_type_error(self):
        item = set()

        with pytest.raises(ValueError):
            boe_db.boe_diary_entry_query(item)

    def test_none(self):
        with pytest.raises(ValueError):
            boe_db.boe_diary_entry_query(None)

class TestBoeDiaryEntryIsValid:
    def test_dict(self):
        item = {
            'id': 'a',
            'date': 'b',
            'title': 'c',
            'section': 'd',
            'department': 'e',
            'epigraph': 'f',
            'pdf_url': 'g',
            'xml_url': 'h',
            'htm_url': 'i'
        }

        assert boe_db.boe_diary_entry_is_valid(item) == True

    def test_no_id(self):
        item = {
            'id': '',
            'date': 'b',
            'title': 'c',
            'section': 'd',
            'department': 'e',
            'epigraph': 'f',
            'pdf_url': 'g',
            'xml_url': 'h',
            'htm_url': 'i'
        }

        assert boe_db.boe_diary_entry_is_valid(item) == False

    def test_no_section(self):
        item = {
            'id': 'a',
            'date': 'b',
            'title': 'c',
            'section': '',
            'department': 'e',
            'epigraph': 'f',
            'pdf_url': 'g',
            'xml_url': 'h',
            'htm_url': 'i'
        }

        assert boe_db.boe_diary_entry_is_valid(item) == False

    def test_only_id_and_section(self):
        item = {
            'id': 'a',
            'date': '',
            'title': '',
            'section': 'b',
            'department': '',
            'epigraph': '',
            'pdf_url': '',
            'xml_url': '',
            'htm_url': ''
        }

        assert boe_db.boe_diary_entry_is_valid(item) == True

    def test_type_error(self):
        item = set()

        assert boe_db.boe_diary_entry_is_valid(item) == False

    def test_none(self):
        
        assert boe_db.boe_diary_entry_is_valid(None) is False
