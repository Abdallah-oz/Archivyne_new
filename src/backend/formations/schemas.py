from pydantic import BaseModel


class FormationCreate(BaseModel):
    title: str
    level: str
    duration: str
    payante: bool

class FormationResponse(FormationCreate):
    id: int

    class Config:
        from_attributes = True

class FormationUpdate(BaseModel):
    title: str | None = None
    level: str | None = None
    duration: str | None = None
    payante: bool | None = None