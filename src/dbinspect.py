from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
load_dotenv()

class postgres:
    def __init__(self):
        self.user = os.getenv('DB_USER')           # PostgreSQL 사용자 이름(문제발생)
        self.password = os.getenv('DB_PASSWORD')     # PostgreSQL 비밀번호
        self.host = os.getenv('DB_HOST')           # 서버 주소 (원격일 경우 IP 주소)
        self.port = os.getenv('DB_PORT')                # PostgreSQL 기본 포트
        self.database = os.getenv('DB_DATABASE')     # 사용할 데이터베이스 이름

    def dbconnect(self):
        # PostgreSQL 연결 설정
        engine = create_engine(f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}')
        try:
            with engine.connect() as conn:
                print('dbconnect success')
                return conn
        except Exception as e:
            print(f'dbconnect error: {e}')
            return None
    
    def db_query(self, query: str):
        with self.dbconnect() as conn:
            return conn.execute(text(query))