import luigi

class SFTPParams(luigi.Config):
    host = luigi.Parameter()
    user = luigi.Parameter()
    password = luigi.Parameter()
