"""
Streamlit 웹 인터페이스

사용자 친화적인 웹 UI를 제공하는 Streamlit 애플리케이션입니다.
"""

import streamlit as st
import requests
import json
from datetime import datetime
from typing import Dict, Any, List
import time

# 페이지 설정
st.set_page_config(
    page_title="🍽️ 음식 추천 에이전트",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API 서버 URL (로컬 개발용)
API_BASE_URL = "http://localhost:8000"

def check_api_health() -> bool:
    """API 서버 상태 확인"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_recommendations(user_input: Dict[str, Any]) -> Dict[str, Any]:
    """API를 통해 추천 결과 가져오기"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/recommend",
            json=user_input,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API 요청 실패: {e}")
        return None

def main():
    """메인 애플리케이션"""
    
    # 헤더
    st.title("🍽️ 음식 추천 에이전트")
    st.markdown("---")
    
    # API 서버 상태 확인
    if not check_api_health():
        st.error("⚠️ API 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요.")
        st.info("터미널에서 다음 명령어로 API 서버를 시작하세요: `python -m src.api.main`")
        return
    
    st.success("✅ API 서버 연결 성공!")
    
    # 사이드바 - 사용자 입력 폼
    with st.sidebar:
        st.header("📝 사용자 정보 입력")
        
        # 나이 입력
        age = st.number_input(
            "나이",
            min_value=1,
            max_value=120,
            value=25,
            help="나이를 입력하세요"
        )
        
        # 선호 음식 종류
        cuisine_options = ["한식", "중식", "일식", "양식", "분식", "치킨", "피자", "카페", "기타"]
        cuisine_preference = st.selectbox(
            "선호 음식 종류",
            cuisine_options,
            help="선호하는 음식 종류를 선택하세요"
        )
        
        # 날씨
        weather_options = ["맑음", "흐림", "비", "눈", "더움", "추움"]
        weather = st.selectbox(
            "현재 날씨",
            weather_options,
            help="현재 날씨 상태를 선택하세요"
        )
        
        # 지역
        location = st.text_input(
            "지역",
            value="강남",
            help="검색하고 싶은 지역을 입력하세요 (예: 강남, 홍대, 부산)"
        )
        
        # 동반자 유형
        companion_options = ["혼밥", "데이트", "가족식사", "친구모임", "회식", "비즈니스"]
        companion_type = st.selectbox(
            "동반자 유형",
            companion_options,
            help="식사 동반자 유형을 선택하세요"
        )
        
        # 분위기
        ambiance_options = ["시끌벅적한", "조용한", "아늑한", "인스타감성", "전통적인", "모던한"]
        ambiance = st.selectbox(
            "원하는 분위기",
            ambiance_options,
            help="원하는 맛집 분위기를 선택하세요"
        )
        
        # 특별 요구사항
        special_requirements = st.text_area(
            "특별 요구사항",
            placeholder="예: 주차 가능, 반려동물 동반 가능, 채식 메뉴 있음, 키즈존 있음",
            help="특별한 요구사항이 있다면 입력하세요"
        )
        
        # 추천 요청 버튼
        if st.button("🍽️ 맛집 추천 받기", type="primary", use_container_width=True):
            # 입력 데이터 검증
            if not location.strip():
                st.error("지역을 입력해주세요.")
                return
            
            # 사용자 입력 데이터 구성
            user_input = {
                "age": age,
                "cuisine_preference": cuisine_preference,
                "weather": weather,
                "location": location.strip(),
                "companion_type": companion_type,
                "ambiance": ambiance,
                "special_requirements": special_requirements.strip() if special_requirements else None
            }
            
            # 세션 상태에 저장
            st.session_state.user_input = user_input
            st.session_state.recommendation_requested = True
    
    # 메인 영역
    if st.session_state.get('recommendation_requested', False):
        user_input = st.session_state.get('user_input', {})
        
        # 로딩 표시
        with st.spinner("맛집을 검색하고 추천을 생성하는 중입니다..."):
            # API 호출
            result = get_recommendations(user_input)
        
        if result:
            # 결과 표시
            st.header("🎯 추천 결과")
            
            # 사용자 프로필 정보
            with st.expander("👤 사용자 프로필 정보", expanded=False):
                user_profile = result.get('user_profile', {})
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("나이대", user_profile.get('age_group', 'N/A'))
                    st.metric("계절", user_profile.get('season', 'N/A'))
                
                with col2:
                    st.metric("날씨", user_profile.get('weather_condition', 'N/A'))
                    st.metric("선호 음식", user_profile.get('preferred_cuisine', 'N/A'))
                
                with col3:
                    st.metric("동반자 유형", user_profile.get('companion_type', 'N/A'))
                    st.metric("분위기", user_profile.get('preferred_ambiance', 'N/A'))
            
            # 검색 결과
            search_results = result.get('search_results', [])
            if search_results:
                st.subheader("🔍 검색된 맛집 목록")
                for i, restaurant in enumerate(search_results, 1):
                    with st.expander(f"{i}. {restaurant.get('title', '제목 없음')}", expanded=False):
                        st.write(f"**설명:** {restaurant.get('description', '설명 없음')}")
                        if restaurant.get('link'):
                            st.write(f"**링크:** {restaurant['link']}")
            
            # AI 추천 결과
            recommendations = result.get('recommendations', [])
            if recommendations:
                st.subheader("🤖 AI 개인화 추천")
                
                for i, recommendation in enumerate(recommendations, 1):
                    st.markdown(f"### 추천 {i}")
                    
                    # 마크다운 형식으로 표시
                    st.markdown(recommendation)
                    st.markdown("---")
            
            # 세션 정보
            st.info(f"📊 세션 ID: {result.get('session_id', 'N/A')} | 생성 시간: {result.get('created_at', 'N/A')}")
            
            # 새 추천 요청 버튼
            if st.button("🔄 새로운 추천 받기", use_container_width=True):
                st.session_state.recommendation_requested = False
                st.rerun()
        
        else:
            st.error("추천 생성에 실패했습니다. 다시 시도해주세요.")
    
    else:
        # 초기 화면
        st.markdown("""
        ## 🎯 개인화된 맛집 추천 서비스
        
        왼쪽 사이드바에서 정보를 입력하고 **"맛집 추천 받기"** 버튼을 클릭하세요!
        
        ### ✨ 주요 기능
        - **나이대별 선호도 분석**: 나이에 따른 음식 선호도 패턴 분석
        - **날씨별 추천**: 현재 날씨에 맞는 음식 추천
        - **동반자별 맞춤**: 혼밥, 데이트, 가족식사 등 상황별 추천
        - **AI 개인화**: Google Gemini를 활용한 맞춤형 추천
        - **실시간 검색**: 네이버 API를 통한 최신 맛집 정보
        
        ### 📱 사용 방법
        1. 왼쪽 사이드바에서 정보를 입력하세요
        2. "맛집 추천 받기" 버튼을 클릭하세요
        3. AI가 분석한 개인화된 추천을 확인하세요
        """)
        
        # 통계 정보 (예시)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("총 추천 수", "1,234", "12")
        
        with col2:
            st.metric("활성 사용자", "567", "8")
        
        with col3:
            st.metric("평균 만족도", "4.8/5.0", "0.2")
        
        with col4:
            st.metric("지원 지역", "전국", "서울")

if __name__ == "__main__":
    main()
