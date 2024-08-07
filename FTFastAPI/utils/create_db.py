"""Module to create database tables."""

from utils.database import Base, engine

Base.metadata.create_all(bind=engine)
