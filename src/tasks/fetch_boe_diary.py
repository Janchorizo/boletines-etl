import datetime
from os import path
import luigi

from params.global_params import GlobalParams
from helpers import boe
from helpers import helpers

def date_2_output_path (date: datetime.datetime) -> str:
    return path.join(GlobalParams().base_dir,
                     'diaries', 
                     f"boe_diary_raw_{date.strftime('%d_%m_%Y')}.xml")

class FetchBoeDiary(luigi.Task):
    date = luigi.DateParameter()

    def requires(self):
        return None

    def output(self):
        return luigi.LocalTarget(date_2_output_path(self.date))

    def run(self):
        url = boe.summary_url_for_date(self.date)
        response = helpers.fetch_page(url)
        content = response.content.decode('utf-8')
                                
        with self.output().open('w') as f:
            f.write(content)

