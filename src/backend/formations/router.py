from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.database import get_session
from .models import Formation
from .schemas import FormationCreate, FormationResponse, FormationUpdate
from backend.auth.router import get_current_user


router=APIRouter(prefix="/formations", tags=["formations"])


@router.get("/",response_model=list[FormationResponse])
async def get_formations(sessions:AsyncSession=Depends(get_session)):
    result = await sessions.execute(select(Formation))
    formations = result.scalars().all()
    return formations

@router.post("/", response_model=FormationResponse)
async def create_formation(formation: FormationCreate, sessions: AsyncSession = Depends(get_session), current_user: str = Depends(get_current_user) ):
    db_formation = Formation(**formation.model_dump())
    sessions.add(db_formation)
    await sessions.commit()
    await sessions.refresh(db_formation)
    return db_formation

#get by id
@router.get("/{formation_id}",response_model=FormationResponse)
async def get_formatiom_by_id( formation_id: int, session:AsyncSession=Depends(get_session)):
    result= await session.execute(select(Formation).where(Formation.id == formation_id))
    formation = result.scalar_one_or_none()

    if formation is None:
        raise HTTPException(status_code=404, detail="Formation not found")
    return formation

@router.put("/{formation_id}", response_model=FormationResponse)
async def modifier_formation(formation_id : int, formation: FormationCreate ,session: AsyncSession=Depends(get_session), current_user: str = Depends(get_current_user) ):
    result= await session.execute(select(Formation).where(Formation.id == formation_id))
    formation_anc = result.scalar_one_or_none()
    if formation_anc is None:
        raise HTTPException(status_code=404, detail="Formation not found")
    for key, value in formation.model_dump().items():
        setattr(formation_anc, key, value)
    await session.commit()
    await session.refresh(formation_anc)
    return formation_anc

@router.patch("/{formation_id}", response_model=FormationResponse)
async def update_formation(formation_id: int, formation: FormationUpdate, session: AsyncSession = Depends(get_session), current_user: str = Depends(get_current_user) ):
    result = await session.execute(select(Formation).where(Formation.id == formation_id))
    formation_anc = result.scalar_one_or_none()

    if formation_anc is None:
        raise HTTPException(status_code=404, detail="Formation not found")

    for key, value in formation.model_dump(exclude_unset=True).items():
        setattr(formation_anc, key, value)

    await session.commit()
    await session.refresh(formation_anc)
    return formation_anc


@router.delete("/{formation_id}")
async def delete_formation(formation_id: int, session: AsyncSession = Depends(get_session), current_user: str = Depends(get_current_user) ):
    result = await session.execute(select(Formation).where(Formation.id == formation_id))
    formation = result.scalar_one_or_none()

    if formation is None:
        raise HTTPException(status_code=404, detail="Formation not found")

    await session.delete(formation)
    await session.commit()
    return {"message": "Formation deleted successfully"}