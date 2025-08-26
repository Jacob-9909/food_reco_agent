# 표준 라이브러리
import datetime
from typing import List, Dict, Any

# 서드파티 라이브러리
from langchain_google_genai import ChatGoogleGenerativeAI

# 로컬 애플리케이션
from naver_search import search_restaurants as naver_search
from restaurant_data import search_restaurants as backup_search

# 타입 정의
from custom_types import GraphState

# 사용자 입력 받기
def get_user_input(state: GraphState) -> GraphState:
    """사용자로부터 입력을 받는 노드"""
    print("---사용자 입력 받기---")
    try:
        state['age'] = int(input("나이를 입력하세요: "))
        state['cuisine_preference'] = input("선호하는 음식 종류를 입력하세요: ")
        state['weather'] = input("현재 날씨를 입력하세요: ")
        state['location'] = input("지역을 입력하세요: ")
        
        # 동반자유형 입력
        print("\n동반자유형을 입력하세요:")
        print("예시: 혼밥, 데이트, 가족식사, 친구모임, 회식")
        state['companion_type'] = input("동반자유형: ").strip()
        
        # 분위기 입력
        print("\n원하는 분위기를 입력하세요:")
        print("예시: 시끌벅적한, 조용한, 아늑한, 인스타감성, 전통적인")
        state['ambiance'] = input("분위기: ").strip()
        
        # 특별 요구사항 입력
        print("\n특별 요구사항을 입력하세요 (여러 개 입력 가능, 쉼표로 구분):")
        print("예시: 주차 가능, 반려동물 동반 가능, 채식 메뉴 있음, 키즈존 있음")
        print("특별 요구사항이 없으면 '없음' 또는 빈 값으로 입력하세요")
        state['special_requirements'] = input("특별 요구사항: ").strip()
        
        print(f"\n입력 완료:")
        print(f"나이={state['age']}, 선호음식={state['cuisine_preference']}, 날씨={state['weather']}, 지역={state['location']}")
        print(f"동반자유형={state['companion_type']}, 분위기={state['ambiance']}, 특별요구사항={state['special_requirements']}")
        
    except Exception as e:
        print(f"입력 중 오류 발생: {e}")
        state['error'] = f"입력 중 오류가 발생했습니다: {e}"
    return state

# 사용자 선호도 분석
def analyze_user_preferences(state: GraphState) -> GraphState:
    """사용자 선호도를 분석하고 프로필을 생성하는 노드"""
    print("---사용자 선호도 분석---")
    try:
        age = state['age']
        cuisine = state['cuisine_preference']
        weather = state['weather']
        companion_type = state['companion_type']
        ambiance = state['ambiance']
        special_requirements = state['special_requirements']
        
        # 나이대별 선호도 패턴 분석
        age_group = ""
        if age < 20:
            age_group = "10대"
        elif age < 30:
            age_group = "20대"
        elif age < 40:
            age_group = "30대"
        elif age < 50:
            age_group = "40대"
        elif age < 60:
            age_group = "50대"
        else:
            age_group = "60대 이상"
        
        # 날씨별 음식 선호도 분석
        weather_preferences = {
            "맑음": ["BBQ", "피자", "치킨", "샐러드", "아이스크림", "카페"],
            "흐림": ["국수", "스튜", "핫팟", "커피", "따뜻한 음식"],
            "비": ["국수", "스튜", "핫팟", "따뜻한 국", "커피", "따뜻한 음식"],
            "눈": ["핫팟", "스튜", "따뜻한 국", "따뜻한 음료", "커피"],
            "더움": ["냉면", "샐러드", "아이스크림", "콜드브루", "빙수", "냉국"],
            "추움": ["핫팟", "스튜", "따뜻한 국", "따뜻한 음료", "커피", "따뜻한 음식"]
        }
        
        # 계절별 추천 로직
        current_month = datetime.datetime.now().month
        season = ""
        if current_month in [3, 4, 5]:
            season = "봄"
        elif current_month in [6, 7, 8]:
            season = "여름"
        elif current_month in [9, 10, 11]:
            season = "가을"
        else:
            season = "겨울"
        
        # 나이대별 일반적인 선호도
        age_preferences = {
            "10대": ["피자", "햄버거", "치킨", "아이스크림", "떡볶이"],
            "20대": ["카페", "분식", "치킨", "피자", "샐러드"],
            "30대": ["한식", "양식", "카페", "치킨", "피자"],
            "40대": ["한식", "양식", "중식", "일식", "카페"],
            "50대": ["한식", "중식", "일식", "양식", "전통음식"],
            "60대 이상": ["한식", "전통음식", "중식", "일식", "건강식"]
        }
        
        # 사용자 프로필 생성
        user_profile = {
            "location": state['location'],
            "age_group": age_group,
            "season": season,
            "weather_condition": weather,
            "preferred_cuisine": cuisine,
            "companion_type": companion_type,
            "preferred_ambiance": ambiance,
            "special_requirements": special_requirements,
            "age_based_preferences": age_preferences.get(age_group, []),
            "weather_based_preferences": weather_preferences.get(weather, []),
        }
        
        state['user_profile'] = user_profile
        print(f"사용자 프로필 생성 완료: {age_group}, {season} 계절, {weather} 날씨")
        print(f"동반자유형: {companion_type}, 분위기: {ambiance}")
        print(f"특별요구사항: {special_requirements}")
        print(f"나이대별 선호도: {user_profile['age_based_preferences']}")
        print(f"날씨별 선호도: {user_profile['weather_based_preferences']}")
        
    except Exception as e:
        print(f"선호도 분석 중 오류 발생: {e}")
        state['error'] = f"선호도 분석 중 오류가 발생했습니다: {e}"
    
    return state

