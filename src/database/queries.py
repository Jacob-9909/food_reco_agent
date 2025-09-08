"""
SQLAlchemy ORM 쿼리 예제 모음

이 모듈은 새로운 데이터베이스 모델을 사용한 다양한 ORM 쿼리 예제들을 제공합니다.
실제 프로덕션 코드에서는 이 예제들을 참고하여 필요한 쿼리를 작성하세요.
"""

from sqlalchemy import and_, or_, func
from sqlalchemy.orm import Session

# 모듈화된 데이터베이스 관련 클래스들을 import
try:
    # 패키지 내에서 import할 때
    from .models import UserSession, SearchResult, Recommendation
    from .connection import get_session, test_database_connection
except ImportError:
    # 직접 실행할 때
    from models import UserSession, SearchResult, Recommendation
    from connection import get_session, test_database_connection

def orm_query_examples():
    """SQLAlchemy ORM을 사용한 다양한 쿼리 예제들"""
    session = get_session()
    
    try:
        print("=== SQLAlchemy ORM 쿼리 예제 ===\n")
        
        # 1. READ - 모든 사용자 세션 조회
        print("1. READ - 모든 사용자 세션 조회")
        all_sessions = session.query(UserSession).all()
        for session_data in all_sessions:
            print(f"  {session_data}")
        print()
        
        # 2. READ - 조건부 조회 (WHERE 절)
        print("2. READ - 조건부 조회")
        # 특정 지역의 세션들
        seoul_sessions = session.query(UserSession).filter(UserSession.location.like('%서울%')).all()
        print(f"서울 지역 세션들: {seoul_sessions}")
        
        # 특정 나이대의 세션들
        young_sessions = session.query(UserSession).filter(UserSession.age < 30).all()
        print(f"30세 미만 세션들: {young_sessions}")
        print()
        
        # 3. READ - 복합 조건 (AND, OR)
        print("3. READ - 복합 조건")
        # AND 조건: 서울 지역이면서 20대인 세션들
        seoul_20s = session.query(UserSession).filter(
            and_(
                UserSession.location.like('%서울%'),
                UserSession.age >= 20,
                UserSession.age < 30
            )
        ).all()
        print(f"서울 지역 20대 세션들: {seoul_20s}")
        
        # OR 조건: 한식 또는 일식을 선호하는 세션들
        korean_japanese = session.query(UserSession).filter(
            or_(
                UserSession.cuisine_preference == '한식',
                UserSession.cuisine_preference == '일식'
            )
        ).all()
        print(f"한식 또는 일식 선호 세션들: {korean_japanese}")
        print()
        
        # 4. READ - 정렬 (ORDER BY)
        print("4. READ - 정렬")
        # 나이순 정렬
        sessions_by_age = session.query(UserSession).order_by(UserSession.age.desc()).all()
        print(f"나이 내림차순 세션들: {sessions_by_age}")
        
        # 생성일시순 정렬
        sessions_by_date = session.query(UserSession).order_by(UserSession.created_at.desc()).all()
        print(f"최신 생성 세션들: {sessions_by_date}")
        print()
        
        # 5. READ - 집계 함수 (COUNT, AVG, MAX, MIN)
        print("5. READ - 집계 함수")
        # 전체 세션 수
        total_sessions = session.query(func.count(UserSession.id)).scalar()
        print(f"전체 세션 수: {total_sessions}")
        
        # 평균 나이
        avg_age = session.query(func.avg(UserSession.age)).scalar()
        print(f"평균 나이: {avg_age:.1f}세")
        
        # 최고/최저 나이
        max_age = session.query(func.max(UserSession.age)).scalar()
        min_age = session.query(func.min(UserSession.age)).scalar()
        print(f"나이 범위: {min_age}세 ~ {max_age}세")
        print()
        
        # 6. READ - 검색 결과 조회
        print("6. READ - 검색 결과 조회")
        all_search_results = session.query(SearchResult).all()
        print(f"전체 검색 결과 수: {len(all_search_results)}")
        
        # 네이버 검색 결과만 조회
        naver_results = session.query(SearchResult).filter(SearchResult.source == 'naver').all()
        print(f"네이버 검색 결과 수: {len(naver_results)}")
        print()
        
        # 7. READ - 추천 결과 조회
        print("7. READ - 추천 결과 조회")
        all_recommendations = session.query(Recommendation).all()
        print(f"전체 추천 결과 수: {len(all_recommendations)}")
        
        # Gemini 모델로 생성된 추천만 조회
        gemini_recommendations = session.query(Recommendation).filter(
            Recommendation.ai_model == 'gemini-2.0-flash'
        ).all()
        print(f"Gemini 추천 결과 수: {len(gemini_recommendations)}")
        print()
        
        # 8. READ - JOIN 쿼리 (세션과 검색 결과 연결)
        print("8. READ - JOIN 쿼리")
        # 세션과 검색 결과를 함께 조회
        sessions_with_results = session.query(UserSession, SearchResult).join(
            SearchResult, UserSession.id == SearchResult.session_id
        ).all()
        print(f"검색 결과가 있는 세션 수: {len(sessions_with_results)}")
        
        # 세션과 추천 결과를 함께 조회
        sessions_with_recommendations = session.query(UserSession, Recommendation).join(
            Recommendation, UserSession.id == Recommendation.session_id
        ).all()
        print(f"추천 결과가 있는 세션 수: {len(sessions_with_recommendations)}")
        print()
        
        # 9. READ - 그룹화 (GROUP BY)
        print("9. READ - 그룹화")
        # 지역별 세션 수
        sessions_by_location = session.query(
            UserSession.location,
            func.count(UserSession.id).label('count')
        ).group_by(UserSession.location).all()
        print("지역별 세션 수:")
        for location, count in sessions_by_location:
            print(f"  {location}: {count}개")
        
        # 음식 선호도별 세션 수
        sessions_by_cuisine = session.query(
            UserSession.cuisine_preference,
            func.count(UserSession.id).label('count')
        ).group_by(UserSession.cuisine_preference).all()
        print("음식 선호도별 세션 수:")
        for cuisine, count in sessions_by_cuisine:
            print(f"  {cuisine}: {count}개")
        print()
        
        # 10. READ - 서브쿼리
        print("10. READ - 서브쿼리")
        # 검색 결과가 있는 세션들만 조회
        sessions_with_search = session.query(UserSession).filter(
            UserSession.id.in_(
                session.query(SearchResult.session_id).distinct()
            )
        ).all()
        print(f"검색 결과가 있는 세션 수: {len(sessions_with_search)}")
        
        # 추천 결과가 있는 세션들만 조회
        sessions_with_recommendation = session.query(UserSession).filter(
            UserSession.id.in_(
                session.query(Recommendation.session_id).distinct()
            )
        ).all()
        print(f"추천 결과가 있는 세션 수: {len(sessions_with_recommendation)}")
        print()
        
        print("=== 쿼리 예제 완료 ===")
        
    except Exception as e:
        print(f"쿼리 실행 중 오류 발생: {e}")
    finally:
        session.close()

