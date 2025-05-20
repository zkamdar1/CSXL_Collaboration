"""The Announcement service allows for api to manipulate announcements in database."""

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import db_session
from backend.models.announcements import Announcements
from ..entities.announcements_entity import AnnouncementEntity
from ..models import User
from .permission import PermissionService
from .exceptions import ResourceNotFoundException


# Setup basic service to abstart api call functionality. For future reference, does not work rn.
# also setup basic database session


class AnnouncementsService:
    """Service that performs all of the actions on the `Announcements` table"""

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission: PermissionService = Depends(),
    ):
        """Initializes the `AnnoucementsService` session"""
        self._session = session
        self._permission = permission

    def get_announcements(self) -> list[Announcements]:
        """Retrieves all announcements from table

        Returns: list[Announcement]: list of all 'announcements'
        """
        query = select(AnnouncementEntity).where(
            AnnouncementEntity.state == "Published"
        )
        entities = self._session.scalars(query).all()

        return [entity.to_model() for entity in entities]

    def get_all_announcements(self, subject: User) -> list[Announcements]:
        """Retrieves all announcements from table

        Returns: list[Announcement]: list of all 'announcements'
        """

        # Ensure that the user has appropriate permissions to create users
        self._permission.enforce(
            subject,
            "announcements.view_all",
            f"announcements",
        )

        query = select(AnnouncementEntity)
        entities = self._session.scalars(query).all()

        return [entity.to_model() for entity in entities]

    def create_announcements(
        self, subject: User, announcements: Announcements
    ) -> Announcements:

        # Ensure that the user has appropriate permissions to create users
        self._permission.enforce(
            subject,
            "announcements.create",
            f"announcements/{announcements.slug}",
        )

        announcements.id = None
        entity = AnnouncementEntity.from_model(subject, announcements)
        self._session.add(entity)
        self._session.commit()
        return entity.to_model()

    def update_announcements(
        self, subject: User, announcements: Announcements
    ) -> Announcements:
        self._permission.enforce(
            subject,
            "announcements.update",
            f"announcements/{announcements.slug}",
        )

        entity = self._session.get(AnnouncementEntity, announcements.id)
        if entity is None:
            raise HTTPException(
                status_code=404,
                detail=f"No announcement found with id: {announcements.id}",
            )

        entity.headline = announcements.headline
        entity.synopsis = announcements.synopsis
        entity.main_story = announcements.main_story
        entity.slug = announcements.slug
        entity.organization = announcements.organization
        entity.state = announcements.state
        entity.image = announcements.image
        entity.modification = announcements.modification

        self._session.commit()
        return entity.to_model()

    def delete_announcements_slug(self, subject: User, announcement_slug: str) -> None:
        self._permission.enforce(
            subject,
            "announcements.delete",
            f"announcements/{announcement_slug}",
        )

        try:
            entity = (
                self._session.query(AnnouncementEntity)
                .filter(AnnouncementEntity.slug == announcement_slug)
                .one()
            )
            self._session.delete(entity)
            self._session.commit()
        except Exception as e:
            raise HTTPException(
                status_code=404,
                detail=f"No announcement found with slug: {announcement_slug} : {e}",
            )

    def get_by_slug(self, slug: str) -> Announcements:
        """
        Get the organization from a slug
        If none retrieved, a debug description is displayed.

        Parameters:
            slug: a string representing a unique organization slug

        Returns:
            Organization: Object with corresponding slug

        Raises:
            ResourceNotFoundException if no organization is found with the corresponding slug
        """

        # Query the organization with matching slug
        announcement = (
            self._session.query(AnnouncementEntity)
            .filter(AnnouncementEntity.slug == slug)
            .one_or_none()
        )

        # Check if result is null
        if announcement is None:
            raise ResourceNotFoundException(
                f"No announcement found with matching slug: {slug}"
            )

        return announcement.to_model()
