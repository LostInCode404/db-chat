# Imports
import os
import re
import asyncio
import streamlit as st
from model import get_db_chat_agent

# Start event loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Get the agent, it is cached so initializing it is okay
agent = get_db_chat_agent()

# Fix new line rendering in streamlit write fn
def _fix_streamlit_space(text: str) -> str:
    def _replacement(match: re.Match):
        if match.group(0).startswith(" "):
            return " \n"
        else:
            return "  \n"
    return re.sub(r"( ?)\n", _replacement, text)

# Add sidebar with info
with st.sidebar:
    st.title('DB-Chat')
    st.write(
        'This app allows you to talk to a database in natural language. To configure a custom database, please update the \'.env\' file with connection details and only start the \'app\' service from docker compose.'
    )
    st.header("Database: ")
    st.write(f"`{os.environ['SQL_DB_NAME']}`")
    st.header("Model: ")
    st.write(f"`{os.environ['GOOGLE_MODEL_NAME']}`")

# Add title
st.title("Chat with your database")

# Add text input
question = st.text_input("Question: ")

# If there is a question, get answer and add to UI
if (question):

    # Execute query
    answer = agent.invoke(question)

    # Set value in UI
    print(answer['output'])
    st.header("Answer: ")
    st.write(_fix_streamlit_space(answer['output']))

# Placeholder for answer
else:
    st.header("Answer: ")
    st.write('Enter a question to get the answer here.')
