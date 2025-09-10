"""
FastAPI 메인 애플리케이션

음식 추천 에이전트의 웹 API 서버를 제공합니다.
"""

# FastAPI 관련
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

# 데이터 검증 및 모델링
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# 서버 실행
import uvicorn
from datetime import datetime

# 로컬 모듈
from ..core import workflow_app  # LangGraph 워크플로우
from ..database import save_user_session, save_search_results, save_recommendation

# FastAPI 앱 인스턴스 생성
app = FastAPI(
    title="음식 추천 에이전트 API",
    description="사용자 선호도 기반 개인화된 맛집 추천 서비스",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic 모델 정의
class UserInput(BaseModel):
    """사용자 입력 데이터 모델"""
    age: int = Field(..., ge=1, le=120, description="사용자 나이")
    cuisine_preference: str = Field(..., min_length=1, description="선호 음식 종류")
    weather: str = Field(..., min_length=1, description="현재 날씨")
    location: str = Field(..., min_length=1, description="지역")
    companion_type: str = Field(..., min_length=1, description="동반자 유형")
    ambiance: str = Field(..., min_length=1, description="원하는 분위기")
    special_requirements: Optional[str] = Field(None, description="특별 요구사항")

class RecommendationResponse(BaseModel):
    """추천 결과 응답 모델"""
    session_id: int
    recommendations: List[str]
    search_results: List[Dict[str, str]]
    user_profile: Dict[str, Any]
    created_at: datetime

class HealthResponse(BaseModel):
    """헬스 체크 응답 모델"""
    status: str
    timestamp: datetime
    version: str

# API 엔드포인트
@app.get("/", response_class=HTMLResponse)
async def root():
    """메인 페이지"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>음식 추천 에이전트</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; }
            .api-link { display: inline-block; margin: 10px; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }
            .api-link:hover { background: #0056b3; }
            .description { text-align: center; margin: 20px 0; color: #666; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🍽️ 음식 추천 에이전트</h1>
            <p class="description">사용자 선호도 기반 개인화된 맛집 추천 서비스</p>
            <div style="text-align: center;">
                <a href="/docs" class="api-link">API 문서 보기</a>
                <a href="/health" class="api-link">서버 상태 확인</a>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """서버 상태 확인"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="1.0.0"
    )

@app.post("/recommend", response_model=RecommendationResponse)
async def get_recommendations(user_input: UserInput):
    """
    사용자 입력을 바탕으로 맛집을 추천합니다.
    
    Args:
        user_input: 사용자 입력 데이터
        
    Returns:
        RecommendationResponse: 추천 결과
    """
    try:
        # 초기 상태 설정
        initial_state = {
            "age": user_input.age,
            "cuisine_preference": user_input.cuisine_preference,
            "weather": user_input.weather,
            "location": user_input.location,
            "companion_type": user_input.companion_type,
            "ambiance": user_input.ambiance,
            "special_requirements": user_input.special_requirements or "",
            "search_results": [],
            "recommendations": [],
            "error": "",
            "user_profile": {},
            "session_id": 0
        }
        
        # LangGraph 워크플로우 실행
        final_results = workflow_app.invoke(initial_state)
        
        # 추천 결과 처리
        recommendations = []
        if final_results.get('recommendations'):
            for recommendation in final_results['recommendations']:
                if hasattr(recommendation, 'content'):
                    recommendations.append(recommendation.content)
                else:
                    recommendations.append(str(recommendation))
        
        return RecommendationResponse(
            session_id=final_results.get('session_id', 0),
            recommendations=recommendations,
            search_results=final_results.get('search_results', []),
            user_profile=final_results.get('user_profile', {}),
            created_at=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"추천 생성 중 오류가 발생했습니다: {str(e)}")

@app.get("/recommendations/{session_id}")
async def get_recommendation_by_session(session_id: int):
    """
    세션 ID로 추천 결과를 조회합니다.
    
    Args:
        session_id: 세션 ID
        
    Returns:
        추천 결과 정보
    """
    # TODO: 데이터베이스에서 세션별 추천 결과 조회 구현
    return {"message": f"세션 {session_id}의 추천 결과 조회 기능은 추후 구현 예정입니다."}

@app.get("/stats")
async def get_statistics():
    """
    서비스 통계 정보를 반환합니다.
    
    Returns:
        통계 정보
    """
    # TODO: 실제 통계 데이터 구현
    return {
        "total_sessions": 0,
        "total_recommendations": 0,
        "popular_cuisines": [],
        "popular_locations": []
    }

if __name__ == "__main__":
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
