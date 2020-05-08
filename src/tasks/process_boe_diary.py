import datetime
import functools
from os import path
import json

from lxml import etree as et
import luigi

from params.global_params import GlobalParams
from tasks.fetch_boe_diary import FetchBoeDiary
from helpers import boe
from helpers import helpers
from helpers import boe_diary_processing

def date_2_output_path (date: datetime.datetime) -> str:
    return path.join(GlobalParams().base_dir,
                     'diaries', 
                     f"boe_diary_processed_{date.strftime('%d_%m_%Y')}.json")

class ProcessBoeDiary(luigi.Task):
    date = luigi.DateParameter()

    def requires(self):
        return FetchBoeDiary(date=self.date)

    def output(self):
        return luigi.LocalTarget(date_2_output_path(self.date))

    def run(self):
        with self.input().open() as f:
            diary_content = f.read()
        
        tree = et.fromstring(diary_content.encode())
        items = list(helpers.pipe(tree,
            boe_diary_processing.get_sections,
            boe_diary_processing.get_departments_per_section,
            boe_diary_processing.get_items_per_department,
            boe_diary_processing.get_details_per_item,
            functools.partial(map, lambda item: {**item, 'date':self.date.isoformat()})))
                                
        with self.output().open('w') as f:
            json.dump(items, f)

