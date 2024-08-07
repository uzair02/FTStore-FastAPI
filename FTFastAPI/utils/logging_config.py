from loguru import logger

logger.add("logs/app.log", rotation="500 MB", retention="10 days", backtrace=True, diagnose=True)
