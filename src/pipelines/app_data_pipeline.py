import os
import sys
import json
import luigi
import pymysql

from pipelines import no_indexing_boe_pipeline
from tasks.make_boe_diary_summary import MakeBoeDiarySummary


class AppDataPipeline(luigi.WrapperTask):
    date = luigi.DateParameter()

    def complete(self):
        return MakeBoeDiarySummary(date=self.date).complete()

    def requires(self):
        return None #no_indexing_boe_pipeline.Pipeline(date=self.date)

    def run(self):
        yield MakeBoeDiarySummary(date=self.date)

if __name__ == '__main__':
    luigi.run(['Pipeline',
        '--local-scheduler',
        '--workers', '3',
        '--GlobalParams-base-dir', './temp',
        '--date', sys.argv[1]
        ])
