import pymysql

class MyDB:
    # 생성자 함수 
    def __init__(
            self, 
            _host = 'localhost', 
            _port = 3306, 
            _user = 'root', 
            _password = '1234', 
            _db = 'ezen'):
        # 매개변수를 통해 입력된 인자값을 변수에 저장 
        self.host = _host
        self.port = _port
        self.user = _user
        self.password = _password
        self.db = _db
    # sql_query() 함수 생성
    def sql_query(self, _sql, *_values):
        # DB 서버와의 연결 
        _db = pymysql.connect(
            host = self.host, 
            port = self.port, 
            user = self.user, 
            password = self.password, 
            db = self.db
        )
        # 가상 공간 생성
        cursor = _db.cursor(pymysql.cursors.DictCursor)
        try:
            # 질의 
            cursor.execute(_sql, _values)
        except Exception as e:
            print('Error')
            _db.close()
            return e
        # 질의가 select문이라면?
        # if _sql.lower().split()[0] == 'select':
        # if _sql.strip().lower().startswith('select'):
        if _sql.strip().lower()[:6] == 'select':
            # 가상 공간에서 결과 값을 로드 
            result = cursor.fetchall()
        else:
            # DB 서버와 동기화 
            _db.commit()
            result = "Query OK"
        # DB 서버와의 연결을 종료
        _db.close()
        # 결과값을 되돌려준다. 
        return result
        