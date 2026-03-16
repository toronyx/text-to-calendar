from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from ptc_server.routes.endpoints import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO 16-Mar-2026 load any services here
    try:
        yield # app runs here
    finally:
        pass # do any cleanup

app = FastAPI(title="Job Hunt Automation API", lifespan=lifespan)

app.include_router(router)