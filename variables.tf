variable "gcp_project_id" {
  description = "The GCP project ID to deploy resources into."
  type        = string
  # Replace with your actual project ID from the GCP Console
  default     = "enterprisedata-464016"
}

variable "gcp_region" {
  description = "The GCP region for resources."
  type        = string
  # Choose a region close to you or a standard one like us-central1
  default     = "asia-southeast1"
}

variable "gcs_bucket_prefix" {
  description = "A unique prefix for your GCS buckets to avoid name clashes."
  type        = string
  # Use your name or initials to make it unique
  default     = "ab-ecommerce"
}