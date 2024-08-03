import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

# 네이버 파이넨스 사이트에 요청
finance_url = 'https://finance.naver.com/'

# requests 라이브러리를 이용하여 요청 
finance_res = requests.get(finance_url)

# bs를 이용하여 데이터를 파싱 
finance_soup = bs(finance_res.text, 'html.parser')

# 태그의 개수가 1개인 것을 확인 
# 전체 html에서 div가 'section_sise_top'인 태그로 라인의 수를 줄인다. 
section_data = finance_soup.find('div', attrs = {
    'class' : 'section_sise_top'
})

# table 4개의 정보를 모두 저장 
tables = section_data.find_all('table')

# 반복문을 이용하여 tables데이터를 반복 실행
for table1 in tables:
    # table1에서 thead의 값들을 출력하여 DataFrame에 columns의 값을 사용
    thead_data = table1.find('thead')

    # thead_data에서 th태그를 모두 출력 
    th_list = thead_data.find_all('th')

    # th_list에서 문자들만 출력하여 새로운 리스트에 대입 
    # 리스트 형태의 데이터에서 각 원소들에 특정 행동을 하는 함수 -> map()
    cols = list(
        map(
            lambda x : x.get_text(), 
            th_list
        )
    )
    
    # table1에서 tbody부분 데이터를 출력
    tbody_data = table1.find('tbody')

    # tbody_data에서 tr들을 모두 출력 
    tr_list = tbody_data.find_all('tr')

    # 위의 value 작업들을 반복 실행 
    # tr_list의 개수만큼
    values = []
    for tr_data in tr_list:
        # tr_data에서 th태그, td태그를 출력
        th_list = tr_data.find_all('th')
        td_list = tr_data.find_all('td')
        value_data = th_list + td_list
        val = [ value.get_text().strip() for value in value_data ]
        values.append(val)

    # cols, values를 이용하여 DataFrame 생성
    df = pd.DataFrame(values, columns=cols)