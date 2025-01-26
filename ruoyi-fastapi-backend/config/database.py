from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from urllib.parse import quote_plus
from config.env import DataBaseConfig
from typing_extensions import Annotated
from sqlalchemy import String,Text,func,text
from datetime import datetime
from uuid import uuid4




ASYNC_SQLALCHEMY_DATABASE_URL = (
    f'mysql+asyncmy://{DataBaseConfig.db_username}:{quote_plus(DataBaseConfig.db_password)}@'
    f'{DataBaseConfig.db_host}:{DataBaseConfig.db_port}/{DataBaseConfig.db_database}'
)
if DataBaseConfig.db_type == 'postgresql':
    ASYNC_SQLALCHEMY_DATABASE_URL = (
        f'postgresql+asyncpg://{DataBaseConfig.db_username}:{quote_plus(DataBaseConfig.db_password)}@'
        f'{DataBaseConfig.db_host}:{DataBaseConfig.db_port}/{DataBaseConfig.db_database}'
    )

async_engine = create_async_engine(
    ASYNC_SQLALCHEMY_DATABASE_URL,
    echo=DataBaseConfig.db_echo,
    max_overflow=DataBaseConfig.db_max_overflow,
    pool_size=DataBaseConfig.db_pool_size,
    pool_recycle=DataBaseConfig.db_pool_recycle,
    pool_timeout=DataBaseConfig.db_pool_timeout,
)
AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine)


class Base(DeclarativeBase):
    pass

# uuid 所有的非自增ID都可以使用这个类型
uuidPk = Annotated[String(36), mapped_column(primary_key=True, server_default=text('uuid()'), default=lambda: str(uuid4()))]
# 创建时间/更新时间
create_time = Annotated[datetime,mapped_column(nullable=False, server_default=func.CURRENT_TIMESTAMP()),]
