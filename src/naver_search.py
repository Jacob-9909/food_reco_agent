import os
import json
import urllib.request
import urllib.parse
import urllib.error
from typing import List, Dict

class NaverAPIError(Exception):
    """네이버 API 호출 시 발생하는 오류"""
    pass

def search_web(query: str, display: int = 50) -> List[Dict[str, str]]:
    """
    네이버 웹 검색 API를 사용하여 정보를 검색하고 구조화된 딕셔너리 리스트를 반환합니다.
    
    Args:
        query (str): 검색어
        display (int): 검색 결과 출력 건수 (기본값 50)
        
    Returns:
        List[Dict[str, str]]: 검색 결과 목록. 각 항목은 'title', 'description', 'link' 키를 가집니다.
        
    Raises:
        ValueError: API 키가 설정되지 않은 경우
        NaverAPIError: API 호출에 실패한 경우
    """
    client_id = os.getenv("NAVER_CLIENT_ID")
    client_secret = os.getenv("NAVER_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        raise ValueError("네이버 API 클라이언트 ID와 시크릿이 설정되지 않았습니다. .env 파일을 확인하세요.")
    
    url = "https://openapi.naver.com/v1/search/webkr.json"  # 웹 검색 API
    params = {
        "query": query,
        "display": display,
        "start": 1,
        "sort": "sim"  # 정렬 옵션: sim(유사도순), date(날짜순)
    }
    
    # URL 인코딩
    query_string = urllib.parse.urlencode(params)
    request_url = url + "?" + query_string
    
    # HTTP 요청 헤더 설정
    request = urllib.request.Request(request_url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    
    try:
        # API 요청 보내기
        response = urllib.request.urlopen(request)
        
        # 응답 처리
        response_code = response.getcode()
        if response_code == 200:  # 정상 응답
            response_body = response.read()
            response_body_str = response_body.decode('utf-8')
            result = json.loads(response_body_str)
            
            # 결과 가공
            search_results = []
            if 'items' in result and result['items']:
                for item in result['items']:
                    # HTML 태그 제거
                    title = item['title'].replace('<b>', '').replace('</b>', '')
                    description = item['description'].replace('<b>', '').replace('</b>', '')
                    search_results.append({
                        "title": title,
                        "description": description,
                        "link": item['link']
                    })
            return search_results
        else:
            raise NaverAPIError(f"API 호출 실패: {response_code}")
            
    except urllib.error.HTTPError as e:
        raise NaverAPIError(f"HTTP 오류: {e.code} - {e.read().decode('utf-8')}") from e
    except urllib.error.URLError as e:
        raise NaverAPIError(f"URL 오류: {e.reason}") from e
    except Exception as e:
        raise NaverAPIError(f"검색 중 알 수 없는 오류 발생: {e}") from e

def search_restaurants(location: str, cuisine: str, weather: str) -> List[Dict[str, str]]:
    """
    네이버 웹 검색 API를 사용하여 맛집을 검색합니다.
    
    Args:
        location (str): 위치 (예: '서울', '부산', '대구')
        cuisine (str): 음식 종류 (예: '한식', '중식', '일식', '양식')
        weather (str): 날씨 (예: '맑음', '흐림', '비', '더움', '추움')
        
    Returns:
        List[Dict[str, str]]: 맛집 추천 목록
    """
    # 날씨에 따른 키워드 추가
    weather_keywords = {
        "맑음": "뷰 좋은",
        "흐림": "아늑한",
        "비": "실내",
        "더움": "시원한",
        "추움": "따뜻한"
    }
    
    # 검색어 구성
    weather_keyword = weather_keywords.get(weather, "")
    query = f"{location} {cuisine} {weather_keyword} 맛집 추천"
    print(f"네이버 검색어: {query}")
    
    try:
        results = search_web(query)
        if not results:
            # 결과가 없을 경우, 더 간단한 검색어로 재시도
            print("첫 번째 검색 결과가 없습니다. 단순 검색어로 재시도합니다.")
            query_simple = f"{location} {cuisine} 맛집"
            print(f"재시도 검색어: {query_simple}")
            results = search_web(query_simple)
    except NaverAPIError as e:
        print(f"네이버 API 오류 발생: {e}. 단순 검색어로 재시도합니다.")
        query_simple = f"{location} {cuisine} 맛집"
        print(f"재시도 검색어: {query_simple}")
        try:
            results = search_web(query_simple)
        except NaverAPIError as e_simple:
            print(f"재시도 중에도 오류 발생: {e_simple}")
            return []  # 재시도 실패 시 빈 리스트 반환
            
    return results
