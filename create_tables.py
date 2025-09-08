#!/usr/bin/env python3
"""
데이터베이스 테이블 생성 스크립트

이 스크립트는 새로운 데이터베이스 모델에 대한 테이블을 생성합니다.
"""

from src.database import Base, db_manager

def create_tables():
    """데이터베이스 테이블을 생성합니다."""
    try:
        print("데이터베이스 연결 테스트 중...")
        if not db_manager.test_connection():
            print("❌ 데이터베이스 연결에 실패했습니다.")
            return False
        
        print("✅ 데이터베이스 연결 성공!")
        print("테이블 생성 중...")
        
        # 모든 테이블 생성
        Base.metadata.create_all(bind=db_manager.engine)
        
        print("✅ 모든 테이블이 성공적으로 생성되었습니다!")
        print("\n생성된 테이블:")
        print("- food_reco.user_session (사용자 세션 정보)")
        print("- food_reco.search_result (검색 결과)")
        print("- food_reco.recommendation (추천 결과)")
        
        return True
        
    except Exception as e:
        print(f"❌ 테이블 생성 중 오류 발생: {e}")
        return False

if __name__ == "__main__":
    print("🍽️  음식 추천 에이전트 - 데이터베이스 테이블 생성")
    print("=" * 60)
    
    success = create_tables()
    
    if success:
        print("\n🎉 데이터베이스 설정이 완료되었습니다!")
        print("이제 'python run_app.py' 명령어로 앱을 실행할 수 있습니다.")
    else:
        print("\n❌ 데이터베이스 설정에 실패했습니다.")
        print("환경변수 설정을 확인해주세요.")
