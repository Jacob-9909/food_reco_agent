"""
Database module for food recommendation agent

이 모듈은 데이터베이스 연결, 모델, 쿼리 관련 기능을 제공합니다.
"""

from .models import Base, UserSession, SearchResult, Recommendation
from .connection import get_session, get_db, test_database_connection, db_manager
from .queries import orm_query_examples
from .storage_service import (
    StorageService, 
    save_user_session, 
    save_search_results, 
    save_recommendation, 
    save_complete_session
)

__all__ = [
    # 모델
    "Base",
    "UserSession",
    "SearchResult", 
    "Recommendation",
    # 연결 관리
    "get_session",
    "get_db",
    "test_database_connection",
    "db_manager",
    # 쿼리 예제
    "orm_query_examples",
    # 저장 서비스
    "StorageService",
    "save_user_session",
    "save_search_results", 
    "save_recommendation",
    "save_complete_session"
]
