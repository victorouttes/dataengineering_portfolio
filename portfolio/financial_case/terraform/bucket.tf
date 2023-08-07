# Bucket creation
resource "google_storage_bucket" "victorouttes_portfolio" {
  name                        = "victorouttes_portfolio"
  location                    = "US"
  force_destroy               = true
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30
    }
  }
}

# Roles
resource "google_storage_bucket_iam_member" "bucket_inside_admin_permission" {
  bucket = google_storage_bucket.victorouttes_portfolio.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.victorouttes_portfolio_service_account.email}"
}

resource "google_storage_bucket_iam_member" "bucket_info_permission" {
  bucket = google_storage_bucket.victorouttes_portfolio.name
  role   = "roles/storage.legacyBucketReader"
  member = "serviceAccount:${google_service_account.victorouttes_portfolio_service_account.email}"
}

# Bucket for Code Creation (usage in cloud functions)
resource "google_storage_bucket" "victorouttes_portfolio_functions_bucket" {
  name                        = "victorouttes-functions-bucket"
  location                    = "US"
  force_destroy               = true
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
}

resource "google_storage_bucket_iam_member" "bucket_functions_permission" {
  bucket = google_storage_bucket.victorouttes_portfolio_functions_bucket.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_service_account.victorouttes_function_service_account.email}"
}

data "archive_file" "function_archive" {
  type        = "zip"
  source_file = "${path.root}/../code/function_source/main.py"
  output_path = "${path.root}/../code/function_source.zip"
}

resource "google_storage_bucket_object" "archive" {
  name   = "index.zip"
  bucket = google_storage_bucket.victorouttes_portfolio_functions_bucket.name
  source = "${path.root}/../code/function_source.zip"
}
