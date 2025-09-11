import React from 'react';

const Header: React.FC = () => {
  return (
    <header className="bg-white shadow-sm border-b">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <span className="text-3xl">🍽️</span>
            <h1 className="text-2xl font-bold text-gray-900">
              음식 추천 에이전트
            </h1>
          </div>
          <div className="hidden md:flex items-center space-x-4 text-sm text-gray-600">
            <span>개인화된 맛집 추천</span>
            <span>•</span>
            <span>AI 기반 추천</span>
            <span>•</span>
            <span>실시간 검색</span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
