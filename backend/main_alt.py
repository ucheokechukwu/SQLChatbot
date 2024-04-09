from backend.chains.sql_chain import sql_chain_invoke
from backend.models.sql_query import QueryInput

async def sql_chain(query:dict) -> str:
    query = QueryInput.model_validate(query)
    """Retry the agent if the tool fails to run.
    Can happen during intermittent connection issues to external APIs."""
    try:
        return await sql_chain_invoke(query)
    except Exception as e:
        return (str(e))