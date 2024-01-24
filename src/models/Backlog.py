from pydantic import BaseModel
from typing import Optional

class Backlog(BaseModel):
    user_id: str
    name: str
    platform: str
    hours: Optional[int] = 0
    finished: Optional[bool] = False
    platinum: Optional[bool] = False
    price: Optional[float] = 0.0   