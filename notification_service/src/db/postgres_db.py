from core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool

async_engine = create_async_engine(
    settings.db_connection,
    echo=True,
    poolclass=AsyncAdaptedQueuePool,
    future=True
)
async_session = async_sessionmaker(
    bind=async_engine,
    future=True,
    expire_on_commit=False
)
base = declarative_base()

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session