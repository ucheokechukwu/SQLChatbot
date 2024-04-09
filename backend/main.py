from fastapi import FastAPI
from backend.chains.sql_chain import sql_chain_invoke
from backend.models.sql_query import QueryInput
from backend.utils.async_utils import async_retry
#
app = FastAPI(
    title="SQL Chatbot 🤖",
    description="Endpoints for the SQL Chatbot"
)

@async_retry(max_retries=10, delay=1)
async def invoke_agent_with_retry(query:QueryInput) -> str:
    """Retry the agent if the tool fails to run.
    Can happen during intermittent connection issues to external APIs."""
    return await sql_chain_invoke(query)

@app.get("/")
async def get_status():
    return {"status":"running"}

@app.post("/sql_chain")
async def sql_agent(query: QueryInput) -> str:
    response = await invoke_agent_with_retry(query)
    return response
