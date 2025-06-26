# Create a dedicated VPC network for our data platform
resource "google_compute_network" "data_platform_vpc" {
  name                    = "data-platform-vpc"
  auto_create_subnetworks = false # We want to control subnetwork creation
}

# Reserve a private IP range that Google's services (like Cloud SQL for Composer) can use
resource "google_compute_global_address" "private_ip_alloc" {
  name          = "private-ip-alloc-for-services"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  ip_version    = "IPV4"
  network       = google_compute_network.data_platform_vpc.id
  prefix_length = 16
}

# Create the VPC Peering connection between our VPC and Google's services network
resource "google_service_networking_connection" "vpc_peering_to_google" {
  network                 = google_compute_network.data_platform_vpc.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_alloc.name]
}

# --- ADD THIS NEW RESOURCE BLOCK ---
# Create a subnetwork inside our new VPC for Composer to use.
resource "google_compute_subnetwork" "composer_snet" {
  name          = "composer-snet"
  ip_cidr_range = "10.2.0.0/16"
  region        = var.gcp_region
  network       = google_compute_network.data_platform_vpc.id
}