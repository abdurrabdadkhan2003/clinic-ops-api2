from pydantic import BaseModel, constr
from datetime import date, datetime
from typing import Optional

class PatientBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    contact_number: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    contact_number: Optional[str] = None

class PatientResponse(PatientBase):
    patient_id: int
    created_at: datetime

    class Config:
        from_attributes = True
