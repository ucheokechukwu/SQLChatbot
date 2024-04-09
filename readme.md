# SQLChatbot

* [Demo](https://sqlquerybot.streamlit.app/)

![Screenshot]()

This chatbot interfaces with a [LangChain](https://python.langchain.com/docs/get_started/introduction) to query PostgreSQL databases. An update of the earlier version which integrates FastAPI in the backend.

Alternatively: The same app can be run from `main_alt.py` which does not integrate FastAPI into the backend, and calls the chain asynchronously.

NOTE that the demo runs on a free Open API with limited calls. Alternatively, clone the github, and provide own `OPENAI_API_KEY`.

### Version History:
[Chatbot SQL](https://github.com/ucheokechukwu/chatbot_SQL) an earlier version of this app, which also provides a Chainlit implementation hosted on AWS. In addition to incorporating FastAPI as the backend, this app uses the latest version of Langchain. 


## To Do
1. Enhance functionality of chatbot e.g. creating visuals.
2. Include alternative LLMs to OpenAI
