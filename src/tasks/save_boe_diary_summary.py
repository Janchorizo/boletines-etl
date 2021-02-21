import json
from enum import Enum
import pymysql
import luigi
from luigi.contrib import s3
from luigi.contrib import mysqldb

from params.s3_params import S3Params
from params.db_params import DBParams
from tasks.process_boe_diary_entry import ProcessBoeDiaryEntry
from helpers import boe_db

def entry_id_2_output_path (entry_id: str) -> str:
    return path.join(GlobalParams().base_dir,
                     'diary_entries', 
                     f"boe_diary_entry_raw_{entry_id}.xml")

class SaveBoeDiarySummary(luigi.Task):
    entry = luigi.DictParameter()
    table = 'boe_diary_entry'

    def requires(self):
        return ProcessBoeDiaryEntry(entry_id=self.entry.get('id'), 
                                    entry_url=self.entry.get('xml_url'))

    def get_target(self):
        return mysqldb.MySqlTarget(
            host = DBParams().host,
            database = DBParams().database,
            user = DBParams().user,
            password = DBParams().password,
            table = self.table,
            update_id=str(self.entry.get('id')))

    def output(self):
        return self.get_target()

    def complete(self):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"select * from boe_diary_entry where id = '{self.entry.get('id')}';")
                return len(cursor.fetchall()) == 1

    def get_sql_query(self):
        with self.input().open('r') as f:
            item = json.loads(f.read())
        item.update(self.entry)

        for k in item:
            if hasattr(item[k], 'replace'):
                item[k] = item[k].replace("'", '"')

        if not boe_db.boe_diary_entry_is_valid(item):
            print(item.keys())
            raise Exception('Entry does not meet requirements')

        return boe_db.boe_diary_entry_query(item)

    def connect(self):
        connection = pymysql.connect(host=DBParams().host,
                                     user=DBParams().user,
                                     password=DBParams().password,
                                     db=DBParams().database)
        return connection

    def run(self):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                query = self.get_sql_query()
                cursor.execute(query)
            connection.commit()
            self.get_target().touch()
