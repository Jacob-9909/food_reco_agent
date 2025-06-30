# 표준 라이브러리
import os
from typing import List, TypedDict, Dict, Any

# 서드파티 라이브러리
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_openai import OpenAI
from langgraph.graph import END, StateGraph

# 로컬 애플리케이션
from naver_search import search_restaurants as naver_search
from restaurant_data import search_restaurants as backup_search

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
google_cse_id = os.getenv("GOOGLE_CSE_ID")
openai_api_key = os.getenv("OPENAI_API_KEY")

# 상태 정의
class GraphState(TypedDict):
    age: int
    cuisine_preference: str
    weather: str
    location: str
    search_results: List[Dict[str, str]]
    recommendations: List[str]
    error: str
    user_profile: Dict[str, Any]  # 사용자 프로필 정보 추가

# 노드 함수 정의
def get_user_input(state: GraphState) -> GraphState:
    """사용자로부터 입력을 받는 노드"""
    print("---사용자 입력 받기---")
    try:
        state['age'] = int(input("나이를 입력하세요: "))
        state['cuisine_preference'] = input("선호하는 음식 종류를 입력하세요: ")
        state['weather'] = input("현재 날씨를 입력하세요: ")
        state['location'] = input("지역을 입력하세요: ")
        print(f"입력: 나이={state['age']}, 선호음식={state['cuisine_preference']}, 날씨={state['weather']}, 지역={state['location']}")
    except Exception as e:
        print(f"입력 중 오류 발생: {e}")
        state['error'] = f"입력 중 오류가 발생했습니다: {e}"
    return state

def analyze_user_preferences(state: GraphState) -> GraphState:
    """사용자 선호도를 분석하고 프로필을 생성하는 노드"""
    print("---사용자 선호도 분석---")
    try:
        age = state['age']
        cuisine = state['cuisine_preference']
        weather = state['weather']
        
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
            "맑음": ["샐러드", "BBQ", "피자", "아이스크림"],
            "흐림": ["국수", "스튜", "핫팟", "커피"],
            "비": ["국수", "스튜", "핫팟", "따뜻한 음식"],
            "눈": ["핫팟", "스튜", "따뜻한 국", "따뜻한 음료"],
            "더움": ["냉면", "샐러드", "아이스크림", "콜드브루"],
            "추움": ["핫팟", "스튜", "따뜻한 국", "따뜻한 음료"]
        }
        
        # 계절별 추천 로직
        import datetime
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
            "age_group": age_group,
            "season": season,
            "weather_condition": weather,
            "preferred_cuisine": cuisine,
            "age_based_preferences": age_preferences.get(age_group, []),
            "weather_based_preferences": weather_preferences.get(weather, []),
            "seasonal_recommendations": get_seasonal_recommendations(season),
            "dietary_considerations": get_dietary_considerations(age),
            "price_range": get_price_range_by_age(age),
            "ambiance_preference": get_ambiance_preference(age_group)
        }
        
        state['user_profile'] = user_profile
        print(f"사용자 프로필 생성 완료: {age_group}, {season} 계절, {weather} 날씨")
        print(f"나이대별 선호도: {user_profile['age_based_preferences']}")
        print(f"날씨별 선호도: {user_profile['weather_based_preferences']}")
        
    except Exception as e:
        print(f"선호도 분석 중 오류 발생: {e}")
        state['error'] = f"선호도 분석 중 오류가 발생했습니다: {e}"
    
    return state

def get_seasonal_recommendations(season: str) -> List[str]:
    """계절별 추천 음식"""
    seasonal_foods = {
        "봄": ["나물", "딸기", "한우", "봄나물", "새싹채소"],
        "여름": ["냉면", "빙수", "콜드브루", "샐러드", "아이스크림"],
        "가을": ["게", "전복", "송이버섯", "단풍", "고구마"],
        "겨울": ["핫팟", "스튜", "따뜻한 국", "따뜻한 음료", "겨울나물"]
    }
    return seasonal_foods.get(season, [])

def get_dietary_considerations(age: int) -> List[str]:
    """나이별 식이 고려사항"""
    if age < 20:
        return ["영양 균형", "성장 촉진"]
    elif age < 40:
        return ["칼로리 관리", "영양 균형"]
    elif age < 60:
        return ["건강 관리", "칼로리 제한"]
    else:
        return ["건강식", "소화가 잘되는 음식", "영양소 보충"]

def get_price_range_by_age(age: int) -> str:
    """나이별 가격대 선호도"""
    if age < 20:
        return "저가"
    elif age < 30:
        return "중저가"
    elif age < 50:
        return "중가"
    else:
        return "중고가"

def get_ambiance_preference(age_group: str) -> List[str]:
    """나이대별 분위기 선호도"""
    ambiance_preferences = {
        "10대": ["트렌디", "인스타그래머블", "시끌벅적"],
        "20대": ["트렌디", "로맨틱", "친근함"],
        "30대": ["세련됨", "편안함", "로맨틱"],
        "40대": ["고급스러움", "편안함", "전통적"],
        "50대": ["고급스러움", "전통적", "편안함"],
        "60대 이상": ["전통적", "편안함", "고급스러움"]
    }
    return ambiance_preferences.get(age_group, [])

