from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import models, schemas, services
from database import  SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message" : "Hello World!"}

@app.get('/prova/{id}')
async def prova(id: int):
    return {"valore" : id}

@app.post("/classrooms/", response_model=schemas.Classroom)
def create_classroom(classroom: schemas.ClassroomCreate, db: Session = Depends(get_db)):
    db_classroom = services.get_classroom_by_name(db, class_name=classroom.class_name)
    if db_classroom:
        raise HTTPException(status_code=400, detail="Classroom already exist")
    return services.create_classroom(db=db, classroom=classroom)

@app.get("/classrooms/", response_model=list[schemas.Classroom])
def read_classrooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    classrooms = services.get_classroms(db, skip=skip, limit=limit)
    return classrooms

@app.get("/classrooms/{class_id}", response_model=schemas.Classroom)
def read_classroom(class_id: int, db: Session = Depends(get_db)):
    db_classroom = services.get_classroom(db, class_id=class_id)
    if db_classroom is None:
        raise HTTPException(status_code=404, detail="Classroom not found")
    return db_classroom

@app.post("/classrooms/{class_id}/subjects/", response_model=schemas.Subject)
def create_classroom_subject(class_id: int, subject: schemas.SubjectCreate, db: Session = Depends(get_db)):
    db_classroom = services.get_classroom(db, class_id=class_id)
    if db_classroom is None:
        raise HTTPException(status_code=404, detail="Classroom not found")
    db_subject = services.get_classroom_subjects_by_name(db, class_id=class_id, subject_name=subject.name)
    if db_subject:
        raise HTTPException(status_code=400, detail="Subject %s already exist in selected classroom" %subject.name)
    return services.create_classroom_subject(db=db, subject=subject, class_id=class_id)

@app.get("/classrooms/{class_id}/subjects/", response_model=list[schemas.Subject])
def read_classroom_subjects(class_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_classroom = services.get_classroom(db, class_id=class_id)
    if db_classroom is None:
        raise HTTPException(status_code=404, detail="Classroom not found")
    db_subjects = services.get_classroom_subjects(db, class_id, skip=skip, limit=limit)
    return db_subjects

@app.post("/classrooms/{class_id}/{subject_id}/exercises", response_model=schemas.Exercise)
def create_subject_exercises(class_id: int, subject_id: int, exercise: schemas.ExerciseCreate, db: Session = Depends(get_db)):
    db_classroom = services.get_classroom(db, class_id=class_id)
    if db_classroom is None:
        raise HTTPException(status_code=404, detail="Classroom not found")
    db_subject = services.get_subject(db, subject_id=subject_id)
    if db_subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    return services.create_subject_exercise(db=db, exercise=exercise, subject_id=subject_id)

@app.get("/classrooms/{class_id}/{subject_id}/exercises", response_model=list[schemas.Exercise])
def read_subject_exercises(class_id: int, subject_id, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_classroom = services.get_classroom(db, class_id=class_id)
    if db_classroom is None:
        raise HTTPException(status_code=404, detail="Classroom not found")
    db_subject = services.get_subject(db, subject_id=subject_id)
    if db_subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    db_subjects = services.get_subject_exercises(db, subject_id, skip=skip, limit=limit)
    return db_subjects

@app.delete("/classrooms/{class_id}")
def delete_classroom(class_id: int, db: Session = Depends(get_db)):
    db_classroom = services.get_classroom(db, class_id=class_id)
    if db_classroom is None:
        raise HTTPException(status_code=404, detail="Classroom not found")
    return services.delete_classroom(db, class_id)

@app.delete("/classrooms/{class_id}/{subject_id}")
def delete_subject(class_id: int, subject_id: int, db: Session = Depends(get_db)):
    db_classroom = services.get_classroom(db, class_id=class_id)
    if db_classroom is None:
        raise HTTPException(status_code=404, detail="Classroom not found")
    db_subject = services.get_subject(db, subject_id=subject_id)
    if db_subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    return services.delete_classroom_subject(db, subject_id)

@app.delete("/classrooms/{class_id}/{subject_id}/{exercise_id}")
def delete_exercise(class_id: int, subject_id: int, exercise_id: int, db: Session = Depends(get_db)):
    db_classroom = services.get_classroom(db, class_id=class_id)
    if db_classroom is None:
        raise HTTPException(status_code=404, detail="Classroom not found")
    db_subject = services.get_subject(db, subject_id=subject_id)
    if db_subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    db_exercise = services.get_exercise(db, exercise_id=exercise_id)
    if db_exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return services.delete_subject_exercise(db, exercise_id)