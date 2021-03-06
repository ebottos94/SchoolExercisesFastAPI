from unicodedata import name
from sqlalchemy.orm import Session
import models, schemas
import security
import pandas as pd
import sqlite3
import os
from config import settings
def get_classroom(db: Session, class_id: int):
    return db.query(models.Classroom).filter(models.Classroom.id == class_id).first()

def get_subject(db: Session, subject_id: int):
    return db.query(models.Subject).filter(models.Subject.id == subject_id).first()

def get_exercise(db: Session, exercise_id: int):
    return db.query(models.Exercise).filter(models.Exercise.id == exercise_id).first()

def get_classroom_by_name(db: Session, class_name: str):
    return db.query(models.Classroom).filter(models.Classroom.class_name == class_name).first()

def get_user_by_name(db: Session, username: str):
    return db.query(models.Classroom).filter(models.User.username == username).first()


def get_classroms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Classroom).offset(skip).limit(limit).all()

def get_classroom_subjects(db: Session, class_id: int,  skip: int = 0, limit: int = 100):
    return db.query(models.Subject).filter(models.Subject.class_id == class_id).offset(skip).limit(limit).all()

def get_classroom_subjects_by_name(db: Session, class_id: int, subject_name: str):
    return db.query(models.Subject).filter(models.Subject.class_id == class_id, models.Subject.name == subject_name).first()

def get_subject_exercises(db: Session, subject_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Exercise).filter(models.Exercise.subject_id == subject_id).offset(skip).limit(limit).all()


def create_classroom(db: Session, classroom: schemas.ClassroomCreate):
    db_class = models.Classroom(class_name=classroom.class_name)
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class


def get_subjects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Subject).offset(skip).limit(limit).all()


def create_classroom_subject(db: Session, subject: schemas.SubjectCreate, class_id: int):
    db_subject = models.Subject(**subject.dict(), class_id=class_id)
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

def create_subject_exercise(db: Session, exercise: schemas.ExerciseCreate, subject_id: int):
    db_exercise = models.Exercise(**exercise.dict(), subject_id=subject_id)
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise

def delete_classroom(db: Session, class_id: int):
    classroom = db.get(models.Classroom, class_id)
    db.delete(classroom)
    subject_id = db.query(models.Subject.id).filter(models.Subject.class_id == class_id).offset(0).limit(100).all()
    for id in subject_id :
        db.query(models.Exercise).filter(models.Exercise.subject_id == int(id[0])).delete()
    db.query(models.Subject).filter(models.Subject.class_id == class_id).delete()
    db.commit()
    return {"ok": True}

def delete_classroom_subject(db: Session, subject_id: int):
    subject = db.get(models.Subject, subject_id)
    db.delete(subject)
    db.query(models.Exercise).filter(models.Exercise.subject_id == subject_id).delete()
    db.commit()
    return {"ok": True}

def delete_subject_exercise(db: Session, exercise_id: int):
    exercise = db.get(models.Exercise, exercise_id)
    db.delete(exercise)
    db.commit()
    return {"ok": True}

def create_user(db: Session, username: schemas.UserCreate, password: str):
    hashed_password = security.get_password_hash(password)
    db_user = models.User(**username.dict(), hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_db_csv():
    location = os.path.dirname(__file__)
    path_db_full = settings.path_db
    path_db = path_db_full.split('/')[-1]
    abs_db_path = os.path.join(location, path_db)
    conn = sqlite3.connect(abs_db_path, isolation_level=None,
                       detect_types=sqlite3.PARSE_COLNAMES)
    query_string = """
        SELECT classrooms.class_name as "Classroom Name",  school_subject.name as "Subject Name", exercise.title as "Exercise"
        FROM classrooms , school_subject, exercise
        WHERE classrooms.id = school_subject.class_id
        AND school_subject.id = exercise.subject_id
        order by classrooms.id, school_subject.id
    """
    db_df = pd.read_sql_query(query_string, conn)
    db_df.to_csv('database_classi.csv', index=False)
    csv_path = os.path.join(location, 'database_classi.csv')
    return csv_path
