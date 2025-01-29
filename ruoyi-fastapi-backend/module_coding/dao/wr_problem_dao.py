from typing import List, Optional
from sqlalchemy import select,delete
from sqlalchemy.orm import Session
from config.database import AsyncSessionLocal, async_engine, Base # 导入异步的session
from sqlalchemy.ext.asyncio import AsyncSession
from module_coding.entity.vo.wr_problem_query_vo import WrProblemVO
from module_coding.entity.bo.wr_problem_bo import wrProblem
from utils.log_util import logger
from uuid import uuid4
from utils.page_util import PageUtil,PageResponseModel






class WrProblemDao:
    """
    题目表 DAO (Data Access Object)
    """

    @classmethod
    async def add_problem(cls,db: AsyncSession, problem: WrProblemVO) -> None:
        """
        添加题目
        """
        problem.id = uuid4()
        bo = wrProblem(**problem.model_dump())
        async with db as session:
            session.add(bo)
            await session.commit()

    @classmethod
    async def add_problems(cls, problems: List[WrProblemVO]) -> None:
        """
        批量添加题目
        """
        async with AsyncSessionLocal() as session:
            session.add_all(problems)
            await session.commit()


    @classmethod
    async def delete_problems(cls,db: AsyncSession, ids: str) -> None:
        """
        根据 ID 删除题目
        """
        idList = ids.split(",")
        async with db as session:
            stmt = delete(wrProblem).where(wrProblem.id._in(idList))
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def update_problem(cls,db: AsyncSession ,  problem: WrProblemVO) -> None:
        """
        根据 ID 更新题目
        """
        bo = wrProblem(**problem.model_dump())
        async with db as session:
            await session.merge(bo)
            await session.commit()

            

    @classmethod
    async def get_problem_by_id(cls, problem_id: str) -> Optional[WrProblemVO]:
        """
          根据ID 获取题目信息
        """
        async with AsyncSessionLocal() as session:
             stmt = select(wrProblem).where(wrProblem.id == problem_id)
             problem =  await session.execute(stmt).scalar_one_or_none()
             return problem

    async def get_problems(self, limit: int = 10, offset: int = 0) -> List[WrProblemVO]:
      """
       获取所有题目信息
      """
      async with AsyncSessionLocal() as session:
        stmt = select(WrProblemVO).limit(limit).offset(offset)
        problems = await session.execute(stmt).scalars().all()
        return list(problems)
    
    @classmethod
    async def get_problems_by_type(cls, problem_type: str, limit: int = 10, offset: int = 0) -> List[WrProblemVO]:
     """
     根据类型获取题目列表
     """
     async with AsyncSessionLocal() as session:
        stmt = select(wrProblem).where(wrProblem.problem_type==problem_type).limit(limit).offset(offset)
        problems = await session.execute(stmt).scalars().all()
        return list(problems)
     
    @classmethod
    async def search_problems(cls, query_db: AsyncSession, queryVo: WrProblemVO, page_size: int = 10, page_num: int = 1) -> PageResponseModel:
        """
        根据关键字搜索题目
        """
        stmt = select(wrProblem)
        if queryVo.problem_title:
            stmt = stmt.where(wrProblem.problem_title.contains(queryVo.problem_title))
        # TODO : 补充一下其他查询条件

        result = await PageUtil.paginate(query_db, stmt, page_num, page_size, True)
        return result
		

		
				
		
		
		