import pandas as pd 
import os 
from glob import glob

def read_df(_path, _encoding = 'utf-8'):
    # 해당하는 파일에서 확장자를 분리
    head, tail = os.path.splitext(_path)
    # head : ../csv/2021/202101_exepense_list
    # tail : .csv
    if tail == '.csv':
        df = pd.read_csv(_path, encoding= _encoding)
    elif tail == '.tsv':
        df = pd.read_csv(_path, encoding=_encoding, seq='\t')
    elif tail == '.json':
        df = pd.read_json(_path, encoding= _encoding)
    elif tail == 'xml':
        df = pd.read_xml(_path, encoding=_encoding)
    elif tail in ['.xlsx', '.xls']:
        df = pd.read_excel(_path)
    else:
        df = pd.DataFrame()
    return df

def data_load_add(_path, _end='csv'):
    file_list = os.listdir(_path)
    _path += '/'
    file_list_filter = [
        file for file in file_list if file.split('.')[-1] == _end
    ]
    result = pd.DataFrame()
    for file in file_list_filter:
        try:
            df = read_df(_path+file)
        except:
            try:
                df = read_df(_path+file, 'CP949')
            except:
                df = read_df(_path+file, 'EUC-KR')
        result = pd.concat([result, df])
    return result

def data_load(_path):
    # 입력받은 경로를 기준으로 파일의 목록 로드 
    # glob
    file_list = glob(_path+"/*.*")
    result = dict()
    for file in file_list:
        folder, name = os.path.split(file)
        head, tail = os.path.splitext(name)
        # print(head, '\t', tail)
        try : 
            df = read_df(file)
        except:
            try:
                df = read_df(file, 'CP949')
            except:
                df = read_df(file, 'EUC-KR')    
        # 로드한 데이터프레임의 길이가 0인 경우 : 전역변수 생성X
        # 전역변수에 head값을 사용한다. 
        # 모듈을 이용해서 전역 변수 생성이 불가능
        # 하나의 변수에 여러개의 데이터프레임을 저장 
        # 딕셔너리 데이터를 이용하여 key에는 파일의 이름 
        # value에는 데이터프레임을 대입 
        # 딕셔너리를 return 
        print(len(df))
        if len(df) != 0:
            # globals()[head] = df.copy()
            result[head] = df.copy()
            print(f"{head} key 생성")
            print(result.keys())
        else:
            print(f"{head} 파일은 데이터 파일이 아닙니다.")
    return result