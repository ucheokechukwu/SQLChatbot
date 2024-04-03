import os
import time
import requests
import streamlit as st
from backend import entrypoint




from backend.chains.sql_chain import sql_chain_invoke
import streamlit as st
CHATBOT_URL = st.secrets["CHATBOT_URL"]
POSTGRES_LOGIN = dict(st.secrets.POSTGRES_LOGIN)
chat_model = st.secrets.SQLBOT_MODEL








# streamlit framework and state variables

# Initialize chat history and sidebar visibility
if "messages" not in st.session_state:
    st.session_state.messages = []
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False  
# initialize db
if 'POSTGRES_LOGIN' not in st.session_state:
    st.session_state.POSTGRES_LOGIN = POSTGRES_LOGIN   
# initialize chat_gpt
if 'chat_model' not in st.session_state:
    st.session_state.chat_model = CHATBOT_URL
# initialize memory
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = ""   
# if 'sidebar_state' not in st.session_state:
#     st.session_state.sidebar_state = 'collapsed'


# st.set_page_config(initial_sidebar_state=st.session_state.sidebar_state)  
st.title("SQL ChatBot")  
    
    
    

# sidebar to change chatgpt and server settings
with st.sidebar:
    st.session_state.chat_model = st.selectbox('Select the Chat GPT Version',
                            ("GPT3.5", "GPT4"))
    st.checkbox("Check to use default server connection", key="disabled")

    with st.form("Postgres_Settings"):
        st.write("Postgres SQL Server settings")
        postgres_input = POSTGRES_LOGIN.copy()
        for key in POSTGRES_LOGIN.keys():
            if key == 'password':
                postgres_input[key] = st.text_input(
                key, disabled=st.session_state.disabled, type="password")
            else:
                postgres_input[key] = st.text_input(
                key, disabled=st.session_state.disabled)
        submitted = st.form_submit_button(
            "Submit", disabled=st.session_state.disabled)
        if submitted:
            st.session_state.POSTGRES_LOGIN = postgres_input
#             st.session_state.sidebar_state = 'collapsed' if st.session_state.sidebar_state == 'expanded' else 'expanded'


# chatbot



# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if question := st.chat_input("Type in your SQL question here"):
    # Display user message in chat message container
    st.chat_message("user").markdown(question)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": question})  
    
    try:
        data = {"question": question, "chat_history":st.session_state.chat_history}
        response = requests.post(CHATBOT_URL, json=data)
        assert response.status_code == 200

        output_text = response.json()
                        
        st.session_state.chat_history += ('Human: '+question+'\nAI: '+output_text+'\n')
    except Exception as e:
        print(e)
        output_text = f"""I cannot find a suitable answer from the SQLChat. Please rephrase and try again."""
                                  
                    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(output_text)
    # Add assistant response to chat history
    st.session_state.messages.append(
        {"role": "assistant", "content": output_text})
        
        
        
        
        
        
        
        
        
        
        
        
        
        