from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from starlette.concurrency import run_in_threadpool
import cloudinary.uploader

from backend.auth.services import get_current_user
from backend.cloudinary_config import is_configured

from backend.database import get_session
from .models import Project
from .schemas import ProjectCreate, ProjectResponse

router = APIRouter(prefix="/projects", tags=["projects"])

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png"}


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
        category=project.category,
        photos=project.photos,
    )
    session.add(new_project)
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.post("/{project_id}/photos", response_model=ProjectResponse)
async def upload_project_photos(
    project_id: int,
    files: list[UploadFile] = File(...),
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    result = await session.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    if not is_configured():
        raise HTTPException(
            status_code=503,
            detail="Cloudinary is not configured on the server",
        )

    uploaded_urls = list(project.photos or [])

    for file in files:
        if file.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=400,
                detail="Only JPG, JPEG and PNG images are allowed",
            )

        try:
            upload_result = await run_in_threadpool(
                cloudinary.uploader.upload,
                file.file,
                folder="archivyne/projects",
                resource_type="image",
            )
        except Exception as error:
            raise HTTPException(
                status_code=502,
                detail="Image upload to Cloudinary failed",
            ) from error

        uploaded_urls.append(upload_result["secure_url"])

    project.photos = uploaded_urls
    await session.commit()
    await session.refresh(project)
    return project

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
    existing_project.photos = project.photos

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
    existing_project.photos = project.photos

    await session.commit()
    await session.refresh(existing_project)
    return existing_project
