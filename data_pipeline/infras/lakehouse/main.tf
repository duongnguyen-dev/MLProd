terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.80.0"
    }
  }
}

// The library with methods for creating and
// managing the infrastructure in GCP, this will
// apply to all the resources in the project
provider "google" {
  credentials = "./savvy-surge-448015-g4-62cc397bc79b.json" # Replace this with you key .json file
  project     = var.project_id
  region      = var.region
}

// Google Kubernetes Engine
resource "google_container_cluster" "mlprod-cluster" {
  name = "${var.project_id}-mlprod-gke"
  location = var.zone

  # We can't create a cluster with no node pool defined, but we want to only use
  # separately managed node pools. So we create the smallest possible default
  # node pool and immediately delete it.
  remove_default_node_pool = true 
  initial_node_count = 1
}

// Node pool: a group of VMs within the cluster, 
// and you can have multiple node pools with different configurations in the same cluster.
resource "google_container_node_pool" "mlprod-nodes" {
  name = "mlprod-node-pool"
  location = var.zone
  cluster = google_container_cluster.mlprod-cluster.name
  node_count = 3
  
  node_config {
    preemptible = true # similar to spot VMs 
    machine_type = var.machine_type
    disk_size_gb = var.boot_disk_size
  }
}

# resource "google_compute_firewall" "sgd-firewall" {
#   name = var.firewall_name
#   network = "default"

#   allow {
#     protocol = "tcp"
#     ports = ["30001"]
#   }

#   source_ranges = ["0.0.0.0/0"] // Allow all traffic
# }