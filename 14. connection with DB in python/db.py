import pymysql # pip install pymysql 설치

# python 예제 코드 실행 전 필요한 DB 작업
# 1. 설치되어있는 mysql에 접속
# > mysql -u root -p
# 2. root 계정 비밀번호 1234로 설정
# m> ALTER USER 'root'@'localhost' IDENTIFIED BY '1234';
# 3. testdb 데이터 베이스 생성.
# m> CREATE DATABASE testdb;
# m> USE testdb;
# 4. testtable 생성 sql
# m>create table testtable ( test_id int NOT NULL, test_value varchar(10) NULL, PRIMARY KEY(test_id));
# 5. 테스트용 데이터 삽입 sql
# m>insert into testtable (test_id, test_value) values(1, 'test data');

conn = pymysql.connect(
    user='root',        # db 계정 아이디
    password='1234',    # root 계정 비밀번호
    host='127.0.0.1',   # ip주소
    database='testdb',  # Database name
    port=3306,          # port는 최초 설치 시 입력한 값(기본값은 3306)
    charset='utf8'
)
#print(conn)
# db select, insert, update, delete 작업 객체
cursor = conn.cursor()
# 실행할 select 문 구성
sql = "SELECT * FROM testtable where test_id = 1"
# cursor 객체를 이용해서 수행한다.
cursor.execute(sql)
# select 된 결과 셋 얻어오기
resultList = cursor.fetchall()  # tuple 이 들어있는 list
#print(len(resultList))
print(resultList) # db에서 가져온 값
# DB 에 저장된 rows 출력해보기

for result in resultList:
    test_id = result[0]      # test_id
    test_value = result[1]   # test_value
    info = "test_id:{}, test_value :{}, ".format(test_id, test_value)
    print(info)


