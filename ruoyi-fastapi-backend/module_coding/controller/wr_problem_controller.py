from fastapi import APIRouter, Depends, Request
from module_coding.service.wr_problem_service import WrProblemService
from module_admin.annotation.log_annotation import Log
from sqlalchemy.ext.asyncio import AsyncSession
from config.get_db import get_db
from config.enums import BusinessType
from module_coding.entity.vo.wr_problem_query_vo import WrProblemVO,WrProblemPageVo
from utils.response_util import ResponseUtil
from typing import List
from module_admin.service.login_service import oauth2_scheme







wrProblemController = APIRouter(prefix='/wr/problem')

@wrProblemController.get("/pagelist", response_model=List[WrProblemVO])
async def getList(
        request: Request,
        queryVo: WrProblemPageVo = Depends(WrProblemPageVo.as_query),
        query_db: AsyncSession = Depends(get_db)) :
    problems = await WrProblemService.getPageList(query_db,queryVo,queryVo.page_size,queryVo.page_num)
    return ResponseUtil.success(problems)

    

@wrProblemController.post("/inserOrUpdate")
async def insertOrUpdate(
        request: Request,
        queryVo: WrProblemVO,
        query_db: AsyncSession = Depends(get_db)) :
    return ResponseUtil.success(await WrProblemService.insertOrUpdate(query_db,queryVo))


@wrProblemController.delete("/deleteBatch")
@Log(title='问题管理', business_type=BusinessType.DELETE)
async def deleteBatch(
        request: Request,
        ids: str,
        query_db: AsyncSession = Depends(get_db)) :
    return ResponseUtil.success(await WrProblemService.deleteBatch(query_db,ids))