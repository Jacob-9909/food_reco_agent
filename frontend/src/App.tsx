import React, { useState, useEffect } from 'react';
import { UserInput, RecommendationResponse } from './types';
import { ApiService } from './services/api';
import Header from './components/Header';
import RecommendationForm from './components/RecommendationForm';
import RecommendationResults from './components/RecommendationResults';
import LoadingSpinner from './components/LoadingSpinner';
import ApiStatus from './components/ApiStatus';

function App() {
  const [isApiHealthy, setIsApiHealthy] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [recommendations, setRecommendations] = useState<RecommendationResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  // API 상태 확인
  useEffect(() => {
    const checkApiHealth = async () => {
      const healthy = await ApiService.checkHealth();
      setIsApiHealthy(healthy);
    };

    checkApiHealth();
    // 30초마다 API 상태 확인
    const interval = setInterval(checkApiHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  const handleRecommendationRequest = async (userInput: UserInput) => {
    setIsLoading(true);
    setError(null);
    setRecommendations(null);

    try {
      const result = await ApiService.getRecommendations(userInput);
      if (result) {
        setRecommendations(result);
      } else {
        setError('추천 생성에 실패했습니다. 다시 시도해주세요.');
      }
    } catch (err) {
      setError('서버와의 통신 중 오류가 발생했습니다.');
      console.error('Recommendation request failed:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewRecommendation = () => {
    setRecommendations(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <div className="container mx-auto px-4 py-8">
        <ApiStatus isHealthy={isApiHealthy} />
        
        {!isApiHealthy ? (
          <div className="max-w-2xl mx-auto">
            <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
              <h2 className="text-xl font-semibold text-red-800 mb-2">
                ⚠️ API 서버에 연결할 수 없습니다
              </h2>
              <p className="text-red-600 mb-4">
                서버가 실행 중인지 확인해주세요.
              </p>
              <p className="text-sm text-red-500">
                터미널에서 다음 명령어로 API 서버를 시작하세요: <code className="bg-red-100 px-2 py-1 rounded">python -m src.api.main</code>
              </p>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
            {/* 사이드바 - 추천 폼 */}
            <div className="lg:col-span-1">
              <div className="sticky top-8">
                <RecommendationForm 
                  onSubmit={handleRecommendationRequest}
                  isLoading={isLoading}
                />
              </div>
            </div>
            
            {/* 메인 콘텐츠 */}
            <div className="lg:col-span-3">
              {isLoading && <LoadingSpinner />}
              
              {error && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-6 mb-6">
                  <h3 className="text-lg font-semibold text-red-800 mb-2">오류 발생</h3>
                  <p className="text-red-600">{error}</p>
                  <button 
                    onClick={handleNewRecommendation}
                    className="mt-4 btn-primary"
                  >
                    다시 시도
                  </button>
                </div>
              )}
              
              {recommendations && (
                <RecommendationResults 
                  recommendations={recommendations}
                  onNewRecommendation={handleNewRecommendation}
                />
              )}
              
              {!isLoading && !error && !recommendations && (
                <div className="text-center py-12">
                  <div className="max-w-2xl mx-auto">
                    <h2 className="text-3xl font-bold text-gray-900 mb-4">
                      🎯 개인화된 맛집 추천 서비스
                    </h2>
                    <p className="text-lg text-gray-600 mb-8">
                      왼쪽 사이드바에서 정보를 입력하고 <strong>"맛집 추천 받기"</strong> 버튼을 클릭하세요!
                    </p>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                      <div className="metric-card">
                        <h3 className="text-2xl font-bold text-primary-600">1,234</h3>
                        <p className="text-gray-600">총 추천 수</p>
                        <span className="text-green-600 text-sm">+12</span>
                      </div>
                      <div className="metric-card">
                        <h3 className="text-2xl font-bold text-primary-600">567</h3>
                        <p className="text-gray-600">활성 사용자</p>
                        <span className="text-green-600 text-sm">+8</span>
                      </div>
                      <div className="metric-card">
                        <h3 className="text-2xl font-bold text-primary-600">4.8/5.0</h3>
                        <p className="text-gray-600">평균 만족도</p>
                        <span className="text-green-600 text-sm">+0.2</span>
                      </div>
                      <div className="metric-card">
                        <h3 className="text-2xl font-bold text-primary-600">전국</h3>
                        <p className="text-gray-600">지원 지역</p>
                        <span className="text-blue-600 text-sm">서울</span>
                      </div>
                    </div>
                    
                    <div className="bg-white rounded-lg shadow-md p-6 text-left">
                      <h3 className="text-xl font-semibold mb-4">✨ 주요 기능</h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="flex items-start space-x-3">
                          <span className="text-primary-600 text-xl">👥</span>
                          <div>
                            <h4 className="font-medium">나이대별 선호도 분석</h4>
                            <p className="text-sm text-gray-600">나이에 따른 음식 선호도 패턴 분석</p>
                          </div>
                        </div>
                        <div className="flex items-start space-x-3">
                          <span className="text-primary-600 text-xl">🌤️</span>
                          <div>
                            <h4 className="font-medium">날씨별 추천</h4>
                            <p className="text-sm text-gray-600">현재 날씨에 맞는 음식 추천</p>
                          </div>
                        </div>
                        <div className="flex items-start space-x-3">
                          <span className="text-primary-600 text-xl">👨‍👩‍👧‍👦</span>
                          <div>
                            <h4 className="font-medium">동반자별 맞춤</h4>
                            <p className="text-sm text-gray-600">혼밥, 데이트, 가족식사 등 상황별 추천</p>
                          </div>
                        </div>
                        <div className="flex items-start space-x-3">
                          <span className="text-primary-600 text-xl">🤖</span>
                          <div>
                            <h4 className="font-medium">AI 개인화</h4>
                            <p className="text-sm text-gray-600">Google Gemini를 활용한 맞춤형 추천</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
