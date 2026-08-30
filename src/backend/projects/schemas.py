from pydantic import BaseModel


class ProjectCreate(BaseModel):
    title: str
    place:str
    type:str
    category:str


class ProjectResponse(BaseModel):
    id: int
    title: str
    place:str
    type:str
    category:str
    
    class Config:
        from_attributes = True

 