from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TestCase(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    api_url: str
    method: str
    headers: dict = {}
    params: dict = {}
    body: Optional[dict] = None
    expected_status: int = 200
    expected_response: Optional[dict] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class TestCaseCreate(BaseModel):
    name: str
    description: str
    api_url: str
    method: str
    headers: dict = {}
    params: dict = {}
    body: Optional[dict] = None
    expected_status: int = 200
    expected_response: Optional[dict] = None

class TestCaseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    api_url: Optional[str] = None
    method: Optional[str] = None
    headers: Optional[dict] = None
    params: Optional[dict] = None
    body: Optional[dict] = None
    expected_status: Optional[int] = None
    expected_response: Optional[dict] = None