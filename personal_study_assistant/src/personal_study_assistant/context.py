from pydantic import BaseModel

class Context(BaseModel):
    word_limit: int = 30