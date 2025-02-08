from sqlalchemy import text, exc
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_pool import db_pool
from typing import List, Dict, Any, Union
import logging

logger = logging.getLogger(__name__)

class SqlExecuteService:
    """
    SQL执行服务
    """

    @classmethod
    async def execute_sqls(cls, sql: str) -> List[Dict[str, Any]]:
        """
        执行多条SQL语句
        """
        # 分割SQL语句并清理
        statements = [
            stmt.strip() 
            for stmt in sql.split(';') 
            if stmt.strip() and not stmt.strip().startswith('--')
        ]
        
        results = []
        
        # 每次调用获取一个新的engine
        engine = await db_pool.get_engine()
        
        try:
            db_name = engine.url.database
            print(f"执行SQL语句: {sql}, 数据库: {db_name}")
            
            for idx, raw_stmt in enumerate(statements, 1):
                stmt = ' '.join(raw_stmt.split())
                result_info = {
                    "seq": idx,
                    "sql": stmt,
                    "type": cls._get_sql_type(stmt),
                    "status": "success",
                    "data": None,
                    "message": "",
                    "rows_affected": 0
                }
                
                try:
                    async with AsyncSession(bind=engine) as session:
                        # 开始独立事务
                        async with session.begin():
                            result = await session.execute(text(stmt))
                            
                            if result.returns_rows:
                                # 查询语句
                                rows = result.mappings().all()
                                result_info["data"] = [dict(row) for row in rows]
                                result_info["rows_affected"] = len(rows)
                            else:
                                # DML/DDL语句
                                await session.commit()
                                result_info["rows_affected"] = result.rowcount
                                
                except exc.SQLAlchemyError as e:
                    result_info["status"] = "error"
                    result_info["message"] = f"{type(e).__name__}: {str(e)}"
                    logger.error(f"SQL执行失败: {stmt} | 错误: {str(e)}")
                
                results.append(result_info)
                
        finally:
            await db_pool.release_engine(engine)
            
        return results

    @staticmethod
    def _get_sql_type(stmt: str) -> str:
        stmt = stmt.upper()
        if stmt.startswith("SELECT"):
            return "query"
        elif stmt.startswith(("INSERT", "UPDATE", "DELETE")):
            return "dml"
        elif stmt.startswith(("CREATE", "ALTER", "DROP")):
            return "ddl"
        else:
            return "other" 