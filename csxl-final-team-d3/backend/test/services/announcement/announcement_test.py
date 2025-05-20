# pytests for backend services
# PyTest
from fastapi import Depends, HTTPException
import pytest
from unittest.mock import create_autospec
from backend.models.pagination import PaginationParams


# PyTest
from backend.services.exceptions import (
    UserPermissionException,
    ResourceNotFoundException,
)




from backend.api.authentication import registered_user
from backend.models.user import User




# Tested Dependencies
from ....models.announcements import Announcements, State
from ....services.announcements import AnnouncementsService


# Injected Service Fixtures
from ..fixtures import announcement_svc_integration, user_svc_integration


# type: ignore
# Explicitly import Data Fixture to load entities in database
from ..core_data import setup_insert_data_fixture




# Data Models for Fake Data Inserted in Setup
from .announcement_test_data import (
    new_announcement,
    updated_announcement1,
    announcements,
    announcement1,
)
from ..user_data import user, ambassador, root


__authors__ = ["Jade Keegan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"




def test_get_all(announcement_svc_integration: AnnouncementsService):
    """Test that all announcements can be retrieved."""
    fetched_announcements = announcement_svc_integration.get_announcements()
    assert fetched_announcements is not None
    assert len(fetched_announcements) == len(announcements)
    assert isinstance(fetched_announcements[0], Announcements)




def test_get_by_slug(announcement_svc_integration: AnnouncementsService):
    """Test that announcements can be retrieved based on their ID."""
    fetched_announcement = announcement_svc_integration.get_by_slug(
        announcement1.slug
    )
    assert fetched_announcement is not None
    assert isinstance(fetched_announcement, Announcements)
    assert fetched_announcement.slug == announcement1.slug




def test_create_announcement_as_root(
    announcement_svc_integration: AnnouncementsService,
):
    """Test that the root user is able to create new organizations."""
    created_announcement = announcement_svc_integration.create_announcements(
        root, new_announcement
    )
    assert created_announcement is not None
    assert created_announcement.id is not None




def test_create_announcement_as_user(
    announcement_svc_integration: AnnouncementsService,
):
    """Test that any user is *unable* to create new organizations."""
    with pytest.raises(UserPermissionException):
        announcement_svc_integration.create_announcements(user, new_announcement)
        pytest.fail()  # Fail test if no error was thrown above




def test_update_announcement_as_user(
    announcement_svc_integration: AnnouncementsService,
):
    """Test that any user is *unable* to update new organizations."""
    with pytest.raises(UserPermissionException):
        announcement_svc_integration.update_announcements(user, updated_announcement1)




def test_update_announcement_does_not_exist(
    announcement_svc_integration: AnnouncementsService,
):
    """Test updating an organization that does not exist."""
    with pytest.raises(HTTPException):
        announcement_svc_integration.update_announcements(root, new_announcement)




def test_delete_announcement_as_user(
    announcement_svc_integration: AnnouncementsService,
):
    """Test that any user is *unable* to delete announcements."""
    with pytest.raises(UserPermissionException):
        announcement_svc_integration.delete_announcements_slug(user, announcement1.slug)




def test_delete_announcement_does_not_exist(
    announcement_svc_integration: AnnouncementsService,
):
    """Test deleting an organization that does not exist."""
    with pytest.raises(HTTPException):
        announcement_svc_integration.delete_announcements_slug(root, new_announcement.slug)




def test_add_announcements(announcement_svc_integration: AnnouncementsService):
    """Test that adding a timer creates and returns the correct timer"""
    result = announcement_svc_integration.create_announcements(root, new_announcement)
    assert result is not None
    assert new_announcement.headline == result.headline
    assert new_announcement.synopsis == result.synopsis
    assert new_announcement.main_story == result.main_story
    assert new_announcement.organization == result.organization
    assert new_announcement.state == result.state
    assert new_announcement.slug == result.slug
    assert new_announcement.image == result.image
    assert new_announcement.publish == result.publish
    assert len(announcement_svc_integration.get_announcements()) == 4




# def test_add_announcements(announcement_svc_integration: AnnouncementsService):
#     announcement = Announcements(
#         id=1, headline="headline 1", synopsis="synopsis 1",
#         main_story="main story 1", organization="org 1", state=State.Draft,
#         slug="slug 1", image="image 1", publish="publish 1",
#         modification="00-00-20", author_id=1
#     )
#     result = AnnouncementsService.create_announcements(user, announcement1)
#     assert result is not None
#     assert announcement.id == result.id
#     assert len(AnnouncementsService.get_announcements(user)) == 1




def test_get_announcements(announcement_svc_integration: AnnouncementsService):
    """Test that get announcements by id returns the correct announcement"""
    results = announcement_svc_integration.get_announcements()
    assert results is not None


    for ind, result in enumerate(results):
        assert result.id == announcements[ind].id
        assert result.headline == announcements[ind].headline
        assert result.synopsis == announcements[ind].synopsis
        assert result.main_story == announcements[ind].main_story
        assert result.organization == announcements[ind].organization
        assert result.state == announcements[ind].state
        assert result.slug == announcements[ind].slug
        assert result.image == announcements[ind].image
        assert result.publish == announcements[ind].publish




def test_update_announcements(announcement_svc_integration: AnnouncementsService):
    """Test that updating a announcement properly edits the announcement's fields"""
    updated_announcement = announcement_svc_integration.update_announcements(
        root, updated_announcement1
    )
    assert updated_announcement is not None
    assert updated_announcement1.headline == updated_announcement.headline
    assert updated_announcement1.synopsis == updated_announcement.synopsis
    assert updated_announcement1.main_story == updated_announcement.main_story
    assert updated_announcement1.organization == updated_announcement.organization
    assert updated_announcement1.state == updated_announcement.state
    assert updated_announcement1.slug == updated_announcement.slug
    assert updated_announcement1.image == updated_announcement.image
    




def test_announcement_none_exists(announcement_svc_integration: AnnouncementsService):
    """Test that attempting to update a timer that does not exist raises a ResourceNotFoundException"""
    with pytest.raises(HTTPException):
        announcement_svc_integration.update_announcements(root, new_announcement)




def test_delete_announcement(announcement_svc_integration: AnnouncementsService):
    """Test that deleting a announcement appropriately removes the announcement"""
    announcement_svc_integration.delete_announcements_slug(root, announcement1.slug)


    result = announcement_svc_integration.get_announcements()
    assert len(announcements) - 1 == len(result)
    assert announcements[0] not in result
