# Imports
import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate, ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder

# Agent cache for the streamlit application
agent_cache = None

# Get chat agent from cache, create if does not exist
def get_db_chat_agent():
    global agent_cache
    if (agent_cache):
        return agent_cache
    else:
        agent_cache = create_db_chat_agent()
        return agent_cache

# Function to generate agent model
def create_db_chat_agent():

    # Get Google API key
    GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
    if (not GOOGLE_API_KEY):
        raise Exception("Missing environment variable: GOOGLE_API_KEY")

    # Setup Gemini LLM
    GOOGLE_MODEL_NAME = os.environ['GOOGLE_MODEL_NAME']
    llm = ChatGoogleGenerativeAI(model=GOOGLE_MODEL_NAME, google_api_key=GOOGLE_API_KEY, temperature=0.1)

    # Setup database
    db = get_sql_database_object()

    # Generate vector store and example selector
    vectorstore = create_few_shots_vector_db()
    example_selector = SemanticSimilarityExampleSelector(vectorstore=vectorstore, k=5, input_keys=["input"])

    # Generate custom prompt
    agent_prompt = generate_agent_prompt(example_selector)

    # Create and return agent
    agent = create_sql_agent(llm, db=db, prompt=agent_prompt, verbose=True, agent_type='tool-calling')
    return agent

# Function to get SQLDatabase object requried by agent
def get_sql_database_object():

    # Get environment variables
    db_host = os.environ['SQL_HOST']
    db_port = os.environ['SQL_PORT']
    db_name = os.environ['SQL_DB_NAME']
    db_user = os.environ['SQL_USERNAME']
    db_password = os.environ['SQL_PASSWORD']

    # Create and return sql db object
    print(f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
    db = SQLDatabase.from_uri(f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
    return db

# Get vector db with few shots data indexed
def create_few_shots_vector_db():

    # Read few shot data file
    file_name = os.environ['FEW_SHOT_DATA_FILE']
    few_shots_data = []
    with open(f'./vector-db/{file_name}', 'r') as f:
        few_shots_data = json.load(f)
    blobs = [" ".join(sample.values()) for sample in few_shots_data]

    # Generate vector embeddings and return vector store
    embedding = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    vectorstore = Chroma.from_texts(blobs, embedding=embedding, metadatas=few_shots_data)
    return vectorstore

# Generate agent prompt
def generate_agent_prompt(example_selector):

    # Prompt strings
    system_prefix = 'You are an agent designed to interact with a SQL database.\nGiven an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.\nUnless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.\nYou can order the results by a relevant column to return the most interesting examples in the database.\nNever query for all the columns from a specific table, only ask for the relevant columns given the question.\nYou have access to tools for interacting with the database.\nOnly use the below tools. Only use the information returned by the below tools to construct your final answer.\nYou MUST always double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.\nOnly have single quotes on any sql command sent to the engine.\nDo not escape single quotes on any sql command sent to the engine.\nDo not return raw query as result after generating it, execute it and return result.\nIf you are returning a list of data as final answer, format it properly using new lines and bullet points.\n\nDO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.\n\nIf the question does not seem related to the database, just return "I don\'t know" as the answer.\n\nWhenever you return any price, use rupees (Rs.) as currency and use two comma separator format for formatting the price.\n\nHere are some examples of user inputs and their corresponding SQL queries:'
    system_suffix = "\n"

    # Few shot examples template
    example_prompt = PromptTemplate(input_variables=['input', 'query', 'answer'], template='Human: {input}\nSQL Query: {query}\nAI: {answer}')

    # Full few shots prompt with examples
    few_shot_prompt = FewShotPromptTemplate(example_selector=example_selector,
                                            example_prompt=example_prompt,
                                            prefix=system_prefix,
                                            suffix=system_suffix,
                                            input_variables=[
                                                "input",
                                                "top_k",
                                                "dialect",
                                            ])

    # Final prompt after adding everything
    full_prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate(prompt=few_shot_prompt),
        ("human", "{input}"),
        ("ai", "I should look at the tables in the database to see what I can query. Then I should query the schema of the most relevant tables."),
        MessagesPlaceholder("agent_scratchpad"),
    ])
    return full_prompt

import time

# Main function to test this out
import sys
if __name__ == '__main__':
    print("Testing agent with some simple prompts")

    # Get agent
    agent = create_db_chat_agent()

    # Test prompts
    agent.invoke('How many total brands are available?')
    agent.invoke('What is the total price of all Adidas products combined?')
    agent.invoke('How many white products are there from Gucci?')

    sys.exit(0)
