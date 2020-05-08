from os import path
import json

from lxml import etree as et
import luigi

from params.global_params import GlobalParams
from tasks.fetch_boe_diary_entry import FetchBoeDiaryEntry
from helpers import boe
from helpers import helpers
from helpers import boe_diary_entry_processing as processing

def entry_id_2_output_path (entry_id: str) -> str:
    return path.join(GlobalParams().base_dir,
                     'diary_entries', 
                     f"boe_diary_entry_processed_{entry_id}.json")

class ProcessBoeDiaryEntry(luigi.Task):
    entry_id = luigi.Parameter()
    entry_url = luigi.Parameter()

    def requires(self):
        return FetchBoeDiaryEntry(entry_id = self.entry_id,
                                  entry_url = self.entry_url)

    def output(self):
        return luigi.LocalTarget(entry_id_2_output_path(self.entry_id))

    def run(self):
        with self.input().open() as f:
            entry_content = f.read()
        
        tree = et.fromstring(entry_content.encode())
        labels = processing.get_labels_from_tree(tree)
        references = processing.get_references_from_tree(tree)

        print({'labels': labels, 'references': references})
                                
        with self.output().open('w') as f:
            json.dump({'labels': labels, 'references': references}, f)

