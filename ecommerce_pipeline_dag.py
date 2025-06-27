import os
from datetime import datetime

from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

# --- CONFIGURATION VARIABLES ---
GCS_BUCKET_NAME = "ab-ecommerce-raw-data"
BIGQUERY_PROJECT = os.environ.get("GCP_PROJECT")
BIGQUERY_DATASET = "ecommerce_staging"
GIT_REPO_URL = "https://github.com/idabaguspurwa/Enterprise-Grade-Sales-and-Marketing-Data-Platform.git"
GIT_REPO_PATH = "/home/airflow/gcs/dags/Enterprise-Grade-Sales-and-Marketing-Data-Platform"
DBT_PROJECT_PATH = f"{GIT_REPO_PATH}/ecommerce_transforms"


# --- DAG DEFINITION ---
with DAG(
    dag_id="full_project_elt_pipeline",
    start_date=datetime(2025, 6, 27),
    description="Full ELT pipeline including dbt execution via BashOperator",
    schedule_interval=None,
    catchup=False,
    tags=["final", "ecommerce", "dbt"],
) as dag:
    
    start_pipeline = EmptyOperator(task_id="start_pipeline")

    # --- LOAD TASKS ---
    load_users_to_staging = GCSToBigQueryOperator(task_id="load_users_to_staging", bucket=GCS_BUCKET_NAME, source_objects=["users/users_*.csv"], destination_project_dataset_table=f"{BIGQUERY_PROJECT}.{BIGQUERY_DATASET}.users", source_format="CSV", skip_leading_rows=1, autodetect=True, write_disposition="WRITE_TRUNCATE")
    load_orders_to_staging = GCSToBigQueryOperator(task_id="load_orders_to_staging", bucket=GCS_BUCKET_NAME, source_objects=["orders/orders_*.csv"], destination_project_dataset_table=f"{BIGQUERY_PROJECT}.{BIGQUERY_DATASET}.orders", source_format="CSV", skip_leading_rows=1, schema_fields=[{"name": "order_id", "type": "INTEGER"}, {"name": "user_id", "type": "INTEGER"}, {"name": "status", "type": "STRING"}, {"name": "gender", "type": "STRING"}, {"name": "created_at", "type": "TIMESTAMP"}, {"name": "returned_at", "type": "TIMESTAMP"}, {"name": "shipped_at", "type": "TIMESTAMP"}, {"name": "delivered_at", "type": "TIMESTAMP"}, {"name": "num_of_item", "type": "INTEGER"}], write_disposition="WRITE_TRUNCATE")
    load_products_to_staging = GCSToBigQueryOperator(task_id="load_products_to_staging", bucket=GCS_BUCKET_NAME, source_objects=["products/products_*.csv"], destination_project_dataset_table=f"{BIGQUERY_PROJECT}.{BIGQUERY_DATASET}.products", source_format="CSV", skip_leading_rows=1, autodetect=True, write_disposition="WRITE_TRUNCATE")
    load_order_items_to_staging = GCSToBigQueryOperator(task_id="load_order_items_to_staging", bucket=GCS_BUCKET_NAME, source_objects=["order_items/order_items_*.csv"], destination_project_dataset_table=f"{BIGQUERY_PROJECT}.{BIGQUERY_DATASET}.order_items", source_format="CSV", skip_leading_rows=1, schema_fields=[{"name": "id", "type": "INTEGER"}, {"name": "order_id", "type": "INTEGER"}, {"name": "user_id", "type": "INTEGER"}, {"name": "product_id", "type": "INTEGER"}, {"name": "inventory_item_id", "type": "INTEGER"}, {"name": "status", "type": "STRING"}, {"name": "created_at", "type": "TIMESTAMP"}, {"name": "shipped_at", "type": "TIMESTAMP"}, {"name": "delivered_at", "type": "TIMESTAMP"}, {"name": "returned_at", "type": "TIMESTAMP"}, {"name": "sale_price", "type": "FLOAT"}], write_disposition="WRITE_TRUNCATE")

    load_complete = EmptyOperator(task_id="load_complete")

    # --- DBT TASKS ---
    clone_dbt_repo = BashOperator(
        task_id="clone_dbt_repo",
        bash_command=f"rm -rf {GIT_REPO_PATH} && git clone --depth 1 {GIT_REPO_URL} {GIT_REPO_PATH}"
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {DBT_PROJECT_PATH} && dbt run --profiles-dir .",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {DBT_PROJECT_PATH} && dbt test --profiles-dir .",
    )

    end_pipeline = EmptyOperator(task_id="end_pipeline")

    # --- TASK DEPENDENCIES ---
    start_pipeline >> [load_users_to_staging, load_orders_to_staging, load_products_to_staging, load_order_items_to_staging] >> load_complete
    load_complete >> clone_dbt_repo >> dbt_run >> dbt_test >> end_pipeline