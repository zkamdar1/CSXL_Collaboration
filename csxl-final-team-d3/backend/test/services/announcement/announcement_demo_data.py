# test data
import pytest
from sqlalchemy.orm import Session


from ....entities.announcements_entity import AnnouncementEntity


from ....models.announcements import Announcements, State


from ..reset_table_id_seq import reset_table_id_seq


from ..user_data import user


__authors__ = ["Jade Keegan"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


announcement1 = AnnouncementEntity(
    id=1,
    headline="headline 1",
    synopsis="synopsis 1",
    main_story="main story 1",
    organization="org 1",
    state=State.Draft,
    slug="slug 1",
    image="image 1",
    publish="publish 1",
    modification="00-00-20",
    author_id=1,
)
announcement2 = AnnouncementEntity(
    id=2,
    headline="headline 2",
    synopsis="synopsis 2",
    main_story="main story 2",
    organization="org 2",
    state=State.Published,
    slug="slug 2",
    image="image 2",
    publish="publish 2",
    modification="0000000",
    author_id=1,
)
announcement3 = AnnouncementEntity(
    id=3,
    headline="headline 3",
    synopsis="synopsis 3",
    main_story="main story 3",
    organization="org 3",
    state=State.Draft,
    slug="slug 3",
    image="image 3",
    publish="publish 3",
    modification="1212121",
    author_id=1,
)




announcements = [announcement1, announcement2, announcement3]




def insert_fake_data(session: Session):
    """Inserts fake pomodoro timer data into the test session."""


    global announcements


    # Create entities for test organization data
    entities = []
    for ann_entity in announcements:
        # Timers created will be associated with Sally Student
        # ann_entity = AnnouncementEntity.from_model(announcement)
        session.add(ann_entity)
        entities.append(ann_entity)


    # Reset table IDs to prevent ID conflicts
    reset_table_id_seq(
        session, AnnouncementEntity, AnnouncementEntity.id, len(announcements) + 1
    )


    # Commit all changes
    session.commit()




@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    """Insert fake data the session automatically when a test is run.
    Note:
        This function runs automatically for each test due to the fixture property `autouse=True`.
    """
    insert_fake_data(session)
    session.commit()
    yield
