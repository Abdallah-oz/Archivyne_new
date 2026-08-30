from sqlalchemy.orm import Mapped, mapped_column
from backend.database import Base

import enum

class LevelChoices(str, enum.Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"

class Formation(Base):
    __tablename__ = "formations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(index=True)
    level: Mapped[LevelChoices] = mapped_column()
    duration: Mapped[str] = mapped_column()
    payante: Mapped[bool] = mapped_column()
