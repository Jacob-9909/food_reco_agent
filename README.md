# 맛집 추천 에이전트

이 프로젝트는 사용자의 나이, 선호 음식, 날씨, 위치, 날짜 등의 정보를 바탕으로 맛집을 추천해주는 AI 에이전트입니다.

## 기능

- 사용자 정보 수집 (나이, 선호 음식, 날씨, 위치, 날짜)
- 네이버 API를 통한 맛집 검색
- 검색 실패 시 정적 데이터 기반 백업 검색 기능
- OpenAI를 활용한 개인화된 맛집 추천

## 사용 기술

- Python
- LangChain
- LangGraph
- OpenAI API
- Naver 검색 API

## 설치 방법

```bash
# 필수 패키지 설치
pip install -r requirements.txt

# .env 파일에 API 키 설정
# OPENAI_API_KEY=your_openai_api_key
# NAVER_CLIENT_ID=your_naver_client_id
# NAVER_CLIENT_SECRET=your_naver_client_secret
```

## 사용 방법

```bash
python main.py
```

프롬프트에 따라 사용자 정보를 입력하면 맛집 추천 결과를 받을 수 있습니다.

## 워크플로우

아래는 맛집 추천 에이전트의 워크플로우를 시각적으로 표현한 다이어그램입니다:

```mermaid
graph TD
    A[get_user_input] --> B[search_restaurants]
    B -->|success| C[recommend_restaurants]
    B -->|error| D[handle_error]
    C --> E[END]
    D --> E[END]
    
    style A fill:#a8d5ff,stroke:#333,stroke-width:2px
    style B fill:#ffe8a8,stroke:#333,stroke-width:2px
    style C fill:#b8ffb8,stroke:#333,stroke-width:2px
    style D fill:#ffb8b8,stroke:#333,stroke-width:2px
    style E fill:#d8d8d8,stroke:#333,stroke-width:2px
```

워크플로우는 LangGraph의 StateGraph를 사용하여 구현되었으며, 다음과 같은 순서로 진행됩니다:

1. 사용자 입력 수집 (나이, 선호 음식, 날씨, 위치, 날짜)
2. 네이버 API를 통한 맛집 검색
3. 검색 결과에 따라 추천 또는 에러 처리 분기
4. 맛집 추천 또는 에러 메시지 출력