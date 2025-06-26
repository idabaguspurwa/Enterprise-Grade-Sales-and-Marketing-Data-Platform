# This block tells Terraform we are using the "google" provider.
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.34" # Use a recent version
    }
  }
}

# This block configures the Google provider with your project details.
provider "google" {
  # Terraform will automatically find your project ID and region
  # from your gcloud configuration. You can also hardcode them here.
  project = var.gcp_project_id
  region  = var.gcp_region
}