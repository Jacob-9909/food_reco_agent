import { UserInput, RecommendationResponse, HealthResponse } from '../types';

const API_BASE_URL = 'http://localhost:8000';

export class ApiService {
  static async checkHealth(): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE_URL}/health`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      return response.ok;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  }

  static async getRecommendations(userInput: UserInput): Promise<RecommendationResponse | null> {
    try {
      const response = await fetch(`${API_BASE_URL}/recommend`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userInput),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data as RecommendationResponse;
    } catch (error) {
      console.error('Failed to get recommendations:', error);
      return null;
    }
  }

  static async getHealthStatus(): Promise<HealthResponse | null> {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Failed to get health status:', error);
      return null;
    }
  }
}
