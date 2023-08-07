terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  credentials = file("${path.root}/../keys/gcp_terraform_key.json")

  project = "newagent-htsvxo"
  region  = "us-central1"
  zone    = "us-central1-c"
}
