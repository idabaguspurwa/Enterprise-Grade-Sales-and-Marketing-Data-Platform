# Staging dataset for raw, unprocessed data loaded from GCS
resource "google_bigquery_dataset" "ecommerce_staging" {
  dataset_id                  = "ecommerce_staging"
  friendly_name               = "E-Commerce Staging Data"
  description                 = "Dataset for raw data loaded from GCS before transformation"
  location                    = var.gcp_region
  delete_contents_on_destroy  = true # Similar to force_destroy for GCS. Good for dev/test.
}

# Production dataset for cleaned, transformed, analytics-ready data
resource "google_bigquery_dataset" "ecommerce_prod" {
  dataset_id                  = "ecommerce_prod"
  friendly_name               = "E-Commerce Production Mart"
  description                 = "Dataset for final, transformed data models ready for analysis"
  location                    = var.gcp_region
  delete_contents_on_destroy  = true
}