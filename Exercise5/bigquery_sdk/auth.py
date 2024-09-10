from google.oauth2 import service_account

def get_credentials_from_service_account(key_path):
    """Get credentials from a service account key."""
    credentials = service_account.Credentials.from_service_account_file(key_path)
    return credentials
