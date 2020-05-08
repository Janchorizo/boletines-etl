import datetime
import json

import luigi
from luigi.contrib import s3

from params.s3_params import S3Params
from tasks.process_boe_diary import ProcessBoeDiary

def date_2_output_path (date: datetime.datetime):
    return f"boe_diary_processed_{date.strftime('%d_%m_%Y')}.json"

class SaveBoeDiary(luigi.Task):
    date = luigi.DateParameter()

    def requires(self):
        return ProcessBoeDiary(date=self.date)

    def output(self):
        client = s3.S3Client(aws_access_key_id = S3Params().aws_access_key_id, 
                             aws_secret_access_key = S3Params().aws_secret_access_key, 
                             aws_session_token = S3Params().aws_session_token)
        return s3.S3Target(date_2_output_path(self.date), None, client)

    def run(self):
        with self.input().open() as f:
            diary_content = f.read()
        
        with self.output().open('w') as f:
            f.write(json.dumps(items))
