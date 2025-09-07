"""
데이터베이스 모델 정의

이 모듈은 SQLAlchemy ORM을 사용하여 데이터베이스 테이블을 Python 클래스로 정의합니다.
각 클래스는 해당하는 데이터베이스 테이블과 매핑됩니다.
"""

from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import declarative_base

# 모든 모델 클래스의 기본 클래스
Base = declarative_base()


class Store(Base):
    """
    음식점 매장 정보를 저장하는 테이블
    
    Attributes:
        id (int): 매장 고유 ID (Primary Key)
        name (str): 매장명
        region_id (int): 지역 ID (Foreign Key)
        min_price (int): 최소 가격
        max_price (int): 최대 가격
        opening_hours (str): 영업시간
        rating (float): 평점
        created_at (datetime): 생성일시
    """
    __tablename__ = 'food_store'
    __table_args__ = {'schema': 'food_reco'}
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    region_id = Column(Integer)
    min_price = Column(Integer)
    max_price = Column(Integer)
    opening_hours = Column(String)
    rating = Column(Float)
    created_at = Column(DateTime)

    def __repr__(self) -> str:
        """객체의 문자열 표현을 반환합니다."""
        return (f"<Store(id={self.id}, name={self.name}, region_id={self.region_id}, "
                f"min_price={self.min_price}, max_price={self.max_price}, rating={self.rating})>")


class Region(Base):
    """
    지역 정보를 저장하는 테이블 (실제 테이블명: mood)
    
    Attributes:
        id (int): 지역 고유 ID (Primary Key)
        si (str): 시/도
        gun (str): 군
        gu (str): 구
    """
    __tablename__ = 'mood'
    __table_args__ = {'schema': 'food_reco'}
    
    id = Column(Integer, primary_key=True)
    si = Column(String)
    gun = Column(String)
    gu = Column(String)

    def __repr__(self) -> str:
        """객체의 문자열 표현을 반환합니다."""
        return f"<Region(id={self.id}, si={self.si}, gun={self.gun}, gu={self.gu})>"


class Mood(Base):
    """
    기분/분위기 정보를 저장하는 테이블 (실제 테이블명: region)
    
    Attributes:
        id (int): 기분 고유 ID (Primary Key)
        name (str): 기분/분위기 이름
    """
    __tablename__ = 'region'
    __table_args__ = {'schema': 'food_reco'}
    
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self) -> str:
        """객체의 문자열 표현을 반환합니다."""
        return f"<Mood(id={self.id}, name={self.name})>"
