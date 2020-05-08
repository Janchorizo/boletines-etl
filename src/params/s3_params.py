import luigi

class S3Params(luigi.Config):
    aws_access_key_id = luigi.Parameter()
    aws_secret_access_key = luigi.Parameter() 
    aws_session_token = luigi.Parameter()
