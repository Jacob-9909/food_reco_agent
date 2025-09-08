from typing import List, TypedDict, Dict, Any

# 상태 정의
class GraphState(TypedDict):
    age: int # 나이 
    cuisine_preference: str # 종류
    weather: str # 날씨
    location: str # 위치
    companion_type: str  # 동반자유형: 혼밥, 데이트, 가족식사, 친구모임, 회식
    ambiance: str # 분위기: 시끌벅적한, 조용한, 아늑한, 인스타감성, 전통적인
    special_requirements: str # 특별 요구사항: 주차 가능, 반려동물 동반 가능, 채식 메뉴 있음, 키즈존 있음
    search_results: List[Dict[str, str]] # 검색 결과
    recommendations: List[str] # 추천 결과
    error: str # 에러 메시지
    user_profile: Dict[str, Any] # 사용자 프로필 정보 추가
    session_id: int # 데이터베이스 세션 ID
