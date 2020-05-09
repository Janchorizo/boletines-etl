'''FetchBoeDiary task for the retrieval of the diary summary.'''

import datetime
import os
import luigi

from params.global_params import GlobalParams
from helpers import boe
from helpers import helpers


def date_2_output_path(date: datetime.datetime, base_dir: str) -> str:
    '''Returns the local filesystem output location for the diary of the given date.'''

    if not isinstance(base_dir, str): 
        raise TypeError(f'Expected a str and got a {type(base_dir)} for base_dir.')

    if not isinstance(date, datetime.datetime):
        raise TypeError(f'Expected datetime.datetime and got {type(date)}')

    return os.path.join(base_dir,
                     'diaries',
                     f"boe_diary_raw_{date.strftime('%d_%m_%Y')}.xml")

class FetchBoeDiary(luigi.Task):
    '''Write the xml diary summary to the local file system for a given date.'''

    date = luigi.DateParameter()

    def output(self):
        output_path = date_2_output_path(self.date, GlobalParams().base_dir)
        return luigi.LocalTarget(output_path)

    def run(self):
        url = boe.summary_url_for_date(self.date)
        response = helpers.fetch_page(url)
        content = response.content.decode('utf-8')

        with self.output().open('w') as file:
            file.write(content)
