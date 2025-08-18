# 서드파티 라이브러리
from dotenv import load_dotenv
from langgraph.graph import END, StateGraph

# 로컬 애플리케이션
from types import GraphState
from nodes import (
    get_user_input,
    analyze_user_preferences,
    search_restaurants,
    recommend_restaurants,
    handle_error_node
)

load_dotenv()

# 조건부 엣지 함수
def should_continue(state: GraphState) -> str:
    """에러 발생 여부에 따라 다음 노드 결정"""
    if state.get('error'):
        return "handle_error"
    return "recommend_restaurants"

# 그래프 빌드
workflow = StateGraph(GraphState)

workflow.add_node("get_user_input", get_user_input) # 사용자 입력 받기
workflow.add_node("analyze_user_preferences", analyze_user_preferences) # 사용자 선호도 분석
workflow.add_node("search_restaurants", search_restaurants) # 맛집 검색
workflow.add_node("recommend_restaurants", recommend_restaurants) # 맛집 추천
workflow.add_node("handle_error", handle_error_node) # 에러 처리

workflow.set_entry_point("get_user_input") # 시작 노드
workflow.add_edge("get_user_input", "analyze_user_preferences") # 사용자 입력 받기 -> 사용자 선호도 분석
workflow.add_edge("analyze_user_preferences", "search_restaurants") # 사용자 선호도 분석 -> 맛집 검색
workflow.add_conditional_edges(
    "search_restaurants",
    should_continue, # 맛집 검색 -> 맛집 추천 or 에러 처리
    {
        "recommend_restaurants": "recommend_restaurants", # 맛집 추천
        "handle_error": "handle_error" # 에러 처리
    }
)
workflow.add_edge("recommend_restaurants", END) # 맛집 추천 -> 종료
workflow.add_edge("handle_error", END) # 에러 처리 -> 종료

# 그래프 컴파일
app = workflow.compile()

# 실행
if __name__ == "__main__":
    initial_state = {
        "age": 0,
        "cuisine_preference": "",
        "weather": "",
        "location": "",
        "companion_type": "",
        "ambiance": "",
        "special_requirements": [],
        "search_results": [],
        "recommendations": [],
        "error": "",
        "user_profile": {}
    }
    
    # LangGraph 실행
    final_results = app.invoke(initial_state) # get_user_input부터 시작
    
    print("\n---최종 결과---")
    if final_results.get('recommendations'):
        print("추천된 맛집:")
        for r in final_results['recommendations']:
            print(f"- {r}")
    if final_results.get('error'):
        print(f"오류: {final_results['error']}")
