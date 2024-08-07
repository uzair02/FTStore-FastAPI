# FTStore

FTStore is a FastAPI-based application that automates data scraping using a nightly crawler. The application collects and updates web data daily at 2 AM, ensuring that users have access to the most current information.

## Features

- Automated data scraping with Scrapy
- Data retrieval and display using FastAPI
- Scheduled scraping every night at 2 AM
- Flexible and maintainable codebase

## Installation

To set up the project, follow these steps:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/FTStore.git

2. **Create and Activate the Virtual Environment**
   
   ```windows
   #for windows
   python -m venv env
   .\env\Scripts\activate

   #for linux
   python3 -m venv env
   source env/bin/activate
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt

5. **Run the Application**
   ```bash
   cd FTStore
   uvicorn main:app --reload

# Project Structure
 - main.py: Entry point for the FastAPI application.
 - controllers/: Contains FastAPI route handlers.
 - models/: Defines database models.
 - schemas/: Pydantic schemas for data validation.
 - utils/: Utility functions and configurations.
 - scrapy/: Scrapy project for data crawling.
 - requirements.txt: List of project dependencies.


# Acknowledgements
 - FastAPI for the web framework.
 - Scrapy for the web crawling framework.
 - APScheduler for the task scheduling.
