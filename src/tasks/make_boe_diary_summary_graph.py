import datetime
from os import path
import json
import collections
import locale
import itertools

import matplotlib
from matplotlib import pyplot as plt
import pymysql
import luigi

from params.global_params import GlobalParams
from params.db_params import DBParams
from helpers import boe
from helpers import helpers
from helpers import boe_diary_processing

def date_2_output_path (date: datetime.datetime) -> str:
    return path.join(GlobalParams().base_dir,
                     'diary_summaries', 
                     f"boe_diary_summary_{date.strftime('%d_%m_%Y')}.png")

class MakeBoeDiarySummaryGraph(luigi.Task):
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

    def create_graph(self, items, date):
        locale.setlocale(locale.LC_ALL,"")
        plt.style.use('fivethirtyeight')
        plt.rcParams['font.size'] = '21'
        fig = plt.figure(figsize=(15, 17))
        gs = matplotlib.gridspec.GridSpec(2, 2, width_ratios=[3, 3])

        sections = {k: 0 for k in boe.code_to_section_name.keys()}
        section_c = collections.Counter(itertools.chain((item.section for item in items)))
        sections = section_c

        sections_sorted = sorted(sections.items(), key=lambda x: x[1])
        section_labels = [f'{boe.code_to__formatted_section_name[k.lower()]} {v:-3}' for k, v in sections_sorted]

        ax0 = fig.add_subplot(gs[0, 0])
        ax0.barh(section_labels, [v for k, v in sections_sorted])
        ax0.set_title(f'{sum(section_c.values())} entradas en {len(section_c)} secciones ...', fontsize=21)
        ax0.set_xlabel('Número de entradas', fontsize=22)

        ax1 = fig.add_subplot(gs[0, 1], sharey=ax0)
        ax1.set_title(f'... con un gasto económico', fontsize=21)
        ax1.axis('off')
        for l, _ in enumerate(section_labels):
            with_cost = tuple(filter(lambda d: d.section == sections_sorted[l][0] and d.economic_impact > 0, items))
            cost = sum(d.economic_impact for d in with_cost)
            
            if cost > 0:
                cost_text = locale.currency(cost, grouping=True)
                ax1.text(0, l, f'{cost_text} entre {len(with_cost)} entradas', fontsize=21)
            else:
                ax1.text(0, l, f'Sin coste detectado.', fontsize=21)

        fig.suptitle(f'Resumen de la actividad en el BOE para el día {date:%d del %m, %Y}', fontsize=24)
        fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        return fig

    def run(self):
        columns = 'id title type_desc section department economic_impact'
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
        
        fig = self.create_graph(entries, self.date)
        fig.savefig(self.output().path, bbox_inches = 'tight', pad_inches = .5)
