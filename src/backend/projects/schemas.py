from pydantic import BaseModel
from .models import Category

class ProjectCreate(BaseModel):
    title: str
    place:str
    type:str
    category: Category


class ProjectResponse(BaseModel):
    id: int
    title: str
    place:str
    type:str
    category:Category
    
    class Config:
        from_attributes = True

 