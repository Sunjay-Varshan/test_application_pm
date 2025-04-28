import requests
import traceback
from config import Config
from msal import ConfidentialClientApplication

config = Config()

# Initialize MSAL authentication client
# This will enable application to generate token on behalf of user
auth_app = ConfidentialClientApplication(
    client_id=config.APP_ID,
    client_credential=config.APP_PASSWORD,
    authority=f"https://login.microsoftonline.com/{config.TENANT_ID}",
)

# this function extracts email of the user who is currently using the bot 
def get_user_email(context):
    """
    Extracts the user's email from Microsoft Graph API using their AAD Object ID.
    """
    try:
        # Step 1: Extract user's AAD Object ID
        user_aad_id = getattr(context.activity.from_property, "aad_object_id", None)
        if not user_aad_id:
            print("[ERROR] No AAD Object ID found in message.")
            return None
        #step 2: acquire token
        #our authenticated app is now acquiring access token for the client
        token_response = auth_app.acquire_token_for_client(
            scopes=["https://graph.microsoft.com/.default"]
        )

        if not token_response or "access_token" not in token_response:
            print("[ERROR] Failed to obtain Graph API access token.")
            return None

        access_token = token_response["access_token"]

        # Step 3: Fetch user email from Microsoft Graph using AAD Object ID
        headers = {"Authorization": f"Bearer {access_token}"}
        graph_url = f"https://graph.microsoft.com/v1.0/users/{user_aad_id}"

        response = requests.get(graph_url, headers=headers)

        if response.status_code == 200:
            user_data = response.json()
            user_email = user_data.get("mail", "Email not found")
            # print(f"[INFO] Retrieved User Email: {user_email}")
            return user_email
        else:
            print(f"[ERROR] Failed to fetch user info. Status: {response.status_code}, Response: {response.json()}")
            return None

    except Exception as e:
        print(f"[ERROR] Exception in get_user_email: {e}")
        traceback.print_exc()
        return None
