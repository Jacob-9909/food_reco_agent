from sqlalchemy import create_engine, text, Column, Integer, String, DateTime, Boolean, and_, or_, func, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os
load_dotenv()

# class postgres:
#     def __init__(self):
#         self.user = os.getenv('DB_USER')           # PostgreSQL 사용자 이름(문제발생)
#         self.password = os.getenv('DB_PASSWORD')     # PostgreSQL 비밀번호
#         self.host = os.getenv('DB_HOST')           # 서버 주소 (원격일 경우 IP 주소)
#         self.port = os.getenv('DB_PORT')                # PostgreSQL 기본 포트
#         self.database = os.getenv('DB_DATABASE')     # 사용할 데이터베이스 이름

#     def dbconnect(self):
#         # PostgreSQL 연결 설정
#         engine = create_engine(f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}')
#         try:
#             with engine.connect() as conn:
#                 print('dbconnect success')
#                 return conn
#         except Exception as e:
#             print(f'dbconnect error: {e}')
#             return None
    
#     def db_query(self, query: str):
#         with self.dbconnect() as conn:
#             return conn.execute(text(query))

Base = declarative_base()

class Store(Base):
    __tablename__ = 'food_store'
    __table_args__ = {'schema': 'food_reco'}
    id = Column(Integer, primary_key=True)
    name = Column(String)
    region_id = Column(Integer)
    min_price = Column(Integer)
    max_price = Column(Integer)
    opening_hours = Column(String)
    rating = Column(Float)
    created_at = Column(DateTime)

    def __repr__(self):
        return f"<Store(id={self.id}, name={self.name}, region_id={self.region_id}, min_price={self.min_price}, max_price={self.max_price}, rating={self.rating})>"

class Region(Base):
    __tablename__ = 'mood'
    __table_args__ = {'schema': 'food_reco'}
    id = Column(Integer, primary_key=True)
    si = Column(String)
    gun = Column(String)
    gu = Column(String)

    def __repr__(self):
        return f"<Mood(id={self.id}, si={self.si}, gun={self.gun}, gu={self.gu})>"

class Mood(Base):
    __tablename__ = 'region'
    __table_args__ = {'schema': 'food_reco'}
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f"<Region(id={self.id}, name={self.name})>"

# 데이터베이스 연결 설정
engine = create_engine(f'postgresql+psycopg2://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_DATABASE")}')
Session = sessionmaker(bind=engine)

