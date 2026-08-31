from sqlalchemy.orm import Mapped, mapped_column
from backend.database import Base
import enum
class Category(str,enum.Enum):
    architecture = "architecture"
    desgin  = "design"

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(index=True)
    place: Mapped[str] = mapped_column()
    type: Mapped[str] = mapped_column()
    category: Mapped[Category] = mapped_column(index=True)
