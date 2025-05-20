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
    id=15,
    headline="CS Workshop: Intro to AI",
    synopsis="A beginner's workshop on Artificial Intelligence and Machine Learning.",
    main_story="Explore the basics of AI and ML with hands-on sessions.",
    organization="Tech University",
    state=State.Published,
    slug="intro-to-ai-workshop",
    image="image1.jpg",
    publish="2024-04-29T09:13:00",
    modification="2024-04-29T11:13:00",
    author_id=1
)

announcement2 = AnnouncementEntity(
    id=16,
    headline="Blockchain Basics",
    synopsis="Understanding Blockchain technology and its applications.",
    main_story="A comprehensive guide to blockchain technology and future trends.",
    organization="Blockchain Hub",
    state=State.Published,
    slug="blockchain-basics",
    image="image2.jpg",
    publish="2024-04-28T14:30:00",
    modification="2024-04-28T15:45:00",
    author_id=1
)

announcement3 = AnnouncementEntity(
    id=17,
    headline="Spring Hackathon 2024",
    synopsis="Annual coding event focused on environmental solutions.",
    main_story="Details of the upcoming Spring Hackathon, including prizes and judges.",
    organization="Community Code",
    state=State.Published,
    slug="spring-hackathon-2024",
    image="image3.jpg",
    publish="2024-04-26T18:15:00",
    modification="2024-04-26T20:30:00",
    author_id=1
)

# Previously provided announcements for April 27 to April 30
# Recapitulating new entries after April 30

announcement5 = AnnouncementEntity(
    id=5,
    headline="Quantum Computing Seminar",
    synopsis="Seminar on the impact of quantum computing in current technology.",
    main_story="Dive into the world of quantum computing with experts from around the globe.",
    organization="Quantum Innovations",
    state=State.Published,
    slug="quantum-computing-seminar",
    image="image5.jpg",
    publish="2024-05-01T10:00:00",
    modification="2024-05-01T12:00:00",
    author_id=1
)

announcement6 = AnnouncementEntity(
    id=6,
    headline="Future of VR in Education",
    synopsis="Exploring virtual reality applications in educational settings.",
    main_story="Join us to discuss the transformative potential of VR technologies in education.",
    organization="EdTech Association",
    state=State.Published,
    slug="future-of-vr",
    image="image6.jpg",
    publish="2024-05-02T09:00:00",
    modification="2024-05-02T11:00:00",
    author_id=1
)

announcement7 = AnnouncementEntity(
    id=7,
    headline="Cybersecurity Conference 2024",
    synopsis="Annual conference focusing on new threats and protection strategies in cybersecurity.",
    main_story="Cybersecurity experts gather to share insights on protecting digital assets.",
    organization="Cybersecurity League",
    state=State.Published,
    slug="cybersecurity-conference-2024",
    image="image7.jpg",
    publish="2024-05-03T14:00:00",
    modification="2024-04-29T16:01:00",
    author_id=1
)

new_announcement = AnnouncementEntity(
    id=None,
    headline="string",
    synopsis="str", 
    main_story= "My string",
    organization= "My string",
    state= State.Draft,
    slug= 'abc',
    image="My string",
    publish= "My string",
    modification="dfsddfs",
    author_id=1
)
updated_announcement1 = AnnouncementEntity(
    id=1,
    headline="My string",
    synopsis="Mine string",
     main_story= "My string",
     organization= "My string",
     state= State.Published,
     slug= 'abc',
     image="My string",
     publish= "My string",
     modification="dfsdf",
     author_id=1
)
announcement8 = AnnouncementEntity(
    id=8,
    headline="Advanced Machine Learning Workshop",
    synopsis="A deep dive into advanced machine learning techniques and their applications.",
    main_story="Join us for an intensive workshop on advanced ML techniques, including hands-on sessions and expert talks.",
    organization="Tech Innovators",
    state="Published",
    slug="advanced-ml-workshop",
    image="image8.jpg",
    publish="2024-04-29T10:30:05",
    modification="2024-04-29T12:30:05",
    author_id=1
)

announcement9 = AnnouncementEntity(
    id=9,
    headline="IoT Security Challenges",
    synopsis="Exploring the security challenges in the Internet of Things.",
    main_story="An informative session on IoT security vulnerabilities and how to mitigate them.",
    organization="Security Experts Inc.",
    state="Published",
    slug="iot-security",
    image="image9.jpg",
    publish="2024-04-29T14:03:00",
    modification="2024-04-29T16:03:00",
    author_id=1
)

announcement10 = AnnouncementEntity(
    id=10,
    headline="Data Science for Healthcare",
    synopsis="How data science is revolutionizing healthcare.",
    main_story="Learn about the impact of data science on healthcare, featuring case studies and industry insights.",
    organization="HealthTech Analytics",
    state="Published",
    slug="data-science-healthcare",
    image="image10.jpg",
    publish="2024-04-29T09:08:00",
    modification="2024-04-29T11:08:00",
    author_id=1
)

announcement11 = AnnouncementEntity(
    id=11,
    headline="Virtual Reality in Education",
    synopsis="Implementing VR solutions in educational curricula.",
    main_story="Discussion on integrating VR technologies into modern education systems for enhanced learning experiences.",
    organization="EduTech Pioneers",
    state="Published",
    slug="vr-education",
    image="image11.jpg",
    publish="2024-04-29T12:00:00",
    modification="2024-04-29T12:00:00",
    author_id=1
)

announcements = [announcement1, announcement2, announcement3, announcement5, announcement6, announcement7, announcement8, announcement9, announcement10, announcement11]


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
