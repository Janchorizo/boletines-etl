import datetime
from os import path
import json
import collections
import locale
import itertools

import pysftp
import matplotlib
from matplotlib import pyplot as plt
import pymysql
import luigi
from luigi.contrib.ftp import RemoteTarget

from params.sftp_params import SFTPParams
from helpers import boe
from helpers import helpers
from helpers import boe_diary_processing
from tasks.make_boe_diary_summary_graph import MakeBoeDiarySummaryGraph

def date_2_output_path (date: datetime.datetime) -> str:
    return path.join('files', 
                     f"boe_diary_summary_{date.strftime('%d_%m_%Y')}.png")

class SaveBoeDiarySummaryGraph(luigi.Task):
    date = luigi.DateParameter()

    def requires(self):
        return MakeBoeDiarySummaryGraph(self.date)

    def output(self):
        return luigi.LocalTarget(date_2_output_path(self.date))

    def complete(self):
        with pysftp.Connection(
                SFTPParams().host,
                username=SFTPParams().user,
                password=SFTPParams().password) as sftp:
            return sftp.exists(date_2_output_path(self.date))

    def run(self):
        with pysftp.Connection(
                SFTPParams().host,
                username=SFTPParams().user,
                password=SFTPParams().password) as sftp:
            return sftp.put(self.input().path, date_2_output_path(self.date))
