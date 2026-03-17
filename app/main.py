from fastapi import FastAPI

from app.api import api_router

app = FastAPI(title="LGPD QA Agent API")

app.include_router(api_router)
