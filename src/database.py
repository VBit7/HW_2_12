import contextlib
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine


class Config:
    DB_URL = "postgresql+asyncpg://postgres:Example1234@localhost:5432/hw11"


config = Config


class DatabaseSessionManager:
    def __init__(self, url: str):
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: async_sessionmaker = async_sessionmaker(autoflush=False, autocommit=False,
                                                                     bind=self._engine)

    @contextlib.asynccontextmanager
    async def session(self):
        if self._session_maker is None:
            raise Exception("Session is not initialized")
        session = self._session_maker()
        try:
            yield session
        except Exception as err:
            print(err)
            await session.rollback()
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(config.DB_URL)


async def get_db():
    async with sessionmanager.session() as session:
        # yield session
        return session
