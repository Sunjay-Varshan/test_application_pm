from azure.data.tables import TableServiceClient, TableEntity,UpdateMode
from azure.core.credentials import AzureNamedKeyCredential
import uuid

from config import Config
config = Config()

credential = AzureNamedKeyCredential(config.COSMOS_ACCOUNT_NAME, config.COSMOS_ACCOUNT_KEY)
# Connect to Cosmos DB Table
table_service = TableServiceClient(
    endpoint=f"https://{config.COSMOS_ACCOUNT_NAME}.table.cosmos.azure.com",
    credential=credential
    )
table_client = table_service.get_table_client(config.COSMOS_TABLE_NAME)
print("Connected to Cosmos DB Table successfully.")

def store_chat_in_cosmos(question, sql_query, response, context):
    """
    stores each instance of the conversation in Cosmos DB
    """
    try:
        # Generate a unique ID for this conversation
        row_key = str(uuid.uuid4())
        
        entity = TableEntity()
        entity["PartitionKey"] = "ChatBot"
        entity["RowKey"] = row_key
        entity["Question"] = question
        entity["SQLQuery"] = sql_query if sql_query else "N/A"
        entity["Response"] = response

        
        table_client.create_entity(entity)
        print("Data successfully uploaded to Cosmos DB Table.")

        return row_key

    except Exception as e:
        print(f"Error uploading data to Cosmos DB: {e}")