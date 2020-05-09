import pytest
from helpers import boe

from tasks.save_boe_diary_entry import entry_id_2_output_path
from tasks.save_boe_diary_entry import SaveOption
from tasks.save_boe_diary_entry import SaveEntryToS3
from tasks.save_boe_diary_entry import SaveEntryToDB
from tasks.save_boe_diary_entry import IndexEntryInES
from tasks.save_boe_diary_entry import SaveBoeDiaryEntry


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
        path = './diary_entries/boe_diary_entry_processed_BOE-B-2020-13286.xml'
        assert entry_id_2_output_path('BOE-B-2020-13286', './') == path

class TestSaveOption:
    def test_properties(self):
        properties = dict(map(lambda property: (property.name, property.value), SaveOption))
        assert properties['DATABASE'] == 1
        assert properties['ELASTICSEARCH'] == 2
        assert properties['S3'] == 3

class TestSaveBoeDiaryEntry:
    def test_no_save_options(self):
        task = SaveBoeDiaryEntry(entry={})
        assert len(task.requires()) == 1

    def test_s3(self):
        task = SaveBoeDiaryEntry(entry={})
        assert len(task.requires()) == 1