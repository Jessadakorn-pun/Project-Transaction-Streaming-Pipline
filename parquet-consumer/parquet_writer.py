import os
import pandas as pd
from datetime import datetime

def write_parquet_idempotent(records: list[dict], table: str, offset: int, s3_client, bucket: str) -> None: 
    
    # checking record
    if not records:
        return

    # config object key in s3 bucket
    date = datetime.utcnow().strftime("%Y-%m-%d")
    s3_key = f"{table}/date={date}/offset={offset}.parquet"
    
    # idempotent check
    try:
        s3_client.head_object(Bucket=bucket, Key=s3_key)
        return # already written
    except Exception:
        pass
    
    # convert payload into dataframe and created as a temp file
    df = pd.DataFrame(records)
    temp_file = f"/tmp/{table}_{offset}.parquet"
    
    df.to_parquet(temp_file, index=False)
    
    # writing file to s3 bucket
    s3_client.upload_file(temp_file, bucket, s3_key)
    
    # clear temp file
    os.remove(temp_file)