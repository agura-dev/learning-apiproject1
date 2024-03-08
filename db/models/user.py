from pydantic import BaseModel
from typing import Optional

#User entity
#BaseModel help us to create an entities
class User(BaseModel): 
    id: Optional[str]
    username: str
    email: str