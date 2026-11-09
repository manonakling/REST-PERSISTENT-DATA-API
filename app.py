#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 17:10:58 2026

@author: manonkling
"""


from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from pydantic import BaseModel, Field, ValidationError
from pathlib import Path
import json

# Project directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = BASE_DIR / "clinical_data.db"
JSONL_PATH = DATA_DIR / "clinical_data.jsonl"

# Flask application
app = Flask(__name__)

# SQLite database
engine = create_engine(f"sqlite:///{DB_PATH}")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# Clinical database model
class ClinicalData(Base):
    __tablename__ = "clinical_data"

    id = Column(Integer, primary_key=True)
    patient_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    diagnosis = Column(String, nullable=False)

    # Three additional clinical columns
    blood_pressure = Column(String, nullable=False)
    heart_rate = Column(Integer, nullable=False)
    oxygen_saturation = Column(Integer, nullable=False)


# Pydantic validation schema
class ClinicalDataSchema(BaseModel):
    patient_name: str = Field(min_length=1)
    age: int = Field(ge=0, le=120)
    diagnosis: str = Field(min_length=1)

    blood_pressure: str = Field(
        pattern=r"^\d{2,3}/\d{2,3}$"
    )
    heart_rate: int = Field(ge=1, le=250)
    oxygen_saturation: int = Field(ge=0, le=100)


# Create database tables
Base.metadata.create_all(engine)


# POST: Add a clinical record
@app.route("/clinical/", methods=["POST"])
def add_clinical_record():
    try:
        data = ClinicalDataSchema.model_validate(
            request.get_json()
        )
    except ValidationError as error:
        return jsonify({
            "error": "Invalid clinical data",
            "details": error.errors(
                include_context=False
            )
        }), 400
    except Exception:
        return jsonify({
            "error": "Invalid JSON request"
        }), 400

    session = SessionLocal()

    try:
        record = ClinicalData(**data.model_dump())

        session.add(record)
        session.commit()
        session.refresh(record)

        record_dict = {
            "id": record.id,
            **data.model_dump()
        }

        # Append record to JSON Lines file
        with open(JSONL_PATH, "a", encoding="utf-8") as file:
            file.write(json.dumps(record_dict) + "\n")

        return jsonify(record_dict), 201

    except Exception as error:
        session.rollback()
        return jsonify({
            "error": str(error)
        }), 500

    finally:
        session.close()


# GET: Retrieve all clinical records
@app.route("/clinical/", methods=["GET"])
def get_clinical_records():
    session = SessionLocal()

    try:
        records = session.query(ClinicalData).all()

        results = [
            {
                "id": record.id,
                "patient_name": record.patient_name,
                "age": record.age,
                "diagnosis": record.diagnosis,
                "blood_pressure": record.blood_pressure,
                "heart_rate": record.heart_rate,
                "oxygen_saturation": record.oxygen_saturation
            }
            for record in records
        ]

        return jsonify(results), 200

    finally:
        session.close()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
