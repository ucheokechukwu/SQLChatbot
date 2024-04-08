from pydantic import BaseModel
class QueryInput(BaseModel):
    question: str
    chat_history: str = ""
    llm: str=None
    db: dict=None