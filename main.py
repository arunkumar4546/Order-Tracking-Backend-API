from fastapi import FastAPI,APIRouter
from fastapi import Request
from app.core.logging import logger
from app.core.db import Base, engine
from app.core.admin import create_admin
from app.core.db import SessionLocal
import os
import app.api.user as user
import app.api.order as order

app = FastAPI(title="Order Service")

Base.metadata.create_all(bind=engine)

# ✅ Middleware goes HERE

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url}")

    response = await call_next(request)

    logger.info(f"Response status: {response.status_code}")

    return response

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("CREATE_ADMIN") == "true":
        db = SessionLocal()
        try:
            create_admin(db)
        finally:
            db.close()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(user.router, prefix="/auth")
app.include_router(order.router, prefix="/orders")