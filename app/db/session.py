import ssl, certifi
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Crée un contexte SSL qui utilise le bundle certifi
ssl_context = ssl.create_default_context(cafile=certifi.where())

engine = create_async_engine(
    settings.database_url,
    echo=True,
    future=True,
    connect_args={"ssl": ssl_context},
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)