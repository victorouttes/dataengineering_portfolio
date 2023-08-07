# Service account creation
resource "google_service_account" "victorouttes_portfolio_service_account" {
  account_id   = "victorouttesportfoliosc"
  display_name = "victorouttesportfoliosc"
  project      = "newagent-htsvxo"
}

# Service account creation
resource "google_service_account" "victorouttes_function_service_account" {
  account_id   = "victorouttesfunctionsc"
  display_name = "victorouttesfunctionsc"
  project      = "newagent-htsvxo"
}

# Account key
resource "google_service_account_key" "victorouttes_portfolio_account_key" {
  service_account_id = google_service_account.victorouttes_portfolio_service_account.name
  key_algorithm      = "KEY_ALG_RSA_2048"
}

resource "local_file" "service_account_key_file" {
  content  = base64decode(google_service_account_key.victorouttes_portfolio_account_key.private_key)
  filename = "${path.root}/../keys/gcp_victorouttes_portfolio_service_account_key.json"
}