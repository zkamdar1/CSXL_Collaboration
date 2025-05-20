"""Entity file to define table structure for annoucements in database"""

from sqlalchemy import Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .entity_base import EntityBase
from backend.models.announcements import State, Announcements
from backend.models.user import User
from typing import Self

#Setup basic table structure for announcement table in database. orginization type needs to be fixed

class AnnouncementEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Announcements` table"""

    # Name for the announcements table in the PostgreSQL database
    __tablename__ = "announcements"

    #Define the main fields of the Annoucements entity.
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    headline: Mapped[str] = mapped_column(String, nullable=False, default="")
    synopsis: Mapped[str] = mapped_column(String, nullable=False, default="")
    main_story: Mapped[str] = mapped_column(String, nullable=False, default="")
    organization: Mapped[str] = mapped_column(String,nullable=True, default=None)
    state: Mapped[State] = mapped_column(Enum(State, create_constraint=True, name="Draft"), nullable=False)
    slug: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    image: Mapped[str] = mapped_column(String,nullable=True, default=None)
    publish: Mapped[str] = mapped_column(String,nullable=False, default="yyyy-MM-ddTHH:mm:ss")
    modification: Mapped[str] = mapped_column(String,nullable=False, default="yyyy-MM-ddTHH:mm:ss")
    
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["UserEntity"] = relationship(back_populates="announcements")
    
    @classmethod
    def from_model(cls, subject: User, model: Announcements) -> Self:
        return cls(
            id=model.id,
            headline=model.headline,
            synopsis=model.synopsis,
            main_story=model.main_story,
            organization=model.organization,
            state=model.state,
            slug=model.slug,
            image=model.image,
            publish=model.publish,
            modification=model.modification,
            author_id=model.author_id,
        )

    def to_model(self) -> Announcements:
        return Announcements(
            id=self.id,
            headline=self.headline,
            synopsis=self.synopsis,
            main_story=self.main_story,
            organization=self.organization,
            state=self.state,
            slug=self.slug,
            image=self.image,
            publish=self.publish,
            modification=self.modification,
            author_id=self.author_id,
        )