def search_restaurants(state: GraphState) -> GraphState:
    """네이버 또는 정적 데이터를 사용하여 맛집을 검색하고 search_results에 저장합니다."""
    print("---맛집 검색 중---")
    try:
        if not all(state.get(k) for k in ['location', 'cuisine_preference', 'weather']):
            raise ValueError("검색에 필요한 'location', 'cuisine_preference', 'weather' 정보가 누락되었습니다.")

        print("네이버 API로 맛집 검색 시도 중...")
        results = naver_search(
            location=state['location'],
            cuisine=state['cuisine_preference'],
            weather=state['weather']
        )

        if not results:
            print("네이버 API 검색 결과가 없거나 오류가 발생했습니다. 정적 데이터로 대체합니다.")
            backup_results_str = backup_search(
                location=state['location'],
                cuisine=state['cuisine_preference'],
                weather=state['weather']
            )
            print(f"정적 데이터 검색 결과: {backup_results_str}")

            # 백업 데이터(문자열 리스트)를 딕셔너리 리스트로 변환
            results = []
            for item_str in backup_results_str:
                parts = item_str.split('\n')
                results.append({
                    'title': parts[0] if len(parts) > 0 else '',
                    'description': parts[1] if len(parts) > 1 else '',
                    'link': parts[2] if len(parts) > 2 else ''
                })

        state['search_results'] = results[:5]
        state['error'] = ""
    except ValueError as ve:
        print(f"입력값 오류: {ve}")
        state['search_results'] = []
        state['error'] = str(ve)
    except Exception as e:
        print(f"검색 중 오류 발생: {e}")
        state['search_results'] = []
        state['error'] = f"맛집 검색 중 오류가 발생했습니다: {e}"
    return state

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
        formatted_rec = f"{i}. {title} - {description[:500]}{'...' if len(description) > 500 else ''}"
        formatted_recommendations.append(formatted_rec)
        
    try:
        print("OpenAI를 사용하여 맛집 추천을 개인화합니다...")
        llm = OpenAI(temperature=0.7)
        
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
            f"다음은 사용자의 입력 정보입니다:\n"
            f"나이: {state['age']}\n"
            f"선호 음식: {state['cuisine_preference']}\n"
            f"날씨: {state['weather']}\n"
            f"지역: {state['location']}\n"
            f"{profile_info}\n"
            f"검색된 맛집 목록:\n"
            f"{chr(10).join(formatted_recommendations)}\n\n"
            f"위 정보를 바탕으로 사용자에게 가장 적합한 맛집을 추천해주세요."
            f"나이대별 선호도, 날씨, 계절, 식이 고려사항을 종합적으로 고려하여 맛집을 선별하고 그 이유도 상세히 설명해주세요. "
            f"최대 3개의 맛집을 추천하고, 각 맛집에 대한 특징과 추천 이유를 **대표 메뉴, 가격대, 분위기, 전반적인 평점(별점 표현)**을 포함하여 한국어로 작성해주세요."
            f"사용자의 나이대와 선호도를 고려한 맞춤형 추천이 되도록 해주세요."
        )
        
        refined_recommendation = llm.invoke(prompt)
        print("OpenAI 추천 결과:")
        print(refined_recommendation)
        
        state['recommendations'] = [refined_recommendation]
    except Exception as e:
        print(f"OpenAI 추천 중 오류 발생: {e}")
        print("오류로 인해 포맷팅된 검색 결과를 그대로 사용합니다.")
        state['recommendations'] = formatted_recommendations
    
    return state

# 조건부 엣지 함수
def should_continue(state: GraphState) -> str:
    """에러 발생 여부에 따라 다음 노드 결정"""
    if state.get('error'):
        return "handle_error"
    return "recommend_restaurants"

def handle_error_node(state: GraphState) -> GraphState:
    """에러 처리 노드"""
    print(f"---오류 처리---")
    print(f"오류 발생: {state['error']}")
    return state

# 그래프 빌드
workflow = StateGraph(GraphState)

workflow.add_node("get_user_input", get_user_input)
workflow.add_node("analyze_user_preferences", analyze_user_preferences)
workflow.add_node("search_restaurants", search_restaurants)
workflow.add_node("recommend_restaurants", recommend_restaurants)
workflow.add_node("handle_error", handle_error_node)


workflow.set_entry_point("get_user_input")
workflow.add_edge("get_user_input", "analyze_user_preferences")
workflow.add_edge("analyze_user_preferences", "search_restaurants")
workflow.add_conditional_edges(
    "search_restaurants",
    should_continue,
    {
        "recommend_restaurants": "recommend_restaurants",
        "handle_error": "handle_error"
    }
)
workflow.add_edge("recommend_restaurants", END)
workflow.add_edge("handle_error", END)


# 그래프 컴파일
app = workflow.compile()

# 실행
if __name__ == "__main__":
    initial_state = {
        "age": 0,
        "cuisine_preference": "",
        "weather": "",
        "location": "",
        "search_results": [],
        "recommendations": [],
        "error": "",
        "user_profile": {}
    }
    
    # LangGraph 실행 (예시: 초기 상태를 직접 제공)
    # app.invoke(initial_state) 와 같이 직접 호출하거나,
    # 사용자 입력을 받는 흐름을 시작할 수 있습니다.
    # 아래는 get_user_input 부터 시작하는 전체 흐름입니다.
    
    final_results = app.invoke(initial_state) # get_user_input부터 시작
    
    print("\n---최종 결과---")
    if final_results.get('recommendations'):
        print("추천된 맛집:")
        for r in final_results['recommendations']:
            print(f"- {r}")
    if final_results.get('error'):
        print(f"오류: {final_results['error']}")
