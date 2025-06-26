# Bucket for raw data files (your data lake)
resource "google_storage_bucket" "raw_data_bucket" {
  # Bucket names must be globally unique. We use a variable prefix to help.
  name          = "${var.gcs_bucket_prefix}-raw-data"
  location      = var.gcp_region
  force_destroy = true # Allows you to delete the bucket with terraform destroy even if it's not empty. Good for dev/test.

  # This setting makes all objects private by default.
  public_access_prevention = "enforced"
}

# Bucket for dbt to store logs and compiled code
resource "google_storage_bucket" "dbt_logs_bucket" {
  name          = "${var.gcs_bucket_prefix}-dbt-logs"
  location      = var.gcp_region
  force_destroy = true

  public_access_prevention = "enforced"
}

# Bucket for Cloud Composer to store DAG files
resource "google_storage_bucket" "airflow_dags_bucket" {
  name          = "${var.gcs_bucket_prefix}-airflow-dags"
  location      = var.gcp_region
  force_destroy = true

  public_access_prevention = "enforced"
}