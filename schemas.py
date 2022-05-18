from typing import List, Union

from pydantic import BaseModel


class ExerciseBase(BaseModel):
    title: str


class ExerciseCreate(ExerciseBase):
    pass


class Exercise(ExerciseBase):
    id: int
    subject_id: int

    class Config:
        orm_mode = True

class SubjectBase(BaseModel):
    name: str


class SubjectCreate(SubjectBase):
    pass


class Subject(SubjectBase):
    id: int
    class_id: int
    exercises : List[Exercise] = []

    class Config:
        orm_mode = True


class ClassroomBase(BaseModel):
    class_name: str


class ClassroomCreate(ClassroomBase):
    pass


class Classroom(ClassroomBase):
    id: int
    subjects: List[Subject] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    pass


class UserInDB(UserBase):
    id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

