from pydantic import BaseModel
from .models import LevelChoices


class FormationCreate(BaseModel):
    title: str
    level: LevelChoices
    duration: str
    payante: bool
    link: str | None = None

class FormationResponse(FormationCreate):
    id: int

    class Config:
        from_attributes = True

class FormationUpdate(BaseModel):
    title: str | None = None
    level: str | None = None
    duration: str | None = None
    payante: bool | None = None
    link: str | None = None