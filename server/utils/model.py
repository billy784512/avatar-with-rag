from typing import Literal
from pydantic import BaseModel

class QueryItem(BaseModel):
    query: str
    type: Literal["vector", "hybrid", "semantic"] = "semantic"
    language: str = "zh-tw"