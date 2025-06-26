resource "google_composer_environment" "ecommerce_airflow_env" {
  name   = "ecommerce-airflow-environment"
  region = var.gcp_region

  config {
    node_config {
      network         = google_compute_network.data_platform_vpc.id
      subnetwork      = google_compute_subnetwork.composer_snet.id
      service_account = google_service_account.composer_service_account.email
    }

    software_config {
      image_version = "composer-3-airflow-2.10.5"
    }

    environment_size = "ENVIRONMENT_SIZE_SMALL"
  }

  depends_on = [google_service_networking_connection.vpc_peering_to_google]
}