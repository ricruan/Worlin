from fastapi import APIRouter, Body, Depends
from module_coding.service.sql_exec_service import SqlExecuteService
from module_coding.service.wr_problem_service import WrProblemService
from utils.response_util import ResponseUtil
from config.get_db import get_db
from sqlalchemy.ext.asyncio import AsyncSession


sqlExecuteController = APIRouter(prefix='/coding')

@sqlExecuteController.post("/execute", tags=['SQL执行'])
async def execute_sql(
    sql: str = Body(..., title="SQL语句", embed=True)
):
    """
    执行SQL语句（支持多语句）
    """
    try:
        results = await SqlExecuteService.execute_sqls(sql)
        return ResponseUtil.success(data=results)
    except Exception as e:
        return ResponseUtil.error(msg=str(e))

@sqlExecuteController.post("/validate", tags=['SQL验证'])
async def validate_sql(
    problem_id: str = Body(..., title="问题ID", embed=True),
    sql: str = Body(..., title="用户SQL", embed=True),
    query_db: AsyncSession = Depends(get_db)
):
    """
    SQL验证接口
    """
    try:
        # 获取问题详情
        problem = await WrProblemService.getDetail(query_db, problem_id)
        if not problem:
            return ResponseUtil.error(msg="问题不存在")
            
        # 执行用户SQL（带预设代码）
        user_result = await SqlExecuteService.execute_sqls(sql)

        print("用户SQL执行结果：", user_result)
        
        # 执行测试SQL（带预设代码+测试用例）
        test_sql = f"{problem.preset_code}\n{problem.test_cases_answers}"  # 假设问题实体有test_sql字段
        is_match = False
        try:
            test_result = await SqlExecuteService.execute_sqls(test_sql)
            print("测试SQL执行结果：", test_result)
            
            # 新的比较逻辑：只比较数据部分
            is_match = len(user_result) == len(test_result)
            if is_match:
                for u_res, t_res in zip(user_result, test_result):
                    # 仅比较查询结果的数据部分
                    if u_res.get('type') == 'query' and t_res.get('type') == 'query':
                        # 标准化数据比较（忽略顺序）
                        u_data = sorted(u_res.get('data', []), key=lambda x: sorted(x.items()))
                        t_data = sorted(t_res.get('data', []), key=lambda x: sorted(x.items()))
                        if u_data != t_data:
                            is_match = False
                            break
        except Exception as e:
            print("测试SQL执行异常:", str(e))
        
        return ResponseUtil.success(data={
            "status": "success" if is_match else "failed",
            "user_result": user_result,
            "error": None if is_match else "查询结果与测试用例结果不符合"
        })
        
    except Exception as e:
        return ResponseUtil.error(
            msg=str(e),
            data={"user_result": await SqlExecuteService.execute_sqls(sql)} if "preset_sql" in locals() else None
        ) 