def get_user_statistics():
    """사용자 통계 정보를 조회하는 함수"""
    session = get_session()
    
    try:
        stats = {}
        
        # 전체 세션 수
        stats['total_sessions'] = session.query(func.count(UserSession.id)).scalar()
        
        # 평균 나이
        stats['avg_age'] = session.query(func.avg(UserSession.age)).scalar()
        
        # 가장 인기 있는 음식 종류
        popular_cuisine = session.query(
            UserSession.cuisine_preference,
            func.count(UserSession.id).label('count')
        ).group_by(UserSession.cuisine_preference).order_by(
            func.count(UserSession.id).desc()
        ).first()
        
        if popular_cuisine:
            stats['popular_cuisine'] = popular_cuisine[0]
            stats['popular_cuisine_count'] = popular_cuisine[1]
        
        # 가장 인기 있는 지역
        popular_location = session.query(
            UserSession.location,
            func.count(UserSession.id).label('count')
        ).group_by(UserSession.location).order_by(
            func.count(UserSession.id).desc()
        ).first()
        
        if popular_location:
            stats['popular_location'] = popular_location[0]
            stats['popular_location_count'] = popular_location[1]
        
        return stats
        
    except Exception as e:
        print(f"통계 조회 중 오류 발생: {e}")
        return {}
    finally:
        session.close()

def get_recent_activity(limit=10):
    """최근 활동을 조회하는 함수"""
    session = get_session()
    
    try:
        # 최근 세션들
        recent_sessions = session.query(UserSession).order_by(
            UserSession.created_at.desc()
        ).limit(limit).all()
        
        # 최근 검색 결과들
        recent_searches = session.query(SearchResult).order_by(
            SearchResult.created_at.desc()
        ).limit(limit).all()
        
        # 최근 추천 결과들
        recent_recommendations = session.query(Recommendation).order_by(
            Recommendation.created_at.desc()
        ).limit(limit).all()
        
        return {
            'recent_sessions': recent_sessions,
            'recent_searches': recent_searches,
            'recent_recommendations': recent_recommendations
        }
        
    except Exception as e:
        print(f"최근 활동 조회 중 오류 발생: {e}")
        return {}
    finally:
        session.close()

# 직접 실행 시 예제 실행
if __name__ == "__main__":
    print("데이터베이스 연결 테스트...")
    if test_database_connection():
        print("\n쿼리 예제 실행...")
        orm_query_examples()
        
        print("\n사용자 통계:")
        stats = get_user_statistics()
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        print("\n최근 활동:")
        recent = get_recent_activity(5)
        print(f"  최근 세션: {len(recent.get('recent_sessions', []))}개")
        print(f"  최근 검색: {len(recent.get('recent_searches', []))}개")
        print(f"  최근 추천: {len(recent.get('recent_recommendations', []))}개")
    else:
        print("데이터베이스 연결에 실패했습니다.")