import datetime
import json
from urllib.parse import quote_plus

import luigi
from pymongo import MongoClient

from params.mongodb_params import MongoDBParams
from tasks.make_dash_data import MakeDashData


class SaveDashData(luigi.Task):
    collection = 'dash_data'
    date = luigi.DateParameter()

    def requires(self):
        return MakeDashData(date=self.date)

    def complete(self):
        formatted_date = '{:%Y-%m-%d}'.format(self.date)
        uri = "mongodb://{}:{}@{}:{}/{}".format(
            quote_plus(MongoDBParams().user),
            quote_plus(MongoDBParams().password),
            quote_plus(MongoDBParams().host),
            quote_plus(MongoDBParams().port),
            quote_plus(MongoDBParams().db)
        )
        
        client = MongoClient(uri)
        db = client[MongoDBParams().db]
        exists = db[self.collection].find_one({'date': formatted_date}) is not None
        client.close()

        return exists

    def run(self):
        with self.input().open() as f:
            summary = json.load(f)
        
        uri = "mongodb://{}:{}@{}:{}/{}".format(
            quote_plus(MongoDBParams().user),
            quote_plus(MongoDBParams().password),
            quote_plus(MongoDBParams().host),
            quote_plus(MongoDBParams().port),
            quote_plus(MongoDBParams().db)
        )
        client = MongoClient(uri)
        db = client[MongoDBParams().db]
        db[self.collection].insert_one(summary)
        client.close()
