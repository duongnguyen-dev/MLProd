variable "project_id" {
  description = "The project Id to host the cluster in"
  default = "savvy-surge-448015-g4"
}

variable "region" {
  description = "The region the cluster in"
  default = "asia-southeast1" # singapore
}

variable "k8s" {
  description = "GKE for ML prod"
  default     = "mlprod"
}

variable "machine_type" {
  description = "Machine type for the instance"
  default = "e2-standard-2"
}

variable "zone" {
  description = "Zone for the instance"
  default = "asia-southeast1-b"
}

# variable "boot_disk_image" {
#   description = "Boot disk image for the instance"
#   default = "ubuntu-os-cloud/ubuntu-2204-lts"
# }

variable "boot_disk_size" {
  description = "Boot disk size for the instance"
  default = 80
}

# variable "firewall_name" {
#   description = "Name of the firewall rule"
#   default     = "serving-grounding-dino-firewall" 
# }