from pydantic import BaseModel
from typing import Optional

class IdentifierBase(BaseModel):
    identifier_name: str
    description: Optional[str] = None
    identifier_type: Optional[str] = None

class IdentifierCreate(IdentifierBase):
    pass

class IdentifierUpdate(BaseModel):
    description: Optional[str] = None
    identifier_type: Optional[str] = None

class IdentifierResponse(IdentifierBase):
    class Config:
        from_attributes = True