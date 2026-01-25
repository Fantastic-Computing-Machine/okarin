import os

from langchain_google_community.calendar.utils import (
    get_google_credentials as load_google_credentials,
)

TOKEN_FILE = "config/token.json"
CREDENTIALS_FILE = "config/credentials.json"


def get_google_credentials(scopes):
    """Return cached Google creds or run the OAuth flow and cache them.

    This wraps langchain's helper to force our token/credentials file locations and
    to ensure the `config/` directory exists before it tries to write `token.json`.
    """

    if not scopes:
        raise ValueError("At least one OAuth scope is required to fetch Google credentials.")

    os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)

    if not os.path.exists(CREDENTIALS_FILE):
        raise FileNotFoundError(
            f"'{CREDENTIALS_FILE}' not found. "
            "Download the OAuth client JSON from Google Cloud Console and place it under config/."
        )

    credentials = load_google_credentials(
        scopes=scopes,
        token_file=TOKEN_FILE,
        client_secrets_file=CREDENTIALS_FILE,
    )

    # If the cached token lacks required scopes, force a fresh OAuth run.
    if credentials and credentials.scopes:
        missing_scopes = set(scopes) - set(credentials.scopes)
        if missing_scopes:
            # Drop the stale token so the next load triggers the OAuth consent screen.
            try:
                os.remove(TOKEN_FILE)
            except FileNotFoundError:
                pass
            credentials = load_google_credentials(
                scopes=scopes,
                token_file=TOKEN_FILE,
                client_secrets_file=CREDENTIALS_FILE,
            )

    return credentials


if __name__ == "__main__":
    scopes = ['https://www.googleapis.com/auth/tasks']
    creds = get_google_credentials(scopes)
    print("Google credentials obtained successfully.")
