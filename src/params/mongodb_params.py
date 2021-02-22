import luigi

class MongoDBParams(luigi.Config):
    db = luigi.Parameter(default='boe')
    port = luigi.Parameter(default='27017')
    host = luigi.Parameter()
    user = luigi.Parameter()
    password = luigi.Parameter()
