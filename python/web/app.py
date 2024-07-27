# 웹 프레임워크를 로드 
from flask import Flask, render_template, request, redirect
# custom_db 모듈을 로드 
import custom_db as c_db

# render_template()함수
# 현재 경로에서 templates라는 하위 폴더에 있는 html문서를 되돌려주는 함수
# request
# 유저가 보낸 요청 메시지에 접근하기위한 기능

# Flask class를 생성
# 생성자 함수(__init__)에는 필수 인자값 1개 존재 : 파일의 이름 
# 파일의 이름 : __name__
app = Flask(__name__)

# 외부의 DB 서버와 연결하는 class 생성
db = c_db.MyDB(
    _host = '172.16.106.1', 
    _port = 3306, 
    _user = 'ezen', 
    _password = '1234', 
    _db = 'ezen'
)
# 내부의 DB 서버와의 연결하는 class 생성
local_db = c_db.MyDB()


# api를 생성 
# 특정 주소로 요청이 들어왔을때 어떠한 데이터를 응답 메시지로 보내줄지를 지정 

# 웹서버의 기본(루트) 주소 : 127.0.0.1:5000

# 네이게이션 함수 
# '/' 주소로 요청을 했을때 바로 아래의 함수를 실행 -> 함수와 연결
@app.route('/')
def index():
    # return 'Hello World'
    # 요청이 들어왔을때 데이터가 아닌 html문서를 되돌려준다. 
    return render_template('index.html')

# api 생성
# 127.0.0.1:5000/second 요청을 보냈을때
@app.route('/second')
def second():
    # return 'Second Page'
    # 유저가 보낸 데이터(request에 존재)를 변수에 저장 & 확인 
    # get 방식에서는 유저가 보낸 데이터가 request안에 args에 데이터가 존재
    # data -> { '_id' : 'test', '_pass' : '1111' }
    print(request.args)
    input_id = request.args['_id']
    input_pass = request.args['_pass']
    data = "이젠아카데미"
    print(f"유저가 입력한 아이디는 {input_id}, 비밀번호는 {input_pass}")
    # 특정 아이디와 비밀번호인 경우에만 second.html를 보여준다. 
    # if (input_id == 'test') and (input_pass == '1111'):
    #     return render_template('second.html', d = data)
    # else:
    #     return '로그인 실패'
    # DB 서버에 유저가 입력한 id와 password를 비교
    login_query = """
        select 
        * 
        from 
        `user`
        where 
        `id` = %s 
        and 
        `password` = %s
    """
    # local에 있는 DB에 확인 
    db_result = local_db.sql_query(login_query, input_id, input_pass)
    # 로그인이 성공하는 조건? -> db_result에 데이터가 존재(길이가 1)
    # if len(db_result) == 1:
    if db_result:
        # second.html과 로그인을 한 유저의 이름
        # [{'id' : 'test', password : '1234', name : 'kim'}]
        user_name = db_result[0]['name']
        return render_template('second.html', d=user_name)
    else:
        # 로그인 화면으로 되돌아간다. 
        # 127.0.0.1:5000/ 주소를 재요청한다. 
        # return render_template('index.html')
        return redirect('/')

# /login api 생성(post 방식)
@app.route('/login', methods=['post'])
def login():
    # 유저가 보낸 데이터를 변수에 저장 
    # post로 보낸 데이터는 request 안에 form에 데이터가 존재
    input_id  = request.form['_id']
    input_pass = request.form['_pass']
    print(f"유저가 입력한 id는 {input_id}이고 password는 {input_pass}")
    # DB 서버에서 id, pass를 확인 
    # 외부의 DB 서버에 접속
    login_query = """
        select * from `user`
        where `id` = %s and `password` = %s
    """
    db_result = db.sql_query(login_query, input_id, input_pass)
    if db_result:
        # 외부의 데이터 파일을 로드하여 보내는 형태
        data_load = """
            select * from `drinks`
        """
        result = db.sql_query(data_load)
        return result
    else:
        return 'id 혹은 password가 맞지 않습니다.'


# 서버를 실행 
# run() 함수의 매개변수 
# debug 매개변수 : False(기본값)-> 서버를 강제적으로 재실행해야 수정된 코드가 반영, True -> 개발자 모드 파일이 수정됬을때 서버가 자동으로 재실행
# port 매개변수 : 5000(기본값), 포트 번호를 지정하는 매개변수
# host 매개변수 : 보안적인 매개변수, 웹서버에 접속할수 있는 ip를 지정
app.run(debug=True, host='0.0.0.0')