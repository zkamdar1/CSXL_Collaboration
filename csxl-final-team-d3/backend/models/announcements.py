from pydantic import BaseModel
from .organization import Organization
from .user import User
from enum import Enum


class State(str, Enum):
    Draft = "Draft"
    Published = "Published"
    Archived = "Archived"


class Announcements(BaseModel):
    """Pydantic model to represent an announcement."""

    id: int | None = None  # primary key
    headline: str
    synopsis: str
    main_story: str  # written in markdown
    organization: str | None = None #optional relationship to Orginization
    state: State = State.Draft  # state can be draft, published, archived
    slug: str  # unique string used in URL
    image: str | None = None  # optional link to imag to use in feed
    publish: str
    modification: str
    author_id: int | None = None
