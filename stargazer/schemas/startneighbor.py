from typing import List

from pydantic import BaseModel


class StarneighborSchema(BaseModel):
    repo: str
    stargazers: List[str]
