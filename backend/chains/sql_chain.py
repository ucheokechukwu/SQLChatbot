import streamlit as st
import asyncio
from langchain.sql_database import SQLDatabase
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_experimental.sql import SQLDatabaseChain


# default values
POSTGRES_LOGIN = dict(st.secrets.POSTGRES_LOGIN)
CHAT_MODEL = st.secrets.SQLBOT_MODEL


def generate_llm(chat_model=CHAT_MODEL):
    """generates llm"""
    llm = ChatOpenAI(
        model_name=chat_model,
        temperature=0,
        verbose=False)
    return llm


def connect_db(postgres_log=POSTGRES_LOGIN):
    """connect to postgres SQL server using langchain and pyscopg"""
    host, port, username, password, database = postgres_log.values()
    
    from langchain.sql_database import SQLDatabase
    # post gres SQL setup
    db = None
    try:
        db = SQLDatabase.from_uri(
            f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")
        return db
    except Exception as e:
        st.error(f"An error {e} occured while connecting to the postgres SQL database")
        raise



# Setup the database chain
QUERY = """
Given an input question: 
{question}

Use the previous chat history as the context to first create a syntactically correct postgresql query to run, then look at the results of the query and return the answer.

This is the chat history:
{chat_history}

Use the following format:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here
"""
prompt = PromptTemplate(template=QUERY, 
                        input_variables=['question','chat_history'])
                        


   
async def sql_chain_invoke(query):
    sql_chain = SQLDatabaseChain.from_llm(
        # llm=generate_llm(query.chat_model) if query.chat_model else generate_llm(),
        llm = generate_llm(),
        # db=connect_db(query.postgres_log) if query.postgres_log else connect_db(),
        db = connect_db(),
        verbose=False,
        return_intermediate_steps = False)
    
    input = prompt.format(question=query.question, chat_history=query.chat_history)

    try:
        response = (await sql_chain.ainvoke(input))['result']
    except Exception as e:
        response = f"""{e}
        I cannot find a suitable answer from the SQLChat. Please rephrase and try again."""
    return response


        
        
        
        
        
        
        