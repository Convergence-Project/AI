from pymongo import MongoClient
import sys, os
import json
import re
import pandas as pd
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

client = MongoClient('127.0.0.1', 27017)# 127.0.0.1 => 몽고디비 IP / 27017 => 포트번호

db = client.English_Q_A #생성할 DB 이름
db_q_a = db.q_a_db #생성하고자 하는 컬렉션 이름
db_bert = db.bert_db
db_llama2 = db.llama2_db
db_gpt = db.gpt_db

global_blank_start = 0
global_blank_finish = 10

global_shuffle1_start = 0
global_shuffle1_finish = 10

global_shuffle2_start = 0
global_shuffle2_finish = 10

global_title_start = 0
global_title_finish = 10

global_topic_start = 0
global_topic_finish = 10

#데이터 삭제
def delete_db(q_a):
    db_q_a.delete_one({"class": q_a})  # 가장 먼저 검색되는 것만 삭제
    print(q_a+" 삭제")
# for _ in range(1,27):
#     delete_db("subject")

#데이터 수정 및 추가하기
def change_db(q_a):
    db_q_a.update_one({"name": "홍길동"}, {'$set': {"bio": "한국인입니다."}}, upsert=True)#가장 먼저 있는 거 수정, upset-> 없으면 추가
    print(q_a+" 수정")


#데이터 불러오기
def load_db(class_num):
    global global_blank_start
    global global_blank_finish
    global global_shuffle1_start
    global global_shuffle1_finish
    global global_shuffle2_start
    global global_shuffle2_finish
    global global_title_start
    global global_title_finish
    global global_topic_start
    global global_topic_finish

    allData = db_q_a.find({"class":class_num}, {"_id": 0})
    result = []

    

    if class_num == 'blank':
        print(global_blank_start, global_blank_finish)
        for temp in allData[global_blank_start:global_blank_finish]:
            result.append(temp)
        global_blank_start += 10
        global_blank_finish += 10
        print(global_blank_start, global_blank_finish)
    elif class_num == 'shuffle1':
        print(global_shuffle1_start, global_shuffle1_finish)
        for temp in allData[global_shuffle1_start:global_shuffle1_finish]:
            result.append(temp)
        global_shuffle1_start += 10
        global_shuffle1_finish += 10
        print(global_shuffle1_start, global_shuffle1_finish)
    elif class_num == 'shuffle2':
        print(global_shuffle2_start, global_shuffle2_finish)
        for temp in allData[global_shuffle2_start:global_shuffle2_finish]:
            result.append(temp)
        global_shuffle2_start += 10
        global_shuffle2_finish += 10
        print(global_shuffle2_start, global_shuffle2_finish)
    elif class_num == 'title':
        print(global_title_start, global_title_finish)
        for temp in allData[global_title_start:global_title_finish]:
            result.append(temp)
        global_title_start += 10
        global_title_finish += 10
        print(global_title_start, global_title_finish)
    elif class_num == 'topic':
        print(global_topic_start, global_topic_finish)
        for temp in allData[global_topic_start:global_topic_finish]:
            result.append(temp)
        global_topic_start += 10
        global_topic_finish += 10
        print(global_topic_start, global_topic_finish)

    

    json_results = json.dumps(result, default=str, ensure_ascii=False)

    return json_results


#데이터 입력
def insert_db(q_a):
    document = q_a
    #도큐먼트 하나 넣기
    db_q_a.insert_one(document)
    print("생성된 문제 - DB 입력")

#데이터 입력
def insert_many_db(q_a):
    document = q_a
    #도큐먼트 하나 넣기
    db_q_a.insert_many(document)
    print("생성된 문제 - DB 입력")

#flask run --host=0.0.0.0 --port=5000


#csv db 넣기
def csv_insert_db(document):
    # CSV 파일 읽기
    csv_file = './csv/final/'+document+'.csv'  # CSV 파일 경로
    data = pd.read_csv(csv_file, encoding='utf-8')
    
    # data.to_csv(csv_file, encoding='utf-8', index=None)
    # data = pd.read_csv(csv_file)
    

    # 데이터 삽입
    data_dict = data.to_dict(orient='records')  # 데이터프레임을 딕셔너리 리스트로 변환
    insert_many_db(data_dict)  # 데이터 삽입


# csv_insert_db('/last/question')