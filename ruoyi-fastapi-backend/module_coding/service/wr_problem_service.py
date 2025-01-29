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
    async def insertOrUpdate(cls,query_db: AsyncSession,qeuryVo: WrProblemVO):
        # user = await LoginService.get_current_user()
        # TODO : 这里当前用户需要处理下
        # qeuryVo.whenInsertOrUpdate(user.user_id)

        qeuryVo.whenInsertOrUpdate("")


        if qeuryVo.id :
            return await WrProblemDao.update_problem(query_db,qeuryVo)
        else :
            return await WrProblemDao.add_problem(query_db,qeuryVo)
        
    
    async def deleteBatch(cls,query_db: AsyncSession,ids: str):
        return await WrProblemDao.delete_problems(query_db,ids)

