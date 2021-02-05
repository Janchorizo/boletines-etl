import os
import sys
import json
import luigi

from tasks.process_boe_diary import ProcessBoeDiary
from tasks.save_boe_diary_entry import SaveBoeDiaryEntry, SaveOption

class Pipeline(luigi.WrapperTask):
    date = luigi.DateParameter()

    @classmethod
    def bulk_complete(cls, parameter_tuples):
        return tuple()

    def complete(self):
        completed = True
        completed = completed and ProcessBoeDiary(date=self.date).complete()
        completed = completed and all(t.complete() for t in self.get_entry_tasks())
        return completed

    def requires(self):
        return ProcessBoeDiary(date=self.date)

    def get_entry_tasks(self):
        with self.input().open('r') as f:
            diary_entries = json.loads(f.read())
        
        return (SaveBoeDiaryEntry(entry=entry, save_options=(SaveOption.DATABASE.value,))
               for entry 
               in diary_entries)

    def run(self):
        yield self.get_entry_tasks()

if __name__ == '__main__':
    print(['Pipeline',
        '--local-scheduler',
        '--workers', '3',
        '--GlobalParams-base-dir', './temp',
        '--DBParams-host', 'localhost',
        '--DBParams-user', 'root',
        '--DBParams-password', 'pass',
        '--DBParams-database', 'boe',
        '--date', sys.argv[1]
        ])
    luigi.run(['Pipeline',
        '--local-scheduler',
        '--workers', '3',
        '--GlobalParams-base-dir', './temp',
        '--DBParams-host', 'localhost',
        '--DBParams-user', 'root',
        '--DBParams-password', 'pass',
        '--DBParams-database', 'boe',
        '--date', sys.argv[1]
        ])
