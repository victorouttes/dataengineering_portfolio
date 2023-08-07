# Cloud Function creation
resource "google_cloudfunctions_function" "portfolio_function" {
  name                  = "handler"
  description           = "Portfolio Function"
  runtime               = "python39"
  available_memory_mb   = 128
  source_archive_bucket = google_storage_bucket.victorouttes_portfolio_functions_bucket.name
  source_archive_object = google_storage_bucket_object.archive.name
  trigger_http          = true
  service_account_email = google_service_account.victorouttes_function_service_account.email
}
