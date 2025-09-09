"""
데이터베이스 저장 서비스

이 모듈은 사용자 입력, 검색 결과, 추천 결과를 데이터베이스에 저장하는 기능을 제공합니다.
"""

import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from .models import UserSession, SearchResult, Recommendation
from .connection import get_session


class StorageService:
    """
    데이터베이스 저장을 담당하는 서비스 클래스
    """
    
    def __init__(self, session: Optional[Session] = None):
        """
        StorageService 초기화
        
        Args:
            session (Session, optional): 데이터베이스 세션. None이면 새로 생성
        """
        self.session = session
        self._should_close_session = session is None
    
    def __enter__(self):
        """컨텍스트 매니저 진입"""
        if self.session is None:
            self.session = get_session()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """컨텍스트 매니저 종료"""
        if self._should_close_session and self.session:
            try:
                if exc_type is None:
                    self.session.commit()
                else:
                    self.session.rollback()
            finally:
                self.session.close()
    
    def save_user_session(self, user_data: Dict[str, Any]) -> int:
        """
        사용자 세션 정보를 데이터베이스에 저장합니다.
        
        Args:
            user_data (Dict[str, Any]): 사용자 입력 데이터
            
        Returns:
            int: 저장된 세션 ID
            
        Raises:
            SQLAlchemyError: 데이터베이스 저장 실패 시
        """
        try:
            user_session = UserSession(
                age=user_data.get('age', 0),
                cuisine_preference=user_data.get('cuisine_preference', ''),
                weather=user_data.get('weather', ''),
                location=user_data.get('location', ''),
                companion_type=user_data.get('companion_type', ''),
                ambiance=user_data.get('ambiance', ''),
                special_requirements=user_data.get('special_requirements', ''),
                created_at=datetime.datetime.now()
            )
            
            self.session.add(user_session)
            self.session.flush()  # ID를 얻기 위해 flush
            
            return user_session.id
            
        except SQLAlchemyError as e:
            self.session.rollback()
            raise SQLAlchemyError(f"사용자 세션 저장 실패: {e}")
    
    def save_search_results(self, session_id: int, search_results: List[Dict[str, str]], source: str = "naver", cuisine_preference: str = "") -> List[int]:
        """
        검색 결과를 데이터베이스에 저장합니다.
        
        Args:
            session_id (int): 사용자 세션 ID
            search_results (List[Dict[str, str]]): 검색 결과 리스트
            source (str): 검색 소스 (기본값: "naver")
            
        Returns:
            List[int]: 저장된 검색 결과 ID 리스트
            
        Raises:
            SQLAlchemyError: 데이터베이스 저장 실패 시
        """
        try:
            result_ids = []
            
            for result in search_results:
                search_result = SearchResult(
                    session_id=session_id,
                    title=result.get('title', ''),
                    description=result.get('description', ''),
                    link=result.get('link', ''),
                    source=source,
                    cuisine_preference=cuisine_preference,
                    created_at=datetime.datetime.now()
                )
                
                self.session.add(search_result)
                self.session.flush()
                result_ids.append(search_result.id)
            
            return result_ids
            
        except SQLAlchemyError as e:
            self.session.rollback()
            raise SQLAlchemyError(f"검색 결과 저장 실패: {e}")
    
    def save_recommendation(self, session_id: int, recommendation_text: str, ai_model: str = "gemini") -> int:
        """
        추천 결과를 데이터베이스에 저장합니다.
        
        Args:
            session_id (int): 사용자 세션 ID
            recommendation_text (str): 추천 내용
            ai_model (str): 사용된 AI 모델 (기본값: "gemini")
            
        Returns:
            int: 저장된 추천 결과 ID
            
        Raises:
            SQLAlchemyError: 데이터베이스 저장 실패 시
        """
        try:
            recommendation = Recommendation(
                session_id=session_id,
                recommendation_text=recommendation_text,
                ai_model=ai_model,
                created_at=datetime.datetime.now()
            )
            
            self.session.add(recommendation)
            self.session.flush()
            
            return recommendation.id
            
        except SQLAlchemyError as e:
            self.session.rollback()
            raise SQLAlchemyError(f"추천 결과 저장 실패: {e}")
    
    def save_complete_session(self, user_data: Dict[str, Any], search_results: List[Dict[str, str]], 
                            recommendations: List[str], source: str = "naver", ai_model: str = "gemini") -> Dict[str, int]:
        """
        전체 세션 데이터를 한 번에 저장합니다.
        
        Args:
            user_data (Dict[str, Any]): 사용자 입력 데이터
            search_results (List[Dict[str, str]]): 검색 결과 리스트
            recommendations (List[str]): 추천 결과 리스트
            source (str): 검색 소스 (기본값: "naver")
            ai_model (str): 사용된 AI 모델 (기본값: "gemini")
            
        Returns:
            Dict[str, int]: 저장된 데이터의 ID들
            
        Raises:
            SQLAlchemyError: 데이터베이스 저장 실패 시
        """
        try:
            # 1. 사용자 세션 저장
            session_id = self.save_user_session(user_data)
            
            # 2. 검색 결과 저장
            search_result_ids = self.save_search_results(session_id, search_results, source)
            
            # 3. 추천 결과 저장
            recommendation_ids = []
            for recommendation_text in recommendations:
                # Gemini 응답 객체인 경우 content 추출
                if hasattr(recommendation_text, 'content'):
                    text = recommendation_text.content
                else:
                    text = str(recommendation_text)
                
                rec_id = self.save_recommendation(session_id, text, ai_model)
                recommendation_ids.append(rec_id)
            
            return {
                'session_id': session_id,
                'search_result_ids': search_result_ids,
                'recommendation_ids': recommendation_ids
            }
            
        except SQLAlchemyError as e:
            self.session.rollback()
            raise SQLAlchemyError(f"전체 세션 저장 실패: {e}")


