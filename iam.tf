# Create a dedicated Service Account for the Cloud Composer environment
resource "google_service_account" "composer_service_account" {
  account_id   = "composer-worker-sa" # Service Account ID
  display_name = "Service Account for Cloud Composer Environment"
}

# Give the Service Account the "Composer Worker" role, which is essential for it to operate.
resource "google_project_iam_member" "composer_worker_role" {
  project = var.gcp_project_id
  role    = "roles/composer.worker"
  member  = "serviceAccount:${google_service_account.composer_service_account.email}"
}

# Give the Service Account permission to read/write to our GCS buckets
resource "google_project_iam_member" "composer_storage_admin_role" {
  project = var.gcp_project_id
  role    = "roles/storage.admin" # For simplicity. In prod, you might use more granular roles.
  member  = "serviceAccount:${google_service_account.composer_service_account.email}"
}

# Give the Service Account permission to create and manage BigQuery jobs and data
resource "google_project_iam_member" "composer_bigquery_admin_role" {
  project = var.gcp_project_id
  role    = "roles/bigquery.admin" # For simplicity. In prod, you'd use roles like bigquery.dataEditor and bigquery.jobUser.
  member  = "serviceAccount:${google_service_account.composer_service_account.email}"
}