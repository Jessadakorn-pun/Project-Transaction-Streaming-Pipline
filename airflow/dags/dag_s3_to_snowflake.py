import os
import logging
import boto3
import snowflake.connector
from datetime import datetime, timedelta
from airflow import DAG
from airflow.models import Variable 
from airflow.operators.python import PythonOperator
from common.logging import setup_logging
from config import *

# setting logger
setup_logging("transfrom-data-lake-to-snowflake.raw")
logger = logging.getLogger(__name__)

# get connection to minio
def get_minio_client():
    
    connection = boto3.client(
        "s3",
        endpoint_url=Variable.get("MINIO_ENDPOINT"),
        aws_access_key_id=Variable.get("MINIO_ACCESS_KEY"),
        aws_secret_access_key=Variable.get("MINIO_SECRET_KEY"),
    )
    
    return connection

# get connection to snowflake
def get_snowflake_connection():
    conn = snowflake.connector.connect(
        user=Variable.get("SNOWFLAKE_AIRFLOW_USER"),
        password=Variable.get("SNOWFLAKE_AIRFLOW_PASSWORD"),
        account=Variable.get("SNOWFLAKE_ACCOUNT"),
        warehouse=Variable.get("SNOWFLAKE_WAREHOUSE"),
        role=Variable.get("SNOWFLAKE_AIRFLOW_ROLE"),
        autocommit=True,
    )

    cur = conn.cursor()
    cur.execute(f"USE DATABASE {Variable.get('SNOWFLAKE_DB')}")
    cur.execute(f"USE SCHEMA {Variable.get('SNOWFLAKE_SCHEMA')}")
    cur.close()

    return conn
    
# discover new files in datalake
def discover_new_files(**context):
    
    os.makedirs(LOCAL_DIR, exist_ok=True)
    s3 = get_minio_client()
    
    bucket = Variable.get("MINIO_BUCKET")

    if not bucket:
        raise ValueError("MINIO_BUCKET is not set in Airflow Variables")
    
    last_loadded = Variable.get(
        "minio_last_loaded_ts",
        default_var="1970-01-01T00:00:00"
    )
    
    last_loaded_ts = datetime.fromisoformat(last_loadded)
    
    new_file = {}
    
    for table in TABLES:
        prefix = f"{table}/"
        response = s3.list_objects_v2(
            Bucket = bucket,
            Prefix = prefix
        )
        
        new_file[table] = []
        
        for obj in response.get("Contents", []):
            if obj["LastModified"].replace(tzinfo=None) > last_loaded_ts:
                local_path = f"{LOCAL_DIR}/{os.path.basename(obj['Key'])}"
                s3.download_file(bucket, obj["Key"], local_path)
                
                new_file[table].append(local_path)
                logger.info(f"Download {obj['Key']}")
                
    context["ti"].xcom_push(key="files", value=new_file)
    
# load file into snowflake raw layer
def load_snowflake(**context):
    files = context["ti"].xcom_pull(
        key="files", task_ids="discover_files"
    )
    
    stage = Variable.get("SNOWFLAKE_AIRFLOW_STAGE")
    db = Variable.get("SNOWFLAKE_DB")
    schema = Variable.get("SNOWFLAKE_SCHEMA")
    
    if not files:
        logger.info("No new file to load")
        return
    
    conn = get_snowflake_connection()
    cur = conn.cursor()
    
    for table, paths in files.items():
        if not paths:
            continue
        
        for path in paths:
            cur.execute(f"PUT file://{path} @{stage}/{table} AUTO_COMPRESS=FALSE")
        
        copy_sql = f"""
            COPY INTO {db}.{schema}.{table} (
                RAW_DATA,
                METADATA_FILENAME,
                LOADED_AT
            )
            FROM (
                SELECT
                    $1,
                    METADATA$FILENAME,
                    CURRENT_TIMESTAMP()
                FROM @{stage}/{table}/
            )
            FILE_FORMAT = (TYPE = PARQUET)
        """
        cur.execute(copy_sql)
        cur.execute(f"REMOVE @{stage}/{table}")
        
        logger.info(f"Loadded data into {table}")
    
    cur.close()
    conn.close()
    
    # update watermark
    Variable.set(
        "minio_last_loaded_ts",
        datetime.utcnow().isoformat()
    )


# DAG
default_args = {
    "owner": "data-platform",
    "retries": 2,
    "retry_delay": timedelta(minutes=2)
}

with DAG(
    dag_id = "minio_to_snowflake_datawarehouse",
    start_date = datetime(2025, 1, 1),
    schedule_interval = "*/5 * * * *",
    default_args = default_args,
    tags = ["cdc", "minio", "snowflake"]
) as dag:
    
    discover = PythonOperator(
        task_id = "discover_files",
        python_callable = discover_new_files,
        provide_context = True
    )
    
    load = PythonOperator(
        task_id = "load_snowflake",
        python_callable = load_snowflake,
        provide_context = True
    )
    
    # dependency
    discover >> load