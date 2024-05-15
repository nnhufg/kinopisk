from dataclasses import dataclass, field
from datetime import date, datetime
import uuid


@dataclass
class FilmWork:

    created_at: date = None
    updated_at: date = None
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    title: str = ""
    description: str = ""
    creation_date: date = None
    rating: float = 0.0
    type: str = ""
    file_path: str = ""

    def __post_init__(self):
        if self.creation_date is None:
            self.creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        if self.updated_at is None:
            self.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        if self.description is None:
            self.description = "Нет описания"
        if self.rating is None:
            self.rating = 0.0
        if self.file_path is None:
            self.file_path = "Нет пути"


@dataclass
class Genre:

    created_at: date = None
    updated_at: date = None
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    name: str = ""
    description: str = ""

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        if self.updated_at is None:
            self.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        if self.description is None:
            self.description = "Нет описания"
        if self.name is None:
            self.name = "Нет имени"


@dataclass
class Person:

    created_at: date = None
    updated_at: date = None
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    full_name: str = ""

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        if self.updated_at is None:
            self.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        if self.full_name is None:
            self.full_name = "Нет имени"


@dataclass
class GenreFilmwork:

    created_at: date = None
    updated_at: date = None
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: str = ""
    genre_id: str = ""

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        if self.updated_at is None:
            self.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")


@dataclass
class PersonFilmwork:

    created_at: date = None
    updated_at: date = None
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    role: str = ""
    film_work_id: str = ""
    person_id: str = ""

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        if self.updated_at is None:
            self.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        if self.role is None:
            self.role = "Нет роли"
