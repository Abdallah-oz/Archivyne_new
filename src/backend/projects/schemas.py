from pydantic import BaseModel, Field
from .models import Category

class ProjectCreate(BaseModel):
    title: str
    place:str
    type:str
    category: Category
    photos: list[str] = Field(default_factory=list)


class ProjectResponse(BaseModel):
    id: int
    title: str
    place:str
    type:str
    category:Category
    photos: list[str]
    
    class Config:
        from_attributes = True

 