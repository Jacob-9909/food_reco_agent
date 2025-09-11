export interface UserInput {
  age: number;
  cuisine_preference: string;
  weather: string;
  location: string;
  companion_type: string;
  ambiance: string;
  special_requirements?: string;
}

export interface SearchResult {
  title: string;
  description: string;
  link?: string;
}

export interface UserProfile {
  age_group: string;
  season: string;
  weather_condition: string;
  preferred_cuisine: string;
  companion_type: string;
  preferred_ambiance: string;
}

export interface RecommendationResponse {
  session_id: number;
  recommendations: string[];
  search_results: SearchResult[];
  user_profile: UserProfile;
  created_at: string;
}

export interface HealthResponse {
  status: string;
  timestamp: string;
  version: string;
}
