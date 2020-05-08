import luigi

class GlobalParams(luigi.Config):
    base_dir = luigi.Parameter()
