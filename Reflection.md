#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 17:18:28 2026

@author: manonkling
"""

Developing this Flask-based clinical records REST API provided significant direct experience with data persistence and interoperability in healthcare information systems. I began by creating a Python virtual environment and installing Flask, SQLAlchemy, and Pydantic. I then developed a clinical database model, implemented data validation, and configured POST and GET endpoints to create and retrieve patient records.

As the project progressed, I expanded the existing clinical data structure by adding three additional fields: blood pressure, heart rate, and oxygen saturation. These additions helped me understand how database models, validation schemas, and API endpoints must remain consistent when presenting new information.

What surprised me most was how one POST request could store the same clinical record in both a SQLite database and a JSON Lines file. Testing the endpoints with curl and inspecting both storage formats confirmed the importance of validating data.

This assignment improved my understanding of RESTful APIs, database persistence, and structured clinical information. Moving forward, I want to explore how healthcare organizations maintain consistency across multiple storage systems when errors or interruptions occur.

