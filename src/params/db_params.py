import luigi

class DBParams(luigi.Config):
    host = luigi.Parameter()
    user = luigi.Parameter()
    password = luigi.Parameter()
    database = luigi.Parameter()

