import streamlit as st
import asyncio
from langchain.sql_database import SQLDatabase
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_experimental.sql import SQLDatabaseChain


# default values
POSTGRES_LOGIN = dict(st.secrets.POSTGRES_LOGIN)
chat_model = st.secrets.SQLBOT_MODEL


def generate_llm(chat_model=chat_model):
    """generates llm"""
    model_name = 'gpt-4' if chat_model == 'GPT4' else 'gpt-3.5-turbo'
    print(f"Chat GPT Model is {model_name}.")
    llm = ChatOpenAI(
        model_name=model_name,
        temperature=0,
        verbose=False)
    return llm


def connect_db(postgres_log):
    """connect to postgres SQL server using langchain and pyscopg"""
    host, port, username, password, database = postgres_log.values()
    
    from langchain.sql_database import SQLDatabase
    # post gres SQL setup
    db = None
    try:
        db = SQLDatabase.from_uri(
            f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")
        print("Connected to: ", host, port, username, password, database)
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
                        
db = connect_db(POSTGRES_LOGIN)
llm = generate_llm(chat_model=chat_model)
sql_chain = SQLDatabaseChain.from_llm(
    llm=llm,
    db=db,
    verbose=False,
    return_intermediate_steps = False)
   
async def sql_chain_invoke(question, chat_history=""):

    input = prompt.format(question=question, chat_history=chat_history)
    print(input)
    try:
        response = (await sql_chain.ainvoke(input))['result']
    except Exception as e:
        response = f"""{e}
        I cannot find a suitable answer from the SQLChat. Please rephrase and try again."""
    print(response)
    # chat_history += ('Human: '+question+'\nAI: '+response+'\n\n\n')
    # # reduce chat_history
    # try:
    #     chat_history = "\n\n\n".join(chat_history.split("\n\n\n")[-3:])
    # except:
    #     pass
    return response


        
        
        
        
        
        
        