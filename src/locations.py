import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from src.config import Config

config = Config()

# Create a session for connection reuse
session = requests.Session()

# Define your retry strategy
retry_strategy = Retry(
    total=5, 
    backoff_factor=0.5, 
    status_forcelist=[400, 401, 402, 403, 404, 500, 502, 503, 504],
    allowed_methods=["GET"]
)

# Mount the HTTPAdapter with the retry strategy
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)

session.headers.update({
    'Token': config.SERVICEID_TOKEN,
    'Content-Type': 'application/json'
})

def autherized_locations(email):
    """
    Fetches location IDs for the given email from the service efficiently.

    Args:
        email (str): The email of the user.

    Returns:
        list: A list of location IDs.
    """
    url = f'{config.SERVICEID_TOKEN_REQUEST_URL}{email}'

    try:
        response = session.get(url, timeout=5)  # Set a timeout to avoid hanging requests
        response.raise_for_status() 
        return [location['id'] for location in response.json()]

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return []

