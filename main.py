from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, get_db

# We don't need to create tables because Alembic from Month 1 handles it,
# but this ensures the Base is mapped.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Meditrack Clinic Ops API", version="1.0")

@app.get("/patients", response_model=List[schemas.PatientResponse], tags=["Patients"])
def get_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    patients = db.query(models.Patient).offset(skip).limit(limit).all()
    return patients

@app.get("/patients/{patient_id}", response_model=schemas.PatientResponse, tags=["Patients"])
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.post("/patients", response_model=schemas.PatientResponse, status_code=status.HTTP_201_CREATED, tags=["Patients"])
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    db_patient = models.Patient(**patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@app.put("/patients/{patient_id}", response_model=schemas.PatientResponse, tags=["Patients"])
def update_patient(patient_id: int, patient_update: schemas.PatientUpdate, db: Session = Depends(get_db)):
    db_patient = db.query(models.Patient).filter(models.Patient.patient_id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    update_data = patient_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_patient, key, value)

    db.commit()
    db.refresh(db_patient)
    return db_patient

@app.delete("/patients/{patient_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Patients"])
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = db.query(models.Patient).filter(models.Patient.patient_id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    db.delete(db_patient)
    db.commit()
    return None
