
# The below script been referred or taken from below References and has been modified as per the value for the cluster.
# [1] "https://developer.hashicorp.com/terraform/tutorials/kubernetes/gke"
# [2] "https://developer.hashicorp.com/terraform/tutorials/kubernetes/kubernetes-provider"


#Below code from line 8-11 has been referred and taken from https://registry.terraform.io/providers/hashicorp/google/latest/docs
provider "google" {
  project     = "assignment3-k8s"
  region      = "us-central1"
}


#Below code from line 16-21 has been referred and taken from https://registry.terraform.io/providers/hashicorp/google/4.44.0/docs/resources/container_cluster.html

resource "google_container_cluster" "assignment3-cluster" {
  name               = "assignment3-cluster"
  location           = "us-central1-a"
  initial_node_count = 1

  remove_default_node_pool = true
}

#Below code from line 26-37 has been referred and taken from https://registry.terraform.io/providers/hashicorp/google-beta/latest/docs/guides/using_gke_with_terraform
#Below code from line 39-54 has been referred and taken from https://cloud.google.com/kubernetes-engine/docs/concepts/persistent-volumes
resource "google_container_node_pool" "assignment3-node-pool" {
  name       = "assignment3-node-pool"
  location   = "us-central1-a"
  cluster    = google_container_cluster.assignment3-cluster.name
  node_count = 1
  autoscaling {
    min_node_count = 1
    max_node_count = 3
  }
  node_config {
    machine_type = "n1-standard-2"
    disk_size_gb = 10
 
  }
}

#Below code from line 57-70 has been referred and taken from https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_firewall
resource "google_compute_firewall" "allow-http" {
  name        = "allow-http"
  network     = "default"
  direction   = "INGRESS"
  priority    = 1000
  
  allow {
    protocol = "tcp"
    ports    = ["80"]
  }
  
  source_ranges = ["0.0.0.0/0"] 
  target_tags   = [google_container_cluster.assignment3-cluster.name]
}



# Below code from line 75-77 has been referred and taken from https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/google_service_account.html
resource "google_service_account" "assignment3_service_account" {
  account_id   = "assignment3-cluster"
  display_name = "My Service Account"
}

#Below code from line 81-84 has been referred and taken from https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/google_project_iam.html
resource "google_project_iam_member" "artifact_registry_reader" {
  project = "assignment3-k8s"
  role    = "roles/artifactregistry.reader"
  member  = "serviceAccount:${google_service_account.assignment3_service_account.email}"
}

#Below code from line 88-91 has been referred and taken from https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/artifact_registry_repository
data "google_artifact_registry_repository" "assignment3_repository" {
  repository_id = "dockerimages"
  project  = "assignment3-k8s"
  location = "us-east4"
}
## Below code from 94-100 has been referred and taken from "https://developer.hashicorp.com/terraform/tutorials/kubernetes/gke"
output "cluster_name" {
  value = google_container_cluster.assignment3-cluster.name
}

output "node_pool_name" {
  value = google_container_node_pool.assignment3-node-pool.name
}