# 편의를 위한 함수들
def save_user_session(user_data: Dict[str, Any]) -> int:
    """
    사용자 세션을 저장하는 편의 함수
    
    Args:
        user_data (Dict[str, Any]): 사용자 입력 데이터
        
    Returns:
        int: 저장된 세션 ID
    """
    with StorageService() as storage:
        return storage.save_user_session(user_data)


def save_search_results(session_id: int, search_results: List[Dict[str, str]], source: str = "naver", cuisine_preference: str = "") -> List[int]:
    """
    검색 결과를 저장하는 편의 함수
    
    Args:
        session_id (int): 사용자 세션 ID
        search_results (List[Dict[str, str]]): 검색 결과 리스트
        source (str): 검색 소스
        cuisine_preference (str): 선호 음식 종류

    Returns:
        List[int]: 저장된 검색 결과 ID 리스트
    """
    with StorageService() as storage:
        return storage.save_search_results(session_id, search_results, source, cuisine_preference)


def save_recommendation(session_id: int, recommendation_text: str, ai_model: str = "gemini") -> int:
    """
    추천 결과를 저장하는 편의 함수
    
    Args:
        session_id (int): 사용자 세션 ID
        recommendation_text (str): 추천 내용
        ai_model (str): 사용된 AI 모델
        
    Returns:
        int: 저장된 추천 결과 ID
    """
    with StorageService() as storage:
        return storage.save_recommendation(session_id, recommendation_text, ai_model)


def save_complete_session(user_data: Dict[str, Any], search_results: List[Dict[str, str]], 
                         recommendations: List[str], source: str = "naver", ai_model: str = "gemini") -> Dict[str, int]:
    """
    전체 세션 데이터를 저장하는 편의 함수
    
    Args:
        user_data (Dict[str, Any]): 사용자 입력 데이터
        search_results (List[Dict[str, str]]): 검색 결과 리스트
        recommendations (List[str]): 추천 결과 리스트
        source (str): 검색 소스
        ai_model (str): 사용된 AI 모델
        
    Returns:
        Dict[str, int]: 저장된 데이터의 ID들
    """
    with StorageService() as storage:
        return storage.save_complete_session(user_data, search_results, recommendations, source, ai_model)
