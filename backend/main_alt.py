from backend.chains.sql_chain import sql_chain_invoke
from backend.models.sql_query import QueryInput
from backend.utils.async_utils import async_retry

@async_retry(max_retries=10, delay=1)
async def invoke_agent_with_retry(query:QueryInput) -> str:
    """Retry the agent if the tool fails to run.
    Can happen during intermittent connection issues to external APIs."""
    try:
        return await sql_chain_invoke(query)
    except Exception as e:
        return (str(e))
        
        
async def sql_agent(query: dict) -> str:
    query = QueryInput.model_validate(query)
    response = await invoke_agent_with_retry(query)
    return response