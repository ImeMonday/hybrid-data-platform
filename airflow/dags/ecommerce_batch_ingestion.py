from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
from clickhouse_driver import Client

# ClickHouse connection
client = Client(
    host='clickhouse',
    user='admin',
    password='admin123'
)

# CSV path inside container
CSV_PATH = "/opt/airflow/data/raw/ecommerce_data.csv"

def load_csv_to_clickhouse():
    # Read CSV
    df = pd.read_csv(CSV_PATH)

    # Keep only required columns
    columns = [
        'InvoiceNo', 'StockCode', 'Description', 'Quantity',
        'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country'
    ]
    df = df[columns]

    # 1. Clean String/Text columns and safely handle missing/NaN values
    # In retail/ecommerce datasets, CustomerID often parses as a float (e.g., 17850.0).
    # We convert it cleanly to an integer string, mapping NaNs to an empty string.
    df['CustomerID'] = df['CustomerID'].fillna(0).astype(int).astype(str).replace('0', '')
    df['InvoiceNo'] = df['InvoiceNo'].astype(str).fillna('')
    df['StockCode'] = df['StockCode'].astype(str).fillna('')
    df['Description'] = df['Description'].fillna('')
    df['Country'] = df['Country'].fillna('')

    # 2. Enforce precise numeric types (avoids passing NumPy types to the driver)
    df['Quantity'] = df['Quantity'].fillna(0).astype(int)
    df['UnitPrice'] = df['UnitPrice'].fillna(0.0).astype(float)
    df['InvoiceDate'] = df['InvoiceDate'].astype(str)

    # 3. Convert DataFrame to a list of native Python tuples
    # This completely bypasses NumPy's internal typing system which breaks clickhouse-driver's .encode()
    records = [tuple(x) for x in df.to_numpy()]

    # Insert into ClickHouse
    client.execute(
        """
        INSERT INTO bronze.ecommerce_orders
        (
            InvoiceNo,
            StockCode,
            Description,
            Quantity,
            InvoiceDate,
            UnitPrice,
            CustomerID,
            Country
        )
        VALUES
        """,
        records
    )

    print(f"Successfully inserted {len(records)} rows into ClickHouse.")

default_args = {
    'owner': 'airflow'
}

with DAG(
    dag_id='ecommerce_batch_ingestion',
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule='@daily',
    catchup=False,
    tags=['ecommerce', 'batch'],
) as dag:

    ingest_task = PythonOperator(
        task_id='load_csv_data',
        python_callable=load_csv_to_clickhouse
    )

    ingest_task