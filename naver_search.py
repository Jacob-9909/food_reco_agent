"""
네이버 검색 API를 활용한 맛집 검색 모듈
"""
import os
import json
import urllib.request
import urllib.parse
import urllib.error

def search_web(query, display=5):
    """
    네이버 웹 검색 API를 사용하여 정보를 검색합니다.
    
    Args:
        query (str): 검색어
        display (int): 검색 결과 출력 건수 (기본값 5)
        
    Returns:
        list: 검색 결과 목록
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
    url = url + "?" + query_string
    
    # HTTP 요청 헤더 설정
    request = urllib.request.Request(url)
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
                    # 검색 결과 포맷팅
                    search_info = f"{title}\n{description}\n{item['link']}"
                    search_results.append(search_info)
                return search_results
            else:
                return ["검색 결과가 없습니다."]
        else:
            return [f"API 호출 실패: {response_code}"]
            
    except urllib.error.HTTPError as e:
        return [f"HTTP 오류: {e.code}"]
    except urllib.error.URLError as e:
        return [f"URL 오류: {e.reason}"]
    except Exception as e:
        return [f"검색 중 오류 발생: {e}"]

def search_restaurants(location, cuisine, weather):
    """
    네이버 웹 검색 API를 사용하여 맛집을 검색합니다.
    
    Args:
        location (str): 위치 (예: '서울', '부산', '대구')
        cuisine (str): 음식 종류 (예: '한식', '중식', '일식', '양식')
        weather (str): 날씨 (예: '맑음', '흐림', '비', '더움', '추움')
        
    Returns:
        list: 맛집 추천 목록
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
    
    # 네이버 API로 검색
    results = search_web(query)
    
    if not results or results[0].startswith("검색 중 오류") or results[0].startswith("API 호출"):
        # 오류 발생 시 간단한 검색어로 재시도
        query_simple = f"{location} {cuisine} 맛집"
        print(f"오류 발생으로 단순 검색어로 재시도: {query_simple}")
        results = search_web(query_simple)
        
    return results