def orm_query_examples():
    """SQLAlchemy ORM을 사용한 다양한 쿼리 예제들"""
    session = Session()
    
    try:
        print("=== SQLAlchemy ORM 쿼리 예제 ===\n")
        
        # # 1. CREATE (생성)
        # print("1. CREATE - 새로운 매장 추가")
        # new_store = Store(name='맛있는 식당', region_id=1, min_price=15000)
        # session.add(new_store)
        # session.commit()
        # print(f"생성된 매장: {new_store}\n")
        
        # 2. READ - 모든 데이터 조회
        print("2. READ - 모든 매장 조회")
        all_stores = session.query(Store).all() # query method
        for store in all_stores:
            print(f"  {store}")
        print()
        
        # 3. READ - 조건부 조회 (WHERE 절)
        print("3. READ - 조건부 조회")
        # 특정 지역의 매장들
        region_1_stores = session.query(Store).filter(Store.region_id == 1).all() # filter method
        print(f"지역 1의 매장들: {region_1_stores}")
        
        # 최소 가격이 10000 이상인 매장들
        expensive_stores = session.query(Store).filter(Store.min_price >= 10000).all()
        print(f"최소 가격 10000원 이상 매장들: {expensive_stores}")
        print()
        
        # 4. READ - 복합 조건 (AND, OR)
        print("4. READ - 복합 조건")
        # AND 조건
        and_condition = session.query(Store).filter(
            and_(Store.region_id == 1, Store.min_price >= 10000)
        ).all()
        print(f"지역 1이면서 최소가격 10000원 이상: {and_condition}")
        
        # OR 조건
        or_condition = session.query(Store).filter(
            or_(Store.region_id == 1, Store.min_price < 5000)
        ).all()
        print(f"지역 1이거나 최소가격 5000원 미만: {or_condition}")
        print()
        
        # 5. READ - 정렬 (ORDER BY)
        print("5. READ - 정렬")
        # 가격 오름차순
        sorted_by_price = session.query(Store).order_by(Store.min_price.asc()).all()
        print(f"가격 오름차순: {sorted_by_price}")
        
        # 이름 내림차순
        sorted_by_name = session.query(Store).order_by(Store.name.desc()).all()
        print(f"이름 내림차순: {sorted_by_name}")
        print()
        
        # 6. READ - 제한 (LIMIT)
        print("6. READ - 제한")
        # 상위 3개만 조회
        top_3 = session.query(Store).limit(3).all()
        print(f"상위 3개: {top_3}")
        print()
        
        # 7. READ - 집계 함수
        print("7. READ - 집계 함수")
        # 총 매장 수
        total_count = session.query(Store).count()
        print(f"총 매장 수: {total_count}")
        
        # 평균 가격
        avg_price = session.query(func.avg(Store.min_price)).scalar()
        print(f"평균 최소 가격: {avg_price:.2f}원")
        
        # 최대 가격
        max_price = session.query(func.max(Store.min_price)).scalar()
        print(f"최대 최소 가격: {max_price}원")
        print()
        
        # 8. READ - LIKE 검색
        print("8. READ - LIKE 검색")
        # 이름에 '맛'이 포함된 매장들
        like_stores = session.query(Store).filter(Store.name.like('%맛%')).all()
        print(f"이름에 '맛'이 포함된 매장들: {like_stores}")
        print()
        
        # 9. UPDATE (수정)
        print("9. UPDATE - 매장 정보 수정")
        # 첫 번째 매장의 가격을 20000원으로 수정
        first_store = session.query(Store).first()
        if first_store:
            first_store.min_price = 20000
            session.commit()
            print(f"수정된 매장: {first_store}")
        print()
        
        # # 10. DELETE (삭제)

        # print("10. DELETE - 매장 삭제")
        # # 특정 조건의 매장 삭제 (예: 가격이 5000원 미만인 매장)
        # stores_to_delete = session.query(Store).filter(Store.min_price < 5000).all()
        # for store in stores_to_delete:
        #     session.delete(store)
        # session.commit()
        # print(f"삭제된 매장 수: {len(stores_to_delete)}")
        # print()
        
        # 11. READ - 최종 결과 확인
        print("11. 최종 결과 확인")
        final_stores = session.query(Store).all()
        print(f"현재 남은 매장들: {final_stores}")
        
        
    except Exception as e:
        print(f"오류 발생: {e}")
        session.rollback()
    finally:
        session.close()

def advanced_orm_queries():
    """고급 ORM 쿼리 예제들"""
    session = Session()
    
    try:
        print("\n=== 고급 ORM 쿼리 예제 ===\n")
        
        # 1. 서브쿼리
        print("1. 서브쿼리")
        # 평균 가격보다 비싼 매장들
        subquery = session.query(func.avg(Store.min_price)).subquery()
        expensive_stores = session.query(Store).filter(
            Store.min_price > subquery.c.anon_1
        ).all()
        print(f"평균 가격보다 비싼 매장들: {expensive_stores}")
        print()
        
        # 2. 그룹핑 (GROUP BY)
        print("2. 그룹핑")
        # 지역별 매장 수
        region_counts = session.query(
            Store.region_id, 
            func.count(Store.id).label('store_count')
        ).group_by(Store.region_id).all()
        print("지역별 매장 수:")
        for region_id, count in region_counts:
            print(f"  지역 {region_id}: {count}개")
        print()
        
        # 3. HAVING 절
        print("3. HAVING 절")
        # 매장이 2개 이상인 지역들
        regions_with_multiple_stores = session.query(
            Store.region_id,
            func.count(Store.id).label('store_count')
        ).group_by(Store.region_id).having(
            func.count(Store.id) >= 2
        ).all()
        print("매장이 2개 이상인 지역들:")
        for region_id, count in regions_with_multiple_stores:
            print(f"  지역 {region_id}: {count}개")
        print()
        
        # 4. EXISTS 절
        print("4. EXISTS 절")
        # 특정 조건을 만족하는 매장이 있는지 확인
        has_expensive_store = session.query(Store).filter(
            Store.min_price > 30000
        ).exists()
        print(f"30000원 이상 매장이 있는가? {session.query(has_expensive_store).scalar()}")
        print()
        
        # 5. JOIN 쿼리
        print("5. JOIN 쿼리")
        # Store와 Region을 JOIN하여 매장명과 지역명을 함께 조회
        store_region_join = session.query(
            Store.name.label('store_name'),
            Region.name.label('region_name'),
            Store.min_price,
            Store.rating
        ).join(Region, Store.region_id == Region.id).all()
        
        print("매장과 지역 정보:")
        for row in store_region_join:
            print(f"  매장: {row.store_name}, 지역: {row.region_name}, 최소가격: {row.min_price}원, 평점: {row.rating}")
        print()
        
        # 6. LEFT JOIN 쿼리
        print("6. LEFT JOIN 쿼리")
        # 모든 매장을 조회하되, 지역 정보가 없는 매장도 포함
        left_join_result = session.query(
            Store.name.label('store_name'),
            Region.name.label('region_name')
        ).outerjoin(Region, Store.region_id == Region.id).all()
        
        print("모든 매장 (지역 정보 포함):")
        for row in left_join_result:
            region_name = row.region_name if row.region_name else "지역 정보 없음"
            print(f"  매장: {row.store_name}, 지역: {region_name}")
        print()
        
    except Exception as e:
        print(f"오류 발생: {e}")
        session.rollback()
    finally:
        session.close()

