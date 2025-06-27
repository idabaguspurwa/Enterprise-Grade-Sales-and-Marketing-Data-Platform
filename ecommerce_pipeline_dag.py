import os
from datetime import datetime

from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

# --- CONFIGURATION VARIABLES ---
GCS_BUCKET_NAME = "ab-ecommerce-raw-data"
BIGQUERY_PROJECT_ID = os.environ.get("GCP_PROJECT")
BIGQUERY_DATASET = "ecommerce_staging"
GIT_REPO_URL = "https://github.com/idabaguspurwa/Enterprise-Grade-Sales-and-Marketing-Data-Platform.git"
DBT_PROJECT_DIR = "/tmp/dbt_project"

# --- DAG DEFINITION ---
with DAG(
    dag_id="final_end_to_end_elt_pipeline",
    start_date=datetime(2025, 6, 27),
    description="A fully automated ELT pipeline that runs dbt via BashOperator",
    schedule_interval=None,
    catchup=False,
    tags=["production", "final"],
) as dag:
    
    start_pipeline = EmptyOperator(task_id="start_pipeline")

    load_tasks = [
        GCSToBigQueryOperator(task_id="load_users_to_staging", bucket=GCS_BUCKET_NAME, source_objects=["users/users_*.csv"], destination_project_dataset_table=f"{BIGQUERY_PROJECT_ID}.{BIGQUERY_DATASET}.users", source_format="CSV", skip_leading_rows=1, autodetect=True, write_disposition="WRITE_TRUNCATE"),
        GCSToBigQueryOperator(task_id="load_orders_to_staging", bucket=GCS_BUCKET_NAME, source_objects=["orders/orders_*.csv"], destination_project_dataset_table=f"{BIGQUERY_PROJECT_ID}.{BIGQUERY_DATASET}.orders", source_format="CSV", skip_leading_rows=1, schema_fields=[{"name": "order_id", "type": "INTEGER"}, {"name": "user_id", "type": "INTEGER"}, {"name": "status", "type": "STRING"}, {"name": "gender", "type": "STRING"}, {"name": "created_at", "type": "TIMESTAMP"}, {"name": "returned_at", "type": "TIMESTAMP"}, {"name": "shipped_at", "type": "TIMESTAMP"}, {"name": "delivered_at", "type": "TIMESTAMP"}, {"name": "num_of_item", "type": "INTEGER"}], write_disposition="WRITE_TRUNCATE"),
        GCSToBigQueryOperator(task_id="load_products_to_staging", bucket=GCS_BUCKET_NAME, source_objects=["products/products_*.csv"], destination_project_dataset_table=f"{BIGQUERY_PROJECT_ID}.{BIGQUERY_DATASET}.products", source_format="CSV", skip_leading_rows=1, autodetect=True, write_disposition="WRITE_TRUNCATE"),
        GCSToBigQueryOperator(task_id="load_order_items_to_staging", bucket=GCS_BUCKET_NAME, source_objects=["order_items/order_items_*.csv"], destination_project_dataset_table=f"{BIGQUERY_PROJECT_ID}.{BIGQUERY_DATASET}.order_items", source_format="CSV", skip_leading_rows=1, schema_fields=[{"name": "id", "type": "INTEGER"}, {"name": "order_id", "type": "INTEGER"}, {"name": "user_id", "type": "INTEGER"}, {"name": "product_id", "type": "INTEGER"}, {"name": "inventory_item_id", "type": "INTEGER"}, {"name": "status", "type": "STRING"}, {"name": "created_at", "type": "TIMESTAMP"}, {"name": "shipped_at", "type": "TIMESTAMP"}, {"name": "delivered_at", "type": "TIMESTAMP"}, {"name": "returned_at", "type": "TIMESTAMP"}, {"name": "sale_price", "type": "FLOAT"}], write_disposition="WRITE_TRUNCATE")
    ]

    load_complete = EmptyOperator(task_id="load_complete")

    # This single task incorporates YOUR fix to use the 'oauth' method.
    dbt_transform_task = BashOperator(
        task_id="dbt_transform_task",
        bash_command=f"""
            # Step 1: Clone the repository
            rm -rf {DBT_PROJECT_DIR}
            git clone --depth 1 {GIT_REPO_URL} {DBT_PROJECT_DIR}
            
            # Step 2: Create a brand new profiles.yml file using the oauth method
            echo "ecommerce_transforms:
              target: prod
              outputs:
                prod:
                  type: bigquery
                  method: oauth
                  project: {BIGQUERY_PROJECT_ID}
                  dataset: ecommerce_prod
                  threads: 4" > {DBT_PROJECT_DIR}/profiles.yml

            # Step 3: Run dbt build from inside the correct directory
            cd {DBT_PROJECT_DIR} && dbt build --profiles-dir .
        """
    )

    end_pipeline = EmptyOperator(task_id="end_pipeline")

    # --- TASK DEPENDENCIES ---
    start_pipeline >> load_tasks
    load_tasks >> load_complete
    load_complete >> dbt_transform_task
    dbt_transform_task >> end_pipeline