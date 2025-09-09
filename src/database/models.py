"""
데이터베이스 모델 정의

이 모듈은 SQLAlchemy ORM을 사용하여 데이터베이스 테이블을 Python 클래스로 정의합니다.
각 클래스는 해당하는 데이터베이스 테이블과 매핑됩니다.
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Text, JSON
from sqlalchemy.orm import declarative_base

# 모든 모델 클래스의 기본 클래스
Base = declarative_base()


# 기존 테이블 모델들은 제거됨
# Store, Region, Mood, FoodStoreMood 모델 삭제


class UserSession(Base):
    """
    사용자 세션 정보를 저장하는 테이블
    
    Attributes:
        id (int): 세션 고유 ID (Primary Key)
        age (int): 사용자 나이
        cuisine_preference (str): 선호 음식 종류
        weather (str): 날씨 정보
        location (str): 지역 정보
        companion_type (str): 동반자 유형
        ambiance (str): 원하는 분위기
        special_requirements (str): 특별 요구사항
        created_at (datetime): 생성일시
    """
    __tablename__ = 'user_session'
    __table_args__ = {'schema': 'food_reco'}
    
    id = Column(Integer, primary_key=True)
    age = Column(Integer)
    cuisine_preference = Column(String)
    weather = Column(String)
    location = Column(String)
    companion_type = Column(String)
    ambiance = Column(String)
    special_requirements = Column(Text)
    created_at = Column(DateTime)

    def __repr__(self) -> str:
        """객체의 문자열 표현을 반환합니다."""
        return (f"<UserSession(id={self.id}, age={self.age}, location={self.location}, "
                f"cuisine_preference={self.cuisine_preference}, created_at={self.created_at})>")


class SearchResult(Base):
    """
    검색 결과를 저장하는 테이블
    
    Attributes:
        id (int): 검색 결과 고유 ID (Primary Key)
        session_id (int): 사용자 세션 ID (Foreign Key)
        title (str): 검색 결과 제목
        description (str): 검색 결과 설명
        link (str): 검색 결과 링크
        source (str): 검색 소스 (naver, backup 등)
        created_at (datetime): 생성일시
    """
    __tablename__ = 'search_result'
    __table_args__ = {'schema': 'food_reco'}
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer)
    title = Column(String)
    description = Column(Text)
    link = Column(String)
    source = Column(String)
    cuisine_preference = Column(String)
    created_at = Column(DateTime)

    def __repr__(self) -> str:
        """객체의 문자열 표현을 반환합니다."""
        return (f"<SearchResult(id={self.id}, session_id={self.session_id}, "
                f"title={self.title}, source={self.source}, cuisine_preference={self.cuisine_preference})>")


class Recommendation(Base):
    """
    추천 결과를 저장하는 테이블
    
    Attributes:
        id (int): 추천 결과 고유 ID (Primary Key)
        session_id (int): 사용자 세션 ID (Foreign Key)
        recommendation_text (str): 추천 내용
        ai_model (str): 사용된 AI 모델
        created_at (datetime): 생성일시
    """
    __tablename__ = 'recommendation'
    __table_args__ = {'schema': 'food_reco'}
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer)
    recommendation_text = Column(Text)
    ai_model = Column(String)
    created_at = Column(DateTime)

    def __repr__(self) -> str:
        """객체의 문자열 표현을 반환합니다."""
        return (f"<Recommendation(id={self.id}, session_id={self.session_id}, "
                f"ai_model={self.ai_model}, created_at={self.created_at})>")
