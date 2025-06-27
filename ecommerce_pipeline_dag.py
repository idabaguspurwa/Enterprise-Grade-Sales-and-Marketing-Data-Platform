import os
from datetime import datetime

from airflow.models.dag import DAG
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.sensors.gcs import GCSObjectsWithPrefixExistenceSensor

# --- CONFIGURATION VARIABLES ---
GCS_BUCKET_NAME = "ab-ecommerce-raw-data"
BIGQUERY_PROJECT = os.environ.get("GCP_PROJECT")
BIGQUERY_DATASET = "ecommerce_staging"

# --- EXPLICIT SCHEMA DEFINITIONS ---
ORDERS_SCHEMA = [
    {"name": "order_id", "type": "INTEGER", "mode": "REQUIRED"},
    {"name": "user_id", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "status", "type": "STRING", "mode": "NULLABLE"},
    {"name": "gender", "type": "STRING", "mode": "NULLABLE"},
    {"name": "created_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
    {"name": "returned_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
    {"name": "shipped_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
    {"name": "delivered_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
    {"name": "num_of_item", "type": "INTEGER", "mode": "NULLABLE"},
]

ORDER_ITEMS_SCHEMA = [
    {"name": "id", "type": "INTEGER", "mode": "REQUIRED"},
    {"name": "order_id", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "user_id", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "product_id", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "inventory_item_id", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "status", "type": "STRING", "mode": "NULLABLE"},
    {"name": "created_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
    {"name": "shipped_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
    {"name": "delivered_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
    {"name": "returned_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
    {"name": "sale_price", "type": "FLOAT", "mode": "NULLABLE"},
]

# --- DAG DEFINITION ---
with DAG(
    dag_id="ecommerce_elt_pipeline",
    start_date=datetime(2025, 6, 27),
    description="An ELT pipeline for e-commerce data from GCS to BigQuery Staging",
    schedule_interval=None,
    catchup=False,
    tags=["ecommerce", "gcs", "bigquery"],
) as dag:
    # --- SENSOR & LOAD TASKS ---
    wait_for_users_file = GCSObjectsWithPrefixExistenceSensor(task_id="wait_for_users_file", bucket=GCS_BUCKET_NAME, prefix="users/")
    load_users_to_staging = GCSToBigQueryOperator(task_id="load_users_to_staging", bucket=GCS_BUCKET_NAME, source_objects=["users/users_*.csv"], destination_project_dataset_table=f"{BIGQUERY_PROJECT}.{BIGQUERY_DATASET}.users", source_format="CSV", skip_leading_rows=1, autodetect=True, write_disposition="WRITE_TRUNCATE")
    
    wait_for_orders_file = GCSObjectsWithPrefixExistenceSensor(task_id="wait_for_orders_file", bucket=GCS_BUCKET_NAME, prefix="orders/")
    load_orders_to_staging = GCSToBigQueryOperator(task_id="load_orders_to_staging", bucket=GCS_BUCKET_NAME, source_objects=["orders/orders_*.csv"], destination_project_dataset_table=f"{BIGQUERY_PROJECT}.{BIGQUERY_DATASET}.orders", source_format="CSV", skip_leading_rows=1, schema_fields=ORDERS_SCHEMA, write_disposition="WRITE_TRUNCATE")
    
    wait_for_products_file = GCSObjectsWithPrefixExistenceSensor(task_id="wait_for_products_file", bucket=GCS_BUCKET_NAME, prefix="products/")
    load_products_to_staging = GCSToBigQueryOperator(task_id="load_products_to_staging", bucket=GCS_BUCKET_NAME, source_objects=["products/products_*.csv"], destination_project_dataset_table=f"{BIGQUERY_PROJECT}.{BIGQUERY_DATASET}.products", source_format="CSV", skip_leading_rows=1, autodetect=True, write_disposition="WRITE_TRUNCATE")

    # --- TASKS FOR ORDER_ITEMS ---
    wait_for_order_items_file = GCSObjectsWithPrefixExistenceSensor(task_id="wait_for_order_items_file", bucket=GCS_BUCKET_NAME, prefix="order_items/")
    load_order_items_to_staging = GCSToBigQueryOperator(task_id="load_order_items_to_staging", bucket=GCS_BUCKET_NAME, source_objects=["order_items/order_items_*.csv"], destination_project_dataset_table=f"{BIGQUERY_PROJECT}.{BIGQUERY_DATASET}.order_items", source_format="CSV", skip_leading_rows=1, schema_fields=ORDER_ITEMS_SCHEMA, write_disposition="WRITE_TRUNCATE")

    # --- TASK DEPENDENCIES ---
    wait_for_users_file >> load_users_to_staging
    wait_for_orders_file >> load_orders_to_staging
    wait_for_products_file >> load_products_to_staging
    wait_for_order_items_file >> load_order_items_to_staging