from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.auth.service import get_current_user

from backend.database import get_session
from .models import Project
from .schemas import ProjectCreate, ProjectResponse

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/", response_model=list[ProjectResponse])
async def get_projects(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Project))
    projects = result.scalars().all()
    return projects



@router.post("/", response_model=ProjectResponse)
async def create_project(project: ProjectCreate, session: AsyncSession = Depends(get_session), current_user: str = Depends(get_current_user) ):
    new_project = Project(
        title=project.title,
        place=project.place,
        type=project.type,
        category=project.category
    )
    session.add(new_project)
    await session.commit()
    await session.refresh(new_project)
    return new_project

@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: int, project: ProjectCreate, session: AsyncSession = Depends(get_session), current_user: str = Depends(get_current_user) ):
    result = await session.execute(select(Project).where(Project.id == project_id))
    existing_project = result.scalar_one_or_none()

    if existing_project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    existing_project.title = project.title
    existing_project.place = project.place
    existing_project.type = project.type
    existing_project.category = project.category

    await session.commit()
    await session.refresh(existing_project)
    return existing_project

@router.delete("/{project_id}")
async def delete_project(project_id: int, session: AsyncSession = Depends(get_session), current_user: str = Depends(get_current_user) ):
    result = await session.execute(select(Project).where(Project.id == project_id))
    existing_project = result.scalar_one_or_none()

    if existing_project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    await session.delete(existing_project)
    await session.commit()
    return {"message": "Project deleted successfully"}

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    return project

@router.put("/{project_id}", response_model=ProjectResponse)
async def replace_project(project_id: int, project: ProjectCreate, session: AsyncSession = Depends(get_session), current_user: str = Depends(get_current_user) ):
    result = await session.execute(select(Project).where(Project.id == project_id))
    existing_project = result.scalar_one_or_none()

    if existing_project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    existing_project.title = project.title
    existing_project.place = project.place
    existing_project.type = project.type
    existing_project.category = project.category

    await session.commit()
    await session.refresh(existing_project)
    return existing_project
