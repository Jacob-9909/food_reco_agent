"""
데이터베이스 연결 및 세션 관리

이 모듈은 PostgreSQL 데이터베이스 연결을 설정하고 세션을 관리합니다.
환경변수를 통해 데이터베이스 연결 정보를 가져옵니다.
"""

import os
from typing import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()


class DatabaseManager:
    """
    데이터베이스 연결 및 세션을 관리하는 클래스
    """
    
    def __init__(self):
        """데이터베이스 연결 정보를 환경변수에서 가져와 초기화합니다."""
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.host = os.getenv('DB_HOST')
        self.port = os.getenv('DB_PORT')
        self.database = os.getenv('DB_DATABASE')
        
        # 데이터베이스 연결 URL 생성
        self.database_url = (
            f'postgresql+psycopg2://{self.user}:{self.password}'
            f'@{self.host}:{self.port}/{self.database}'
        )
        
        # 엔진 및 세션 팩토리 생성
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    def get_session(self) -> Session:
        """
        새로운 데이터베이스 세션을 생성합니다.
        
        Returns:
            Session: SQLAlchemy 세션 객체
        """
        return self.SessionLocal()
    
    def get_session_generator(self) -> Generator[Session, None, None]:
        """
        컨텍스트 매니저로 사용할 수 있는 세션 제너레이터를 반환합니다.
        
        Yields:
            Session: SQLAlchemy 세션 객체
        """
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()
    
    def test_connection(self) -> bool:
        """
        데이터베이스 연결을 테스트합니다.
        
        Returns:
            bool: 연결 성공 여부
        """
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                print("데이터베이스 연결 성공")
                return True
        except Exception as e:
            print(f"데이터베이스 연결 실패: {e}")
            return False


# 전역 데이터베이스 매니저 인스턴스
db_manager = DatabaseManager()

# 편의를 위한 함수들
def get_db() -> Generator[Session, None, None]:
    """
    FastAPI 등에서 의존성 주입으로 사용할 수 있는 세션 제너레이터
    
    Yields:
        Session: SQLAlchemy 세션 객체
    """
    yield from db_manager.get_session_generator()


def get_session() -> Session:
    """
    직접 세션을 가져오는 함수
    
    Returns:
        Session: SQLAlchemy 세션 객체
    """
    return db_manager.get_session()


def test_database_connection() -> bool:
    """
    데이터베이스 연결을 테스트하는 함수
    
    Returns:
        bool: 연결 성공 여부
    """
    return db_manager.test_connection()


# 기존 코드와의 호환성을 위한 전역 변수들
engine = db_manager.engine
Session = db_manager.SessionLocal
