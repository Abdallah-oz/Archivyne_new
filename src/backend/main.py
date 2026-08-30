from dotenv import load_dotenv
load_dotenv()
from contextlib import asynccontextmanager
from fastapi import FastAPI


from backend.database import create_db_and_tables
from backend.projects.router import router as project_router
from backend.formations.router import router as formation_router
from backend.auth.router import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(project_router)
app.include_router(formation_router)
app.include_router(auth_router)