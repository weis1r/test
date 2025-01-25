from sqlalchemy import Column, Integer, String, JSON, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class TestCaseModel(Base):
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    api_url = Column(String)
    method = Column(String)
    headers = Column(JSON, default={})
    params = Column(JSON, default={})
    body = Column(JSON, nullable=True)
    expected_status = Column(Integer, default=200)
    expected_response = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

# 数据库连接配置
DATABASE_URL = "postgresql://postgres:postgres@localhost/test_platform"
engine = create_engine(DATABASE_URL)

# 创建数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建数据库表
def init_db():
    Base.metadata.create_all(bind=engine)