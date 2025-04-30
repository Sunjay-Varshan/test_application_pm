import json
import logging
from dataclasses import dataclass
from langchain_community.utilities import SQLDatabase
from langchain_openai import AzureChatOpenAI
from langgraph.prebuilt import create_react_agent
from teams.ai.tokenizers import Tokenizer
from teams.ai.data_sources import DataSource
from teams.state.state import TurnContext
from teams.state.memory import Memory
from langchain_community.callbacks import get_openai_callback
from src.custom_toolkit import SQLDatabaseToolkit
 
from src.email_extract import get_user_email
from src.vector_sql_search import retrieve_docs
from src.locations import autherized_locations
from src.sqlagentprompt import SQL_AGENT_PROMPT
from src.config import Config
 
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

config = Config()
 
@dataclass
class Result:
    output: str
    length: int
    too_long: bool
 
class MyDataSource(DataSource):
    """
    A data source that queries an SQL database using LangChain.
    """
 
    def __init__(self, name):
        """
        Initializes the LangChain SQL data source.
        """
        self.name = name
        # SQL Database setup
        uri = config.DB
        self.db = SQLDatabase.from_uri(uri, include_tables=['Orders','ApplicationUsers','Children','Pets','Homefindings','HomeFindingProperties','Leases','Properties','Tasks','TaskTypes','AccountPayables','AccountReceivables'])
        logger.info("SQLDatabase initialized successfully")

        self.llm = AzureChatOpenAI(
                    deployment_name=config.AZURE_OPENAI_MODEL_DEPLOYMENT_NAME,
                    openai_api_version="2024-02-01",
                    openai_api_key=config.AZURE_OPENAI_API_KEY,
                    azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
                    model=config.AZURE_OPENAI_TEXT_MODEL_NAME,
                )
        # LangChain toolkit and agent setup
        toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)
        self.tools = toolkit.get_tools()
 
    def name(self):
        return self.name
 
    async def render_data(self, context: TurnContext, memory: Memory, tokenizer: Tokenizer, maxTokens: int):
        """
        Queries the SQL database using the user-provided input.
        """
        #email
        email = 'Tejkiran@dwellworks.com'
        print(f"user email: {email}")
        logger.info(f"Extracted user email: {email}")
        #service team id
        serviceTeamId = autherized_locations(email)
        print(f"Service Team Id: {serviceTeamId}")  
        logger.info(f"Service Team ID: {serviceTeamId}")
        #query
        if serviceTeamId:
            query = memory.get('temp.input')
            logger.info(f"User query received: {query}")
            print(f"User query: {query}")
            if not query:
                return Result('', 0, False)
            
            #retrieve the example queries for the current query
            sample_sql_queries = retrieve_docs(query)
            logger.info(f"Retrieved sample SQL queries: {sample_sql_queries}")
            print(f"Sample SQL queries: {sample_sql_queries}")
    
            system_message = SQL_AGENT_PROMPT.format(dialect="mssql", top_k=5,ServiceTeamId = serviceTeamId, sample_queries = sample_sql_queries)
            agent_executor = create_react_agent(self.llm, self.tools, state_modifier=system_message)
            # Execute the query using LangChain agent
            try:
                sql_query = None

                for step in agent_executor.stream(
                    {"messages": [{"role": "user", "content": query}]},
                    stream_mode="values"
                ):
                    last_message = step["messages"][-1] 

                    # Extract SQL query if present in tool calls
                    for tool_call in last_message.additional_kwargs.get("tool_calls", []):
                        if tool_call["function"]["name"] == "sql_db_query":
                            sql_query = json.loads(tool_call["function"]["arguments"]).get("query")

                # Get the final response
                response = last_message.content
                print(f'Agent response : {response}')

                logger.info(f"SQL Query: {sql_query}")
                logger.info(f"Agent response: {response}")
    
                return Result(self.formatDocument(response), len(response), False) if response else Result('', 0, False)
            except Exception as e:
                print(f"Error querying the database: {e}")
                return Result("", 0, False)
        else:
            generic_response = "We are unable to fetch your access permissions at the moment. Please try again later."
            print(f"Returning generic response: {generic_response}")
            return Result(self.formatDocument(generic_response), len(generic_response), False) if generic_response else Result('', 0, False)
 
    def formatDocument(self, result):
        """
        Formats the result string.
        """
        return f"<context>{result}</context>"
    