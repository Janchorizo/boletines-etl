from datetime import datetime
import pytest
from tasks.fetch_boe_diary_entry import FetchBoeDiaryEntry, entry_id_2_output_path
from params.global_params import GlobalParams

class TestEntryId2OutputPath:
    def test_none(self):
        with pytest.raises(TypeError):
            entry_id_2_output_path(None, None)
        with pytest.raises(ValueError):
            entry_id_2_output_path(None, 'x')
        with pytest.raises(TypeError):
            entry_id_2_output_path('x', None)

    def test_wrong_type(self):
        with pytest.raises(ValueError):
            entry_id_2_output_path(dict(), 'x')
        with pytest.raises(TypeError):
            entry_id_2_output_path('x', dict())

    def test_empty_id(self):
        with pytest.raises(ValueError):
            entry_id_2_output_path('', 'x')

    def test_invalid_id(self):
        with pytest.raises(ValueError):
            entry_id_2_output_path('BOCYL-A-2020-4859', '')
        with pytest.raises(ValueError):
            entry_id_2_output_path('BOE-B-2020', '')
        with pytest.raises(ValueError):
            entry_id_2_output_path('BOE-A-2020123', '')
        with pytest.raises(ValueError):
            entry_id_2_output_path('BOE-2-2020-13286', '')
        with pytest.raises(ValueError):
            entry_id_2_output_path(' BOE-A-2020-4859', '')

    def test_valid(self):
        path = './diary_entries/boe_diary_entry_raw_BOE-B-2020-13286.xml'
        assert entry_id_2_output_path('BOE-B-2020-13286', './') == path

class TestFetchBoeDiaryEntry: # TODO
    pass
