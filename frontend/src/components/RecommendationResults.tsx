import React, { useState } from 'react';
import { RecommendationResponse } from '../types';

interface RecommendationResultsProps {
  recommendations: RecommendationResponse;
  onNewRecommendation: () => void;
}

const RecommendationResults: React.FC<RecommendationResultsProps> = ({ 
  recommendations, 
  onNewRecommendation 
}) => {
  const [expandedProfile, setExpandedProfile] = useState(false);
  const [expandedSearch, setExpandedSearch] = useState<number | null>(null);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('ko-KR');
  };

  return (
    <div className="space-y-6">
      {/* 헤더 */}
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900 flex items-center">
          <span className="mr-2">🎯</span>
          추천 결과
        </h2>
        <button
          onClick={onNewRecommendation}
          className="btn-secondary flex items-center space-x-2"
        >
          <span>🔄</span>
          <span>새로운 추천 받기</span>
        </button>
      </div>

      {/* 사용자 프로필 정보 */}
      <div className="card">
        <button
          onClick={() => setExpandedProfile(!expandedProfile)}
          className="w-full flex items-center justify-between text-left"
        >
          <h3 className="text-lg font-semibold flex items-center">
            <span className="mr-2">👤</span>
            사용자 프로필 정보
          </h3>
          <span className={`transform transition-transform ${expandedProfile ? 'rotate-180' : ''}`}>
            ▼
          </span>
        </button>
        
        {expandedProfile && (
          <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="metric-card">
              <h4 className="text-sm font-medium text-gray-600">나이대</h4>
              <p className="text-xl font-bold text-primary-600">
                {recommendations.user_profile.age_group || 'N/A'}
              </p>
            </div>
            <div className="metric-card">
              <h4 className="text-sm font-medium text-gray-600">계절</h4>
              <p className="text-xl font-bold text-primary-600">
                {recommendations.user_profile.season || 'N/A'}
              </p>
            </div>
            <div className="metric-card">
              <h4 className="text-sm font-medium text-gray-600">날씨</h4>
              <p className="text-xl font-bold text-primary-600">
                {recommendations.user_profile.weather_condition || 'N/A'}
              </p>
            </div>
            <div className="metric-card">
              <h4 className="text-sm font-medium text-gray-600">선호 음식</h4>
              <p className="text-xl font-bold text-primary-600">
                {recommendations.user_profile.preferred_cuisine || 'N/A'}
              </p>
            </div>
            <div className="metric-card">
              <h4 className="text-sm font-medium text-gray-600">동반자 유형</h4>
              <p className="text-xl font-bold text-primary-600">
                {recommendations.user_profile.companion_type || 'N/A'}
              </p>
            </div>
            <div className="metric-card">
              <h4 className="text-sm font-medium text-gray-600">분위기</h4>
              <p className="text-xl font-bold text-primary-600">
                {recommendations.user_profile.preferred_ambiance || 'N/A'}
              </p>
            </div>
          </div>
        )}
      </div>

      {/* 검색 결과 */}
      {recommendations.search_results && recommendations.search_results.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-semibold mb-4 flex items-center">
            <span className="mr-2">🔍</span>
            검색된 맛집 목록
          </h3>
          <div className="space-y-4">
            {recommendations.search_results.map((restaurant, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4">
                <button
                  onClick={() => setExpandedSearch(expandedSearch === index ? null : index)}
                  className="w-full flex items-center justify-between text-left"
                >
                  <h4 className="font-medium text-gray-900">
                    {index + 1}. {restaurant.title || '제목 없음'}
                  </h4>
                  <span className={`transform transition-transform ${expandedSearch === index ? 'rotate-180' : ''}`}>
                    ▼
                  </span>
                </button>
                
                {expandedSearch === index && (
                  <div className="mt-3 pt-3 border-t border-gray-100">
                    <p className="text-gray-700 mb-2">
                      <strong>설명:</strong> {restaurant.description || '설명 없음'}
                    </p>
                    {restaurant.link && (
                      <a
                        href={restaurant.link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-primary-600 hover:text-primary-700 underline"
                      >
                        링크 보기 →
                      </a>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* AI 추천 결과 */}
      {recommendations.recommendations && recommendations.recommendations.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-semibold mb-4 flex items-center">
            <span className="mr-2">🤖</span>
            AI 개인화 추천
          </h3>
          <div className="space-y-6">
            {recommendations.recommendations.map((recommendation, index) => (
              <div key={index} className="border-l-4 border-primary-500 pl-4">
                <h4 className="font-semibold text-gray-900 mb-2">
                  추천 {index + 1}
                </h4>
                <div 
                  className="prose prose-sm max-w-none text-gray-700"
                  dangerouslySetInnerHTML={{ 
                    __html: recommendation.replace(/\n/g, '<br>') 
                  }}
                />
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 세션 정보 */}
      <div className="bg-gray-50 rounded-lg p-4 text-sm text-gray-600">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <span>
            📊 세션 ID: <strong>{recommendations.session_id || 'N/A'}</strong>
          </span>
          <span>
            생성 시간: <strong>{formatDate(recommendations.created_at)}</strong>
          </span>
        </div>
      </div>
    </div>
  );
};

export default RecommendationResults;
