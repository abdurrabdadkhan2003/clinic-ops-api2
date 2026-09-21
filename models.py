from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, func
from database import Base

class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    contact_number = Column(String(20))
    created_at = Column(TIMESTAMP, server_default=func.now())
