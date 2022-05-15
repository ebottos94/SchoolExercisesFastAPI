from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Classroom(Base):
    __tablename__ = "classrooms"

    id = Column(Integer, primary_key=True, index=True)
    class_name = Column(String, unique=True, index=True)

    subjects = relationship("Subject", back_populates="classroom")


class Subject(Base):
    __tablename__ = "school_subject"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    class_id = Column(Integer, ForeignKey("classrooms.id"))

    classroom = relationship("Classroom", back_populates="subjects")
    exercises = relationship("Exercise", back_populates="subjects")

class Exercise(Base):
    __tablename__ = "exercise"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    subject_id = Column(Integer, ForeignKey("school_subject.id"))

    subjects = relationship("Subject", back_populates="exercises")
