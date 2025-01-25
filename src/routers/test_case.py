from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database.models import SessionLocal, TestCaseModel
from ..models.test_case import TestCase, TestCaseCreate, TestCaseUpdate
from ..engine.test_executor import TestExecutor

router = APIRouter(prefix="/api/test-cases", tags=["test-cases"])

# 依赖项：获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=TestCase)
async def create_test_case(test_case: TestCaseCreate, db: Session = Depends(get_db)):
    db_test_case = TestCaseModel(**test_case.dict())
    db.add(db_test_case)
    db.commit()
    db.refresh(db_test_case)
    return db_test_case

@router.get("/", response_model=List[TestCase])
async def list_test_cases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    test_cases = db.query(TestCaseModel).offset(skip).limit(limit).all()
    return test_cases

@router.get("/{test_case_id}", response_model=TestCase)
async def get_test_case(test_case_id: int, db: Session = Depends(get_db)):
    test_case = db.query(TestCaseModel).filter(TestCaseModel.id == test_case_id).first()
    if test_case is None:
        raise HTTPException(status_code=404, detail="测试用例不存在")
    return test_case

@router.put("/{test_case_id}", response_model=TestCase)
async def update_test_case(test_case_id: int, test_case: TestCaseUpdate, db: Session = Depends(get_db)):
    db_test_case = db.query(TestCaseModel).filter(TestCaseModel.id == test_case_id).first()
    if db_test_case is None:
        raise HTTPException(status_code=404, detail="测试用例不存在")
    
    update_data = test_case.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_test_case, key, value)
    
    db.commit()
    db.refresh(db_test_case)
    return db_test_case

@router.delete("/{test_case_id}")
async def delete_test_case(test_case_id: int, db: Session = Depends(get_db)):
    db_test_case = db.query(TestCaseModel).filter(TestCaseModel.id == test_case_id).first()
    if db_test_case is None:
        raise HTTPException(status_code=404, detail="测试用例不存在")
    
    db.delete(db_test_case)
    db.commit()
    return {"message": "测试用例已删除"}

@router.post("/{test_case_id}/execute")
async def execute_test_case(test_case_id: int, db: Session = Depends(get_db)):
    db_test_case = db.query(TestCaseModel).filter(TestCaseModel.id == test_case_id).first()
    if db_test_case is None:
        raise HTTPException(status_code=404, detail="测试用例不存在")
    
    test_case = TestCase.from_orm(db_test_case)
    result = await TestExecutor.execute_test(test_case)
    return result.to_dict()