from datetime import datetime
import pytest
from tasks.fetch_boe_diary import FetchBoeDiary, date_2_output_path

class TestEntryId2OutputPath:
    def test_none(self):
        date = datetime(2020, 5, 7)

        with pytest.raises(TypeError):
            date_2_output_path(None, None)
        with pytest.raises(TypeError):
            date_2_output_path(None, 'x')
        with pytest.raises(TypeError):
            date_2_output_path(date, None)

    def test_wrong_type(self):
        date = datetime(2020, 5, 7)

        with pytest.raises(TypeError):
            date_2_output_path(dict(), 'x')
        with pytest.raises(TypeError):
            date_2_output_path(date, dict())

    def test_empty_base_dir(self):
        date = datetime(2020, 5, 7)

        with pytest.raises(TypeError):
            date_2_output_path(date)

    def test_valid(self):
        date = datetime(2020, 5, 7)
        path = './diaries/boe_diary_raw_07_05_2020.xml'
        assert date_2_output_path(date, './') == path

class TestFetchBoeDiary: # TODO
    pass