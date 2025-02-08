from module_coding.dao.wr_problem_dao import WrProblemDao
from sqlalchemy.ext.asyncio import AsyncSession
from module_coding.entity.vo.wr_problem_query_vo import WrProblemVO
from module_admin.service.login_service import LoginService
from module_admin.entity.vo.user_vo import CurrentUserModel
from utils.log_util import logger






class WrProblemService:
    """问题Service
    """

    @classmethod
    async def getPageList(cls,query_db: AsyncSession,qeuryVo: WrProblemVO,pageSize: int= 10,pageNum: int= 1):

        return await WrProblemDao.search_problems(query_db,qeuryVo,pageSize,pageNum)
    

    @classmethod
    async def insertOrUpdate(cls, query_db: AsyncSession, queryVo: WrProblemVO):
        try:
            # 打印接收到的数据
            logger.info(f"Received data: {queryVo.model_dump()}")
            
            # 处理 enable_flag
            if queryVo.enable_flag is not None:
                queryVo.enable_flag = str(queryVo.enable_flag)
            
            # 设置更新时间和更新人
            queryVo.whenInsertOrUpdate("")

            if queryVo.id:
                logger.info(f"Updating problem with id: {queryVo.id}")
                return await WrProblemDao.update_problem(query_db, queryVo)
            else:
                logger.info("Inserting new problem")
                return await WrProblemDao.add_problem(query_db, queryVo)
        except Exception as e:
            logger.error(f"Error in insertOrUpdate: {str(e)}")
            raise
        
    @classmethod
    async def deleteBatch(cls,query_db: AsyncSession,ids: str):
        return await WrProblemDao.delete_problems(query_db,ids)

    @classmethod
    async def getDetail(cls, query_db: AsyncSession, id: str):
        # 添加类型转换和错误处理
        try:
            problem_id = id
            return await WrProblemDao.get_problem_by_id(query_db, problem_id)
        except ValueError:
            raise ValueError("无效的问题ID格式")
        except Exception as e:
            logger.error(f"获取问题详情失败: {str(e)}")
            raise

