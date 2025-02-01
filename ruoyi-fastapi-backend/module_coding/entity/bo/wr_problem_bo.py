from datetime import datetime
from sqlalchemy import String, Text, DateTime, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column
from config.database import Base
from sqlalchemy import text
from uuid import uuid4

class wrProblem(Base):
    """
    题目表
    """

    __tablename__ = 'wr_problem'  # 指定数据库表名

    # 使用 mapped_column 和 Mapped 来声明列
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()), comment='问题标识') 
    problem_title: Mapped[str | None] = mapped_column(String(255), nullable=True, comment='问题标题')  # 设置允许为空，并添加注释
    problem_tags: Mapped[str | None] = mapped_column(String(255), nullable=True, comment='问题标签')   # 设置允许为空，并添加注释
    problem_content: Mapped[str | None] = mapped_column(Text, nullable=True, comment='问题内容') # 设置允许为空，并添加注释
    language_type: Mapped[str | None] = mapped_column(String(50), nullable=True, comment='语言类型 (mysql、oracle)') # 设置允许为空，并添加注释
    problem_type: Mapped[str | None] = mapped_column(String(20), nullable=True, comment='问题类型（选择题、编程题、填空题、问答题）')# 设置允许为空，并添加注释
    difficulty_level: Mapped[str | None] = mapped_column(String(20), nullable=True, comment='难度层级 （难度层级）')# 设置允许为空，并添加注释
    preset_code: Mapped[str | None] = mapped_column(Text, nullable=True, comment='预设代码')# 设置允许为空，并添加注释
    test_cases_answers: Mapped[str | None] = mapped_column(Text, nullable=True, comment='测试用例\答案')# 设置允许为空，并添加注释
    enable_flag: Mapped[str | None] = mapped_column(String(1), nullable=True, default='1', comment='启用标识 （是否启用）')  # 设置允许为空，默认值1，添加注释
    create_by: Mapped[str | None] = mapped_column(String(64), nullable=True, comment='创建者') # 设置允许为空，并添加注释
    create_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, default=datetime.now(), comment='创建时间')  # 设置允许为空，默认当前时间，并添加注释
    update_by: Mapped[str | None] = mapped_column(String(64), nullable=True, comment='更新者') # 设置允许为空，并添加注释
    update_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, default=datetime.now(), comment='更新时间')# 设置允许为空，默认当前时间，并添加注释
    del_flag: Mapped[str | None] = mapped_column(String(1), nullable=True, default='0', comment='逻辑删除标识')# 设置允许为空，默认值0，并添加注释


    
