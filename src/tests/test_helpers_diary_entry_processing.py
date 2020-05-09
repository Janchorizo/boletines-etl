import pytest
import lxml
from helpers.boe_diary_entry_processing import get_labels_from_tree
from helpers.boe_diary_entry_processing import get_reference_details
from helpers.boe_diary_entry_processing import get_references_from_tree

class TestGetLabelsFromTree:
    def test_none(self):
        with pytest.raises(TypeError):
            get_labels_from_tree(None)

    def test_wrong_type(self):
        with pytest.raises(TypeError):
            get_labels_from_tree(dict())

    def test_empty_labels(self):
        node = lxml.etree.fromstring('<xml></xml>'.encode('UTF-8'))
        assert len(get_labels_from_tree(node)) == 0

class TestGetReferenceDetails:
    def test_none(self):
        with pytest.raises(TypeError):
            get_reference_details(None)

    def test_wrong_type(self):
        with pytest.raises(TypeError):
            get_reference_details(dict())

    def test_empty_labels(self):
        node = lxml.etree.fromstring('<xml></xml>'.encode('UTF-8'))
        assert get_reference_details(node) == {}

class TestGetReferencesFromTree:
    def test_none(self):
        with pytest.raises(TypeError):
            get_references_from_tree(None)

    def test_wrong_type(self):
        with pytest.raises(TypeError):
            get_references_from_tree(dict())

    def test_empty_labels(self):
        node = lxml.etree.fromstring('<xml></xml>'.encode('UTF-8'))
        assert len(get_references_from_tree(node)) == 0