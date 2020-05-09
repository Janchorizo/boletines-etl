import os
import luigi

from params.global_params import GlobalParams
from helpers import boe
from helpers import helpers

def entry_id_2_output_path (entry_id: str, base_dir: str) -> str:
    '''Create local filesystem path for the diary entry output.'''

    if not isinstance(base_dir, str): 
        raise TypeError(f'Expected a str and got a {type(base_dir)} for base_dir.')

    if not boe.is_valid_diary_entry_id(entry_id):
        raise ValueError(f"'{entry_id}' is not a valid entry id.")

    return os.path.join(base_dir,
                     'diary_entries', 
                     f"boe_diary_entry_raw_{entry_id}.xml")

class FetchBoeDiaryEntry(luigi.Task):
    entry_id = luigi.Parameter()
    entry_url = luigi.Parameter()

    def requires(self):
        return None

    def output(self):
        path = entry_id_2_output_path(self.entry_id, GlobalParams().base_dir)
        return luigi.LocalTarget(path)

    def run(self):
        url = boe.file_url_for_resource(self.entry_url)
        response = helpers.fetch_page(url)
        content = response.content.decode('utf-8')
                                
        with self.output().open('w') as f:
            f.write(content)
