# test data
import pytest
from sqlalchemy.orm import Session


from ....entities.announcements_entity import AnnouncementEntity


from ....models.announcements import Announcements, State, User


from ..reset_table_id_seq import reset_table_id_seq


from ..user_data import user, root


__authors__ = ["Jade Keegan"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"




announcement1 = Announcements(
    id=1,
    headline="headline 1",
    synopsis="synopsis 1", main_story="main story 1", organization="org 1", state=State.Published, slug="slug 1", image="image 1", publish="publish 1", modification="00-00-20", author_id=user.id
)
announcement2 = Announcements(
    id=2,
    headline="headline 2",
    synopsis="synopsis 2", main_story="main story 2", organization="org 2", state=State.Published, slug="slug 2", image="image 2", publish="publish 2", modification="0000000", author_id=user.id
)
announcement3 = Announcements(
    id=3,
    headline="headline 3",
    synopsis="synopsis 3", main_story="main story 3", organization="org 3", state=State.Published, slug="slug 3", image="image 3", publish="publish 3", modification="1212121", author_id=user.id
)
new_announcement = Announcements(
    id=4,
    headline="string",
    synopsis="str",
    main_story= "My string",
    organization= "My string",
    state= State.Published,
    slug= 'abcde',
    image="My string",
    publish= "My string",
    modification="dfsddfs",
    author_id=root.id
)
updated_announcement1 = Announcements(
    id=1,
    headline="My string",
    synopsis="Mine string",
     main_story= "My string",
     organization= "My string",
     state= State.Published,
     slug= 'abcefgh',
     image="My string",
     publish= "My string",
     modification="dfsdf",
     author_id=user.id
)
announcements = [announcement1, announcement2, announcement3]




def insert_fake_data(session: Session):
    """Inserts fake pomodoro timer data into the test session."""


    global announcements


    # Create entities for test organization data
    entities = []
    for announcement in announcements:
        # Timers created will be associated with Sally Student
        ann_entity = AnnouncementEntity.from_model(user, announcement)
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
