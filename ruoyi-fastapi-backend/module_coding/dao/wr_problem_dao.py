from typing import List, Optional
from sqlalchemy import select,delete, update
from sqlalchemy.orm import Session
from config.database import AsyncSessionLocal, async_engine, Base # 导入异步的session
from sqlalchemy.ext.asyncio import AsyncSession
from module_coding.entity.vo.wr_problem_query_vo import WrProblemVO, WrProblemPageVo
from module_coding.entity.bo.wr_problem_bo import wrProblem
from utils.log_util import logger
from uuid import uuid4
from utils.page_util import PageUtil,PageResponseModel






class WrProblemDao:
    """
    题目表 DAO (Data Access Object)
    """

    @classmethod
    async def add_problem(cls, db: AsyncSession, problem: WrProblemVO) -> None:
        """
        添加题目
        """
        problem.id = str(uuid4())  # 确保 id 是字符串
        # 将 pydantic 模型转换为字典，并排除 None 值
        insert_data = {k: v for k, v in problem.model_dump().items() if v is not None}
        bo = wrProblem(**insert_data)
        
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
    async def update_problem(cls, db: AsyncSession, problem: WrProblemVO) -> None:
        """
        根据 ID 更新题目
        """
        # 确保所有字符串字段使用utf8mb4编码
        problem_dict = problem.model_dump()
        for key, value in problem_dict.items():
            if isinstance(value, str):
                problem_dict[key] = value.encode('utf8').decode('utf8')
                
        bo = wrProblem(**problem_dict)
        async with db as session:
            await session.merge(bo)
            await session.commit()
                
            

    @classmethod
    async def get_problem_by_id(cls, db: AsyncSession, problem_id: str) -> Optional[WrProblemVO]:
        """
        根据ID 获取题目信息
        """
        async with db as session:
            stmt = select(wrProblem).where(wrProblem.id == problem_id)
            result = await session.execute(stmt)
            problem = result.scalar_one_or_none()
            if problem:
                # 将 SQLAlchemy 模型转换为 pydantic 模型，这样会触发驼峰转换
                return WrProblemVO.model_validate(problem)
            return None

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
    async def search_problems(cls, query_db: AsyncSession, queryVo: WrProblemPageVo, page_size: int = 10, page_num: int = 1) -> PageResponseModel:
        """
        根据关键字搜索题目
        """
        stmt = select(wrProblem)
        
        # 添加查询条件，只有当参数不为 None 时才添加条件
        if queryVo.problem_title:
            stmt = stmt.where(wrProblem.problem_title.contains(queryVo.problem_title))
        if queryVo.problem_tags:
            stmt = stmt.where(wrProblem.problem_tags.contains(queryVo.problem_tags))
        if queryVo.language_type:
            stmt = stmt.where(wrProblem.language_type == queryVo.language_type)
        if queryVo.problem_type:
            stmt = stmt.where(wrProblem.problem_type == queryVo.problem_type)
        if queryVo.difficulty_level:
            stmt = stmt.where(wrProblem.difficulty_level == queryVo.difficulty_level)
        if queryVo.enable_flag is not None:
            stmt = stmt.where(wrProblem.enable_flag == queryVo.enable_flag)

        result = await PageUtil.paginate(query_db, stmt, page_num, page_size, True)
        return result
		

		
				
		
		
		