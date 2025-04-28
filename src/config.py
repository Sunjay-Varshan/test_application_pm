"""
Copyright (c) Microsoft Corporation. All rights reserved.
Licensed under the MIT License.
"""

import os

from dotenv import load_dotenv, dotenv_values

load_dotenv(override=True)
values_env = dotenv_values(".env")

load_dotenv()

class Config:
    """Bot Configuration"""

    PORT = 3978
    APP_ID = os.environ.get("BOT_ID", "")
    APP_PASSWORD = os.environ.get("BOT_PASSWORD", "")
    TENANT_ID = os.environ["TEAMS_APP_TENANT_ID"]
    AZURE_OPENAI_API_KEY = os.environ["AZURE_OPENAI_API_KEY"] # Azure OpenAI API key
    AZURE_OPENAI_MODEL_DEPLOYMENT_NAME = os.environ["AZURE_OPENAI_MODEL_DEPLOYMENT_NAME"] # Azure OpenAI model deployment name
    AZURE_OPENAI_TEXT_MODEL_NAME = os.environ["AZURE_OPENAI_TEXT_MODEL_NAME"]
    AZURE_OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"] # Azure OpenAI endpoint
    DB = os.environ["DATABASE_CONNECTION_STRING"]

    #storage account
    STORAGE_ACCOUNT = os.environ["STORAGE_ACCOUNT"]
    STORAGE_KEY = os.environ["STORAGE_KEY"]
    STORAGE_CONTAINER = os.environ["STORAGE_CONTAINER"]

    #azure ai search
    AI_SEARCH_SERVICE = os.environ["AI_SEARCH_SERVICE"]
    AI_SEARCH_INDEX = os.environ["AI_SEARCH_INDEX"]
    AI_SEARCH_ENDPOINT = os.environ["AI_SEARCH_ENDPOINT"]
    AI_SEARCH_API_KEY  = os.environ["AI_SEARCH_API_KEY"]
    AI_SEARCH_CATEGORY = os.environ["AI_SEARCH_CATEGORY"]
    AI_SEARCH_SEMANTIC_CONFIG_NAME = os.environ["AI_SEARCH_SEMANTIC_CONFIG_NAME"]

    AZURESEARCH_FIELDS_CONTENT  = os.environ["AZURESEARCH_FIELDS_CONTENT"]
    AZURESEARCH_FIELDS_CONTENT_VECTOR = os.environ["AZURESEARCH_FIELDS_CONTENT_VECTOR"]

    #openai creds
    OPENAI_KEY = os.environ["OPENAI_KEY"]
    OPENAI_ENDPOINT = os.environ["OPENAI_ENDPOINT"]
    OPENAI_DEPOLYMENT_ID_ADA = os.environ["OPENAI_DEPOLYMENT_ID_ADA"]
    OPENAI_EMBEDDING_MODEL = os.environ["OPENAI_EMBEDDING_MODEL"]

    #external api access tokens
    SERVICEID_TOKEN = os.environ["SERVICEID_TOKEN"]
    SERVICEID_TOKEN_REQUEST_URL = os.environ["SERVICEID_TOKEN_REQUEST_URL"]

    #cosmos db
    COSMOS_ACCOUNT_NAME = os.environ["COSMOS_ACCOUNT_NAME"]
    COSMOS_ACCOUNT_KEY = os.environ["COSMOS_ACCOUNT_KEY"]
    COSMOS_TABLE_NAME = os.environ["COSMOS_TABLE_NAME"]