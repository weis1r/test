import requests
from typing import Dict, Optional
from datetime import datetime
from ..models.test_case import TestCase

class TestResult:
    def __init__(self, test_case: TestCase):
        self.test_case = test_case
        self.start_time = datetime.now()
        self.end_time: Optional[datetime] = None
        self.status: str = "pending"
        self.actual_status: Optional[int] = None
        self.actual_response: Optional[dict] = None
        self.error_message: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "test_case_id": self.test_case.id,
            "test_case_name": self.test_case.name,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "status": self.status,
            "actual_status": self.actual_status,
            "actual_response": self.actual_response,
            "error_message": self.error_message
        }

class TestExecutor:
    @staticmethod
    async def execute_test(test_case: TestCase) -> TestResult:
        result = TestResult(test_case)
        
        try:
            response = requests.request(
                method=test_case.method,
                url=test_case.api_url,
                headers=test_case.headers,
                params=test_case.params,
                json=test_case.body if test_case.body else None
            )
            
            result.actual_status = response.status_code
            try:
                result.actual_response = response.json()
            except:
                result.actual_response = {"raw_content": response.text}
            
            # 验证状态码
            status_match = test_case.expected_status == response.status_code
            
            # 验证响应内容
            response_match = True
            if test_case.expected_response:
                response_match = TestExecutor._verify_response(
                    test_case.expected_response,
                    result.actual_response
                )
            
            result.status = "success" if status_match and response_match else "failed"
            
        except Exception as e:
            result.status = "error"
            result.error_message = str(e)
        
        result.end_time = datetime.now()
        return result

    @staticmethod
    def _verify_response(expected: dict, actual: dict) -> bool:
        """递归验证响应内容是否匹配预期"""
        if not isinstance(expected, dict) or not isinstance(actual, dict):
            return expected == actual
            
        for key, value in expected.items():
            if key not in actual:
                return False
            if isinstance(value, dict):
                if not TestExecutor._verify_response(value, actual[key]):
                    return False
            elif value != actual[key]:
                return False
        return True