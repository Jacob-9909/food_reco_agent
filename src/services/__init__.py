"""
Services module for food recommendation agent

이 모듈은 외부 API 서비스 및 데이터 소스를 제공합니다.
"""

from .naver_search import search_web, search_restaurants_naver, NaverAPIError
from .restaurant_data import restaurant_data, search_restaurants_backup

__all__ = [
    "search_web",
    "search_restaurants_naver", 
    "NaverAPIError",
    "restaurant_data",
    "search_restaurants_backup"
]
