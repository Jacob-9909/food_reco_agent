#!/usr/bin/env python3
"""
Food Recommendation Agent 실행 스크립트

이 스크립트는 음식 추천 에이전트를 실행하는 메인 엔트리 포인트입니다.
"""

from src.core import workflow_app

def main():
    """메인 실행 함수"""
    print("🍽️  음식 추천 에이전트를 시작합니다!")
    print("=" * 60)
    
    # 초기 상태 설정
    initial_state = {
        "age": 0,
        "cuisine_preference": "",
        "weather": "",
        "location": "",
        "companion_type": "",
        "ambiance": "",
        "special_requirements": "",
        "search_results": [],
        "recommendations": [],
        "error": "",
        "user_profile": {},
        "session_id": 0
    }
    
    try:
        # LangGraph 실행
        final_results = workflow_app.invoke(initial_state)
        
        print("\n" + "="*60)
        print("🍽️  맛집 추천 결과")
        print("="*60)
        
        if final_results.get('recommendations'):
            for i, recommendation in enumerate(final_results['recommendations'], 1):
                if hasattr(recommendation, 'content'):
                    # Gemini 응답 객체인 경우 content 추출
                    content = recommendation.content
                else:
                    # 일반 문자열인 경우
                    content = str(recommendation)
                
                # 마크다운 형식 제거하고 깔끔하게 출력
                content = content.replace('**', '').replace('*', '')
                content = content.replace('## ', '\n').replace('# ', '\n')
                
                print(f"\n📋 추천 {i}:")
                print("-" * 40)
                print(content)
                print("-" * 40)
        
        if final_results.get('error'):
            print(f"\n❌ 오류: {final_results['error']}")
        
        print("\n" + "="*60)
        print("맛집 추천이 완료되었습니다! 🎉")
        print("="*60)
        
    except Exception as e:
        print(f"❌ 실행 중 오류가 발생했습니다: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