def table_specific_queries():
    """각 테이블별 특화된 쿼리 예제들"""
    session = Session()
    
    try:
        print("\n=== 테이블별 특화 쿼리 예제 ===\n")
        
        # 1. Store 테이블 특화 쿼리
        print("1. Store 테이블 특화 쿼리")
        
        # 평점이 높은 상위 5개 매장
        top_rated_stores = session.query(Store).order_by(Store.rating.desc()).limit(5).all()
        print("평점 상위 5개 매장:")
        for store in top_rated_stores:
            print(f"  {store.name} - 평점: {store.rating}")
        print()
        
        # 가격대별 매장 수
        price_ranges = [
            (0, 10000, "1만원 미만"),
            (10000, 20000, "1-2만원"),
            (20000, 30000, "2-3만원"),
            (30000, 999999, "3만원 이상")
        ]
        
        print("가격대별 매장 수:")
        for min_price, max_price, label in price_ranges:
            count = session.query(Store).filter(
                and_(Store.min_price >= min_price, Store.min_price < max_price)
            ).count()
            print(f"  {label}: {count}개")
        print()
        
        # 2. Region 테이블 특화 쿼리
        print("2. Region 테이블 특화 쿼리")
        
        # 지역별 매장 수 (JOIN 사용)
        region_store_counts = session.query(
            Region.name.label('region_name'),
            func.count(Store.id).label('store_count')
        ).outerjoin(Store, Region.id == Store.region_id).group_by(Region.id, Region.name).all()
        
        print("지역별 매장 수:")
        for region_name, count in region_store_counts:
            print(f"  {region_name}: {count}개")
        print()
        
        # 3. Mood 테이블 특화 쿼리
        print("3. Mood 테이블 특화 쿼리")
        
        # 시/도별 기분 데이터
        si_counts = session.query(
            Mood.si,
            func.count(Mood.id).label('mood_count')
        ).group_by(Mood.si).all()
        
        print("시/도별 기분 데이터 수:")
        for si, count in si_counts:
            print(f"  {si}: {count}개")
        print()
        
        # 구/군별 기분 데이터
        gu_counts = session.query(
            Mood.gu,
            func.count(Mood.id).label('mood_count')
        ).filter(Mood.gu.isnot(None)).group_by(Mood.gu).all()
        
        print("구/군별 기분 데이터 수:")
        for gu, count in gu_counts:
            print(f"  {gu}: {count}개")
        print()
        
    except Exception as e:
        print(f"오류 발생: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    # 기본 ORM 쿼리 예제 실행
    orm_query_examples()
    
    # # 고급 ORM 쿼리 예제 실행
    # advanced_orm_queries()
    
    # # 테이블별 특화 쿼리 예제 실행
    # table_specific_queries()

