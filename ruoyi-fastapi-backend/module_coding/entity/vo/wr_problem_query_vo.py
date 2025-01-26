from pydantic import BaseModel,Field,ConfigDict
from typing import Optional, List
from datetime import datetime
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank, Size
from module_admin.annotation.pydantic_annotation import as_query



class WrProblemVO(BaseModel):
    """
    题目表 VO (Value Object)
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)


    id: Optional[str] = Field(None, description="问题标识")
    problem_title: Optional[str] = Field(None, min_length=1, max_length=255, description="问题标题")
    problem_tags: Optional[str] = Field(None, max_length=255, description="问题标签")
    problem_content: Optional[str] = Field(None, description="问题内容")
    language_type: Optional[str] = Field(None, max_length=50, description="语言类型 (mysql、oracle)")
    problem_type: Optional[str] = Field(None, max_length=20, description="问题类型（选择题、编程题、填空题、问答题）")
    difficulty_level: Optional[str] = Field(None, max_length=20, description="难度层级 （难度层级）")
    preset_code: Optional[str] = Field(None, description="预设代码")
    test_cases_answers: Optional[str] = Field(None, description="测试用例\\答案")
    enable_flag: Optional[str] = Field(None, max_length=1, description='启用标识 （是否启用）')
    create_by: Optional[str] = Field(None, max_length=64, description="创建者")
    create_time: Optional[datetime] = Field(None, description="创建时间")
    update_by: Optional[str] = Field(None, max_length=64, description="更新者")
    update_time: Optional[datetime] = Field(None, description="更新时间")
    del_flag: Optional[str] = Field(None, max_length=1, description='逻辑删除标识')

    def whenInsertOrUpdate(self, usrId: str) -> 'WrProblemVO' :
        if self.id is None :
            self.create_by = usrId
            self.create_time = datetime.now()
        
        self.update_by = usrId
        self.update_time = datetime.now()

        return self

@as_query
class WrProblemPageVo(WrProblemVO):
    """分页请求Vo
    """
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')