# 웹 프레임워크를 로드 
from flask import Flask, render_template, request

# render_template()함수
# 현재 경로에서 templates라는 하위 폴더에 있는 html문서를 되돌려주는 함수
# request
# 유저가 보낸 요청 메시지에 접근하기위한 기능

# Flask class를 생성
# 생성자 함수(__init__)에는 필수 인자값 1개 존재 : 파일의 이름 
# 파일의 이름 : __name__
app = Flask(__name__)

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
    if (input_id == 'test') and (input_pass == '1111'):
        return render_template('second.html', d = data)
    else:
        return '로그인 실패'

# 서버를 실행 
# run() 함수의 매개변수 
# debug 매개변수 : False(기본값)-> 서버를 강제적으로 재실행해야 수정된 코드가 반영, True -> 개발자 모드 파일이 수정됬을때 서버가 자동으로 재실행
# port 매개변수 : 5000(기본값), 포트 번호를 지정하는 매개변수
# host 매개변수 : 보안적인 매개변수, 웹서버에 접속할수 있는 ip를 지정
app.run(debug=True, host='0.0.0.0')