from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from api.v1.event_setter import router
from aio_pika import connect_robust

from core.config import settings
from services.broker_service import broker_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    broker_service.connection = await connect_robust(settings.rabbit_connection)
    broker_service.channel = await broker_service.connection.channel()
    broker_service.exchange = await broker_service.channel.declare_exchange(settings.rabbit_exchange)
    yield
    await broker_service.channel.close()
    await broker_service.connection.close()

app = FastAPI(
    lifespan=lifespan,
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    debug=True,
)

app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.service_port,
        reload=True,   
    )