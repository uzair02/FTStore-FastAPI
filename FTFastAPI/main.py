import threading
from fastapi import FastAPI
from controllers import scraper_controller
from utils.database import engine, Base
from utils.scheduler import run_scraper

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(scraper_controller.router)

@app.on_event("startup")
async def startup_event():
    """
    Startup event handler for the FastAPI application.

    This function starts a background thread to run the Scrapy scraper.
    """
    thread = threading.Thread(target=run_scraper)
    thread.start()