# 맛집 검색
def search_restaurants(state: GraphState) -> GraphState:
    """네이버 또는 정적 데이터를 사용하여 맛집을 검색하고 search_results에 저장합니다."""
    print("---맛집 검색 중---")
    try:
        if not state.get('user_profile'):
            raise ValueError("사용자 프로필 정보가 누락되었습니다.")

        print("네이버 API로 맛집 검색 시도 중...")
        results = naver_search(
            user_profile=state['user_profile']
        )
        state['search_results'] = results
    except ValueError as ve:
        print(f"입력값 오류: {ve}")
        state['search_results'] = []
        state['error'] = str(ve)
    except Exception as e:
        print(f"검색 중 오류 발생: {e}")
        state['search_results'] = []
        state['error'] = f"맛집 검색 중 오류가 발생했습니다: {e}"
    return state

# 맛집 추천
def recommend_restaurants(state: GraphState) -> GraphState:
    """검색된 맛집을 바탕으로 최종 추천"""
    print("---맛집 추천---")
    if state['error']:
        print(f"오류로 인해 추천을 진행할 수 없습니다: {state['error']}")
        return state

    if not state.get('search_results'):
        print("추천할 맛집이 없습니다.")
        state['recommendations'] = ["추천할 맛집을 찾지 못했습니다."]
        return state

    # 검색 결과를 바탕으로 프롬프트 생성
    formatted_recommendations = []
    for i, result in enumerate(state['search_results'], 1):
        title = result.get('title', '제목 없음')
        description = result.get('description', '')
        # 링크 정보는 LLM에 직접 제공하기보다, 최종 결과물에 포함하는 것이 더 유용할 수 있습니다.
        formatted_rec = f"{i}. {title} - {description[:300]}{'...' if len(description) > 300 else ''}"
        formatted_recommendations.append(formatted_rec)
        
    try:
        print("Gemini를 사용하여 맛집 추천을 개인화합니다...")
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)
        
        # 사용자 프로필 정보를 포함한 향상된 프롬프트
        user_profile = state.get('user_profile', {})
        profile_info = ""
        if user_profile:
            profile_info = f"""
사용자 프로필 분석 결과:
- 나이대: {user_profile.get('age_group', 'N/A')}
- 계절: {user_profile.get('season', 'N/A')}
- 날씨: {user_profile.get('weather_condition', 'N/A')}
- 나이대별 선호도: {', '.join(user_profile.get('age_based_preferences', []))}
- 날씨별 선호도: {', '.join(user_profile.get('weather_based_preferences', []))}
- 계절별 추천: {', '.join(user_profile.get('seasonal_recommendations', []))}
- 식이 고려사항: {', '.join(user_profile.get('dietary_considerations', []))}
- 가격대: {user_profile.get('price_range', 'N/A')}
- 분위기 선호도: {', '.join(user_profile.get('ambiance_preference', []))}
"""
        
        prompt = (
            f"다음은 사용자 정보입니다:\n"
            f"나이: {state['age']}\n"
            f"선호 음식: {state['cuisine_preference']}\n"
            f"지역: {state['location']}\n"
            f"동반자유형: {state['companion_type']}\n"
            f"원하는 분위기: {state['ambiance']}\n"
            f"특별 요구사항: {', '.join(state['special_requirements']) if state['special_requirements'] else '없음'}\n"
            f"{profile_info}\n"
            f"검색된 맛집 목록:\n"
            f"{chr(10).join(formatted_recommendations)}\n\n"
            f"위 정보를 바탕으로 사용자에게 가장 적합한 맛집을 추천해주세요."
            f"나이대별 선호도, 날씨, 계절, 식이 고려사항, 동반자유형, 분위기, 특별 요구사항을 종합적으로 고려하여 맛집을 선별하고 그 이유도 상세히 설명해주세요. "
            f"3개의 맛집을 추천하고, 각 맛집에 대한 특징과 추천 이유를 **대표 메뉴, 가격대, 분위기, 전반적인 평점(별점 표현), 동반자유형 적합성, 특별 요구사항 만족도**를 포함하여 한국어로 작성해주세요."
            f"사용자의 나이대와 선호도를 고려한 맞춤형 추천이 되도록 해주세요."
        )
        
        refined_recommendation = llm.invoke(prompt)
        # print("gemini 추천 결과:")
        # print(refined_recommendation)
        
        state['recommendations'] = [refined_recommendation]
    except Exception as e:
        print(f"gemini 추천 중 오류 발생: {e}")
        print("오류로 인해 포맷팅된 검색 결과를 그대로 사용합니다.")
        state['recommendations'] = formatted_recommendations
    
    return state

# 에러 처리
def handle_error_node(state: GraphState) -> GraphState:
    """에러 처리 노드"""
    print(f"---오류 처리---")
    print(f"오류 발생: {state['error']}")
    return state
