import React, { useState } from 'react';
import { UserInput } from '../types';

interface RecommendationFormProps {
  onSubmit: (userInput: UserInput) => void;
  isLoading: boolean;
}

const RecommendationForm: React.FC<RecommendationFormProps> = ({ onSubmit, isLoading }) => {
  const [formData, setFormData] = useState<UserInput>({
    age: 25,
    cuisine_preference: '한식',
    weather: '맑음',
    location: '강남',
    companion_type: '혼밥',
    ambiance: '시끌벅적한',
    special_requirements: ''
  });

  const cuisineOptions = ['한식', '중식', '일식', '양식', '분식', '치킨', '피자', '카페', '기타'];
  const weatherOptions = ['맑음', '흐림', '비', '눈', '더움', '추움'];
  const companionOptions = ['혼밥', '데이트', '가족식사', '친구모임', '회식', '비즈니스'];
  const ambianceOptions = ['시끌벅적한', '조용한', '아늑한', '인스타감성', '전통적인', '모던한'];

  const handleInputChange = (field: keyof UserInput, value: string | number) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.location.trim()) {
      alert('지역을 입력해주세요.');
      return;
    }
    onSubmit(formData);
  };

  return (
    <div className="card">
      <h2 className="text-xl font-semibold mb-6 flex items-center">
        <span className="mr-2">📝</span>
        사용자 정보 입력
      </h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* 나이 */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            나이
          </label>
          <input
            type="number"
            min="1"
            max="120"
            value={formData.age}
            onChange={(e) => handleInputChange('age', parseInt(e.target.value) || 25)}
            className="input-field"
            placeholder="나이를 입력하세요"
          />
        </div>

        {/* 선호 음식 종류 */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            선호 음식 종류
          </label>
          <select
            value={formData.cuisine_preference}
            onChange={(e) => handleInputChange('cuisine_preference', e.target.value)}
            className="select-field"
          >
            {cuisineOptions.map(option => (
              <option key={option} value={option}>{option}</option>
            ))}
          </select>
        </div>

        {/* 날씨 */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            현재 날씨
          </label>
          <select
            value={formData.weather}
            onChange={(e) => handleInputChange('weather', e.target.value)}
            className="select-field"
          >
            {weatherOptions.map(option => (
              <option key={option} value={option}>{option}</option>
            ))}
          </select>
        </div>

        {/* 지역 */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            지역 <span className="text-red-500">*</span>
          </label>
          <input
            type="text"
            value={formData.location}
            onChange={(e) => handleInputChange('location', e.target.value)}
            className="input-field"
            placeholder="예: 강남, 홍대, 부산"
            required
          />
        </div>

        {/* 동반자 유형 */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            동반자 유형
          </label>
          <select
            value={formData.companion_type}
            onChange={(e) => handleInputChange('companion_type', e.target.value)}
            className="select-field"
          >
            {companionOptions.map(option => (
              <option key={option} value={option}>{option}</option>
            ))}
          </select>
        </div>

        {/* 분위기 */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            원하는 분위기
          </label>
          <select
            value={formData.ambiance}
            onChange={(e) => handleInputChange('ambiance', e.target.value)}
            className="select-field"
          >
            {ambianceOptions.map(option => (
              <option key={option} value={option}>{option}</option>
            ))}
          </select>
        </div>

        {/* 특별 요구사항 */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            특별 요구사항
          </label>
          <textarea
            value={formData.special_requirements}
            onChange={(e) => handleInputChange('special_requirements', e.target.value)}
            className="input-field h-24 resize-none"
            placeholder="예: 주차 가능, 반려동물 동반 가능, 채식 메뉴 있음, 키즈존 있음"
          />
        </div>

        {/* 제출 버튼 */}
        <button
          type="submit"
          disabled={isLoading}
          className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
        >
          {isLoading ? (
            <>
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              <span>처리 중...</span>
            </>
          ) : (
            <>
              <span>🍽️</span>
              <span>맛집 추천 받기</span>
            </>
          )}
        </button>
      </form>
    </div>
  );
};

export default RecommendationForm;
