import datetime
from os import path
import json
import collections

import pymysql
import luigi

from params.global_params import GlobalParams
from params.db_params import DBParams
from helpers import boe
from tasks.save_boe_diary_summary_graph import SaveBoeDiarySummaryGraph

def date_2_output_path (date: datetime.datetime) -> str:
    return path.join(GlobalParams().base_dir,
                     'diary_summaries', 
                     f"boe_diary_summary_{date.strftime('%d_%m_%Y')}.json")

class MakeBoeDiarySummary(luigi.Task):
    date = luigi.DateParameter()
    table = 'boe_diary_entry'

    def requires(self):
        return SaveBoeDiarySummaryGraph(date=self.date)

    def output(self):
        return luigi.LocalTarget(date_2_output_path(self.date))

    def connect(self):
        connection = pymysql.connect(host=DBParams().host,
                                     user=DBParams().user,
                                     password=DBParams().password,
                                     db=DBParams().database)
        return connection

    def run(self):
        columns = 'id date title type_desc section department economic_impact'
        sql_columns = ', '.join(columns.split(' '))
        Entry = collections.namedtuple('Entry', columns)

        with self.connect() as connection:
            with connection.cursor() as cursor:
                status = cursor.execute(f"SELECT {sql_columns} FROM {self.table} WHERE date = '{self.date:%Y-%m-%d}';")
                if status == 0:
                    entries = None
                else:
                    entries = [Entry(*d) for d in cursor.fetchall()]
        
        if entries is None:
            raise Exception(f'Data is not available. DB status {status}')
        
        entry_type_count = collections.Counter(d.type_desc for d in entries)

        summary = {
            'date': f'{self.date:%Y-%m-%d}',
            'link': boe.summary_url_for_date(self.date),
            'entry_count': len(entries),
            'per_type_def_count': dict(entry_type_count),
            'economic_impact': sum(d.economic_impact for d in entries),
            'summary_graphic': {
                'sftp_file': self.input().path,
                'telegram_id': ''
            },
        }

        with self.output().open('w') as f:
            json.dump(summary, f)

