#from datamodels import Patient, Diagnosis

from typing import List, Optional

from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select

from aimodels import PatientData
from datamodels import InputFax


class Patient(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    gender: str
    age: int = Field(index=True)
    


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()

def create_patient_from_fax(efaxtext):
    return PatientData(efaxtext)

#print(create_patient_from_fax('vivek tomer is 49 year old male'))

#print(Patient.model_validate(PatientData('vivek tomer is 49 year old male')))


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/patients/", response_model=Patient)
def create_patient(efaxtext: str):
    with Session(engine) as session:
        patient = Patient.model_validate(PatientData(efaxtext))
        session.add(patient)
        session.commit()
        session.refresh(patient)
        return patient


@app.get("/patients/", response_model=List[Patient])
def read_patients():
    with Session(engine) as session:
        patients = session.exec(select(Patient)).all()
        return patients