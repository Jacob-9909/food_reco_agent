import React from 'react';

const LoadingSpinner: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="relative">
        <div className="w-16 h-16 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin"></div>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-2xl">🍽️</span>
        </div>
      </div>
      <p className="mt-4 text-lg font-medium text-gray-700">
        맛집을 검색하고 추천을 생성하는 중입니다...
      </p>
      <p className="mt-2 text-sm text-gray-500">
        잠시만 기다려주세요
      </p>
    </div>
  );
};

export default LoadingSpinner;
