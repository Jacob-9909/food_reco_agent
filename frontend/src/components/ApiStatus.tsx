import React from 'react';

interface ApiStatusProps {
  isHealthy: boolean;
}

const ApiStatus: React.FC<ApiStatusProps> = ({ isHealthy }) => {
  return (
    <div className="mb-6">
      {isHealthy ? (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4 flex items-center space-x-3">
          <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-green-800 font-medium">✅ API 서버 연결 성공!</span>
        </div>
      ) : (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-center space-x-3">
          <div className="w-3 h-3 bg-red-500 rounded-full"></div>
          <span className="text-red-800 font-medium">⚠️ API 서버 연결 실패</span>
        </div>
      )}
    </div>
  );
};

export default ApiStatus;
