from os import path
import luigi

from params.global_params import GlobalParams
from helpers import boe
from helpers import helpers

def entry_id_2_output_path (entry_id: str) -> str:
    return path.join(GlobalParams().base_dir,
                     'diary_entries', 
                     f"boe_diary_entry_raw_{entry_id}.xml")

class FetchBoeDiaryEntry(luigi.Task):
    entry_id = luigi.Parameter()
    entry_url = luigi.Parameter()

    def requires(self):
        return None

    def output(self):
        return luigi.LocalTarget(entry_id_2_output_path(self.entry_id))

    def run(self):
        url = boe.file_url_for_resource(self.entry_url)
        response = helpers.fetch_page(url)
        content = response.content.decode('utf-8')
                                
        with self.output().open('w') as f:
            f.write(content)

