"""Announcements API
    
Announcements routes used to create, update, retrieve and delete Announcements."""

# Setup a basic api call to show how we are supposed to have it done for future reference. commented out bc it will not work rn.

from fastapi import APIRouter, Depends
from backend.api.authentication import registered_user
from backend.models.user import User
from ..services.announcements import AnnouncementsService
from ..models.announcements import Announcements
from ..services.permission import PermissionService

api = APIRouter(prefix="/api/announcements")
openapi_tags = {
    "name": "Announcements",
    "description": "Create, update, delete, and retrieve announement posts.",
}


@api.get("", response_model=list[Announcements], tags=["Announcements"])
def get_announcements(
    announcements_service: AnnouncementsService = Depends(),
) -> list[Announcements]:
    """
    Get all announcements

    Parameters:
        announcements_service: a valid AnnouncementsService

    Returns:
        list[announcements]: All `Announcement`s in the `Announcement` database table
    """
    return announcements_service.get_announcements()


@api.get("/all", response_model=list[Announcements], tags=["Announcements"])
def get_all_announcements(
    subject: User = Depends(registered_user),
    announcements_service: AnnouncementsService = Depends(),
    permission_service: PermissionService = Depends(),
) -> list[Announcements]:
    """
    Get all announcements

    Parameters:
        announcements_service: a valid AnnouncementsService

    Returns:
        list[announcements]: All `Announcement`s in the `Announcement` database table
    """
    return announcements_service.get_all_announcements(subject)


@api.post("", response_model=Announcements, tags=["Announcements"])
def create_announcements(
    announcement: Announcements,
    subject: User = Depends(registered_user),
    announcements_service: AnnouncementsService = Depends(),
) -> Announcements:
    return announcements_service.create_announcements(subject, announcement)


@api.put("", response_model=Announcements, tags=["Announcements"])
def update_announcements(
    announcement: Announcements,
    subject: User = Depends(registered_user),
    announcements_service: AnnouncementsService = Depends(),
) -> Announcements:
    return announcements_service.update_announcements(subject, announcement)


@api.delete(
    "/{slug}",
    responses={404: {"model": None}},
    response_model=None,
    tags=["Announcements"],
)
def delete_announcements_slug(
    slug: str,
    subject: User = Depends(registered_user),
    announcements_service: AnnouncementsService = Depends(),
) -> None:
    announcements_service.delete_announcements_slug(subject, slug)


@api.get(
    "/{slug}",
    responses={404: {"model": None}},
    response_model=Announcements,
    tags=["Announcements"],
)
def get_announcement_by_slug(
    slug: str, announcements_service: AnnouncementsService = Depends()
) -> Announcements:
    """
    Get organization with matching slug

    Parameters:
        slug: a string representing a unique identifier for an Organization
        organization_service: a valid OrganizationService

    Returns:
        Organization: Organization with matching slug

    Raises:
        HTTPException 404 if get_by_slug() raises an Exception
    """

    return announcements_service.get_by_slug(slug)
