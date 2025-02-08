import asyncio
from typing import List, Optional
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker
from config.database import async_engine, DataBaseConfig
from utils.log_util import logger

class DBPoolManager:
    """
    改进版数据库连接池管理器
    管理预创建的AsyncEngine实例，支持动态扩容
    """
    def __init__(self):
        self.base_db_name = DataBaseConfig.db_database
        self.pool_size = DataBaseConfig.db_pool_size
        self.engine_pool: List[AsyncEngine] = []
        self.in_use_engines: List[AsyncEngine] = []
        self.lock = asyncio.Lock()
        self.counter = 0  # 用于生成唯一数据库名称

    async def initialize(self):
        """初始化预定义的连接池"""
        async with self.lock:
            for i in range(self.pool_size):
                db_name = f"user_db_{i}"
                engine = await self.create_engine_with_db(db_name)
                self.engine_pool.append(engine)
            logger.info(f"Initialized database pool with {self.pool_size} engines")

    async def create_engine_with_db(self, db_name: str) -> AsyncEngine:
        """创建新的数据库和对应引擎"""
        async with async_engine.connect() as conn:
            # 确保数据库存在
            await conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{db_name}`"))
            await conn.commit()

        # 构建包含数据库名称的连接URL
        return create_async_engine(
            f"{async_engine.url.drivername}://"
            f"{async_engine.url.username}:{async_engine.url.password}@"
            f"{async_engine.url.host}:{async_engine.url.port}/{db_name}",
            echo=DataBaseConfig.db_echo,
            pool_size=1,
            connect_args={
                'charset': 'utf8mb4',
                'ssl': {'ssl_mode': 'DISABLED'}
            }
        )

    async def get_engine(self) -> Optional[AsyncEngine]:
        """获取一个可用的数据库引擎"""
        import random
        async with self.lock:
            if self.engine_pool:
                engine = random.choice(self.engine_pool)
                self.engine_pool.remove(engine)
                self.in_use_engines.append(engine)
                return engine
            
            # 动态扩容创建新引擎
            self.counter += 1
            db_name = f"user_db_dyn_{self.counter}"
            new_engine = await self.create_engine_with_db(db_name)
            self.in_use_engines.append(new_engine)
            logger.info(f"Created dynamic database engine: {db_name}")
            return new_engine
        
    async def get_db(self):
        """获取一个可用的数据库"""
        engine = await self.get_engine()
        async with async_sessionmaker(autocommit=False, autoflush=False, bind=engine) as db:
            yield db

    async def release_engine(self, engine: AsyncEngine):
        """释放并重置引擎对应的数据库"""
        async with self.lock:
            if engine in self.in_use_engines:
                db_name = engine.url.database
                try:
                    async with engine.connect() as conn:
                        print(f"正在重置数据库: {db_name}")
                        # 重置前确保使用目标数据库
                        await conn.execute(text(f"USE `{db_name}`"))
                        await conn.execute(text(f"DROP DATABASE IF EXISTS `{db_name}`"))
                        await conn.execute(text(f"CREATE DATABASE `{db_name}`"))
                        await conn.commit()
                except Exception as e:
                    logger.error(f"重置数据库失败: {db_name} - {str(e)}")
                    await engine.dispose()  # 出现异常时销毁引擎
                finally:
                    self.in_use_engines.remove(engine)
                    self.engine_pool.append(engine)

    async def close_all(self):
        """关闭所有引擎连接"""
        async with self.lock:
            for engine in self.engine_pool + self.in_use_engines:
                await engine.dispose()
            self.engine_pool.clear()
            self.in_use_engines.clear()
            logger.info("Closed all database engines")

# 全局单例实例
db_pool = DBPoolManager()

async def init_db_pool():
    """应用启动时初始化"""
    await db_pool.initialize()

async def close_db_pool():
    """应用关闭时清理"""
    await db_pool.close_all() 