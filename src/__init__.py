"""
Food Recommendation Agent Package

이 패키지는 음식 추천 에이전트의 핵심 기능들을 제공합니다.
"""

# 데이터베이스 관련
from .database import Base, UserSession, SearchResult, Recommendation, get_session, get_db, test_database_connection, db_manager

# 핵심 워크플로우
from .core import GraphState, workflow_app

# 서비스
from .services import search_web, search_restaurants_naver, NaverAPIError, restaurant_data, search_restaurants_backup

__version__ = "0.1.0"
__author__ = "SolidRusT Networks"

__all__ = [
    # 데이터베이스
    "Base",
    "UserSession",
    "SearchResult", 
    "Recommendation",
    "get_session",
    "get_db",
    "test_database_connection",
    "db_manager",
    # 핵심 워크플로우
    "GraphState",
    "workflow_app",
    # 서비스
    "search_web",
    "search_restaurants_naver",
    "NaverAPIError",
    "restaurant_data",
    "search_restaurants_backup"
]
