import datetime
import locale
from os import path
import json
import collections

import pymysql
import luigi

from params.global_params import GlobalParams
from params.db_params import DBParams
from helpers.helpers import shorttened


def date_2_output_path (date: datetime.datetime) -> str:
    return path.join(GlobalParams().base_dir,
                     'dash_data', 
                     f"dash_data_{date.strftime('%d_%m_%Y')}.json")

class MakeDashData(luigi.Task):
    date = luigi.DateParameter()
    table = 'boe_diary_entry'

    def requires(self):
        return None

    def output(self):
        return luigi.LocalTarget(date_2_output_path(self.date))

    def connect(self):
        connection = pymysql.connect(host=DBParams().host,
                                     user=DBParams().user,
                                     password=DBParams().password,
                                     db=DBParams().database)
        return connection

    def run(self):        
        # cost_by_department_barchart
        columns = 'id date title type_desc section department economic_impact'
        sql_columns = ', '.join(columns.split(' '))
        q = f"SELECT {sql_columns} FROM {self.table} WHERE date = '{self.date:%Y-%m-%d}';"
        Entry = collections.namedtuple('Entry', columns)

        with self.connect() as connection:
            with connection.cursor() as cursor:
                status = cursor.execute(q)
                if status == 0:
                    entries = None
                else:
                    entries = [Entry(*d) for d in cursor.fetchall()]
        
        if entries is None:
            raise Exception(f'Data is not available. DB status {status}')

        costs = {}
        for entry in entries:
            if entry.economic_impact > 0:
                costs[entry.department] = costs.setdefault(entry.department, 0) + entry.economic_impact

        barchart = {
            'x': tuple(costs.values()),
            'y': tuple(shorttened(x) for x in costs.keys()),
            'text': tuple(locale.currency(x, grouping=True) for x in costs.values()),
            'hover_name': tuple(costs.keys()),
            'non_null_count': len(costs)
        }

        # sankey
        q = f'''select GROUP_CONCAT(boe_diary_section.name), department, count(department) as count
            from boe_diary_entry, boe_diary_section
            where boe_diary_section.id = boe_diary_entry.section and boe_diary_entry.date = '{self.date:%Y-%m-%d}'
            group by department;
        '''
        Entry = collections.namedtuple('Entry', 'section department count')

        with self.connect() as connection:
            with connection.cursor() as cursor:
                status = cursor.execute(q)
                if status == 0:
                    entries = None
                else:
                    entries = [Entry(*d) for d in cursor.fetchall()]
        
        if entries is None:
            raise Exception(f'Data is not available. DB status {status}')

        section_names = tuple(set(entry.section for entry in entries))
        section_count = {
            section_name: sum(map(lambda x: x.count, filter(lambda x: x.section == section_name, entries)))
            for section_name
            in section_names
        }
        department_count = {entry.department: entry.count for entry in entries}
        department_names = tuple(department_count.keys())

        labels = (
            *[f'{shorttened(name, length=50)} ({section_count[name]})' for name in section_names],
            *[f'{shorttened(name, length=50)} ({department_count[name]})' for name in department_names]
        )

        sankey = {
            'labels': labels,
            'link_source': [section_names.index(x) for x, *_ in entries],
            'link_target': [len(section_names) + department_names.index(y) for x, y, _ in entries],
            'link_value': [count for *_, count in entries]
        }
        
        data = {
            'date': f'{self.date:%Y-%m-%d}',
            'barchart': barchart,
            'sankey': sankey
        }

        with self.output().open('w') as f:
            json.dump(data, f)
