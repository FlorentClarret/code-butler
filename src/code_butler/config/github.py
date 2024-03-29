from pydantic import BaseModel


class Github(BaseModel):
    token: str = ""
