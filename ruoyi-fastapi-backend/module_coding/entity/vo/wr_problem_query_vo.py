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

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        extra='allow'  # 允许额外的字段
    )


    id: Optional[str] = Field(None, description="问题标识")
    problem_title: Optional[str] = Field(alias="problemTitle", min_length=1, max_length=255, description="问题标题")
    problem_tags: Optional[str] = Field(alias="problemTags", max_length=255, description="问题标签")
    problem_content: Optional[bytes | str] = Field(alias="problemContent", description="问题内容")
    language_type: Optional[str] = Field(alias="languageType", max_length=50, description="语言类型")
    problem_type: Optional[str] = Field(alias="problemType", max_length=20, description="问题类型")
    difficulty_level: Optional[str] = Field(alias="difficultyLevel", max_length=20, description="难度层级")
    preset_code: Optional[str] = Field(alias="presetCode", description="预设代码")
    test_cases_answers: Optional[str] = Field(alias="testCasesAnswers", description="测试用例\\答案")
    enable_flag: Optional[str | int] = Field(alias="enableFlag", description='启用标识')
    create_by: Optional[str] = Field(alias="createBy", default=None, max_length=64, description="创建者")
    create_time: Optional[datetime] = Field(alias="createTime", default=None, description="创建时间")
    update_by: Optional[str] = Field(alias="updateBy", default=None, max_length=64, description="更新者")
    update_time: Optional[datetime] = Field(alias="updateTime", default=None, description="更新时间")
    del_flag: Optional[str | int] = Field(alias="delFlag", default=None, description='逻辑删除标识')

    def whenInsertOrUpdate(self, usrId: str) -> 'WrProblemVO' :
        if self.id is None :
            self.create_by = usrId
            self.create_time = datetime.now()
        
        self.update_by = usrId
        self.update_time = datetime.now()
        
        # 确保 enable_flag 是字符串类型
        if self.enable_flag is not None:
            self.enable_flag = str(self.enable_flag)

        return self

@as_query
class WrProblemPageVo(BaseModel):
    """分页查询参数Vo
    """
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )

    # 分页参数
    page_num: int = Field(alias="pageNum", default=1, description='当前页码')
    page_size: int = Field(alias="pageSize", default=10, description='每页记录数')
    
    # 查询条件，全部设为可选
    problem_title: Optional[str] = Field(alias="problemTitle", default=None, description="问题标题")
    problem_tags: Optional[str] = Field(alias="problemTags", default=None, description="问题标签")
    language_type: Optional[str] = Field(alias="languageType", default=None, description="语言类型")
    problem_type: Optional[str] = Field(alias="problemType", default=None, description="问题类型")
    difficulty_level: Optional[str] = Field(alias="difficultyLevel", default=None, description="难度层级")
    enable_flag: Optional[str | int] = Field(alias="enableFlag", default=None, description="启用标识")
