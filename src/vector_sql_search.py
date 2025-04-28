from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores.azuresearch import AzureSearch

from config import Config
config = Config()

AZURESEARCH_FIELDS_CONTENT = config.AZURESEARCH_FIELDS_CONTENT
AZURESEARCH_FIELDS_CONTENT_VECTOR = config.AZURESEARCH_FIELDS_CONTENT_VECTOR   

embeddings = AzureOpenAIEmbeddings(
    azure_deployment=config.OPENAI_DEPOLYMENT_ID_ADA,
    openai_api_version="2024-02-01",
    azure_endpoint=config.OPENAI_ENDPOINT,
    api_key=config.OPENAI_KEY,
)

vector_store = AzureSearch(
    azure_search_endpoint=config.AI_SEARCH_ENDPOINT,
    azure_search_key=config.AI_SEARCH_API_KEY,
    index_name=config.AI_SEARCH_INDEX,
    embedding_function=embeddings.embed_query,
    additional_search_client_options={"retry_total": 4},
    semantic_configuration_name=config.AI_SEARCH_SEMANTIC_CONFIG_NAME
)
retriever = vector_store.as_retriever(search_type="semantic_hybrid", k=3)

def retrieve_docs(query):
    """
    Retrieves relevant documents from Azure AI Search using semantic hybrid search.

    Args:
        query (str): The search query.
        k (int): Number of documents to retrieve.

    Returns:
        list: A list of retrieved documents.
    """
    try:

        docs = retriever.invoke(query)
        return [doc.metadata.get("sqlQuery", "") for doc in docs if doc.metadata.get("sqlQuery")]

    except Exception as e:
        return None
