import pandas as pd
import nltk
from transformers import BertTokenizer ##버트 토크나이저 임포트
from nltk.tokenize import word_tokenize, sent_tokenize ##문장 토크나이저
from transformers import pipeline
import random
from nltk.tokenize import word_tokenize
import numpy as np
import itertools
import googletrans
import os

translator = googletrans.Translator() ##구글 번역기 객체 생성




def shuffle1_gen(num, file_path, output_path):

    df = pd.read_csv(file_path) ##사용 데이터

    class_list = [] #문제유형
    main_list = [] #본문
    view1 = []  #보기1
    view2 = []  #보기2
    view3 = []  #보기3
    view4 = []  #보기4
    view5 = []  #보기5
    awr = []    #정답번호
    commentary = [] #해설

    # js_list=[]
    for count in range(len(df[:num])):
        if len(df['content'][count])>2500:
            continue
        else:
            try:
                # tokenized_sentence = word_tokenize(df['content'][count])
                # tagged = nltk.pos_tag(tokenized_sentence)


                # word = ""
                # for i in tagged:
                #     word += " "+i[0]
                # word
                sentences = sent_tokenize(df['content'][count])

                first_sentence = sentences[0] ## 첫 문장 (기준 글)
                residual = sentences[1:] ## 나머지 글

                x = np.linspace(0,len(residual),4) ##residual을 3등분
                x = x.astype(int)

                choice = random.sample(['a','b','c'], k=3)  ##순서 랜덤으로 샘플링
                answer = tuple(choice) ##정답 순서


                dic = {}
                dic[choice[0]] = residual[x[0]:x[1]]
                dic[choice[1]] = residual[x[1]:x[2]]
                dic[choice[2]]= residual[x[2]:x[3]]


                contents = ''
                dic_keys = ['a','b','c']
                for i in dic_keys:
                    contents = contents+'('+i+') '
                    for j in dic[i]:
                        contents += j+' '
                    contents+='\n'

                answers = ['a','b','c']

                result = itertools.permutations(answers) ##순열로 뽑기
                result = list(result)
                random.shuffle(result) ## 셔플해줌

                ##보기 만들기
                answer_list = []
                answer_list.append(answer)

                for i in result:
                    if i == answer :
                        pass
                    else:
                        answer_list.append(i)
                        if len(answer_list) == 5: ##5지선다형
                            break

                random.shuffle(answer_list) ##섞어줌
                #answer_list.index(answer) ##정답 위치

                main = first_sentence +'\n'+ contents ##본문



                inStr = main[:-1]

                outStr = translator.translate(inStr, dest='ko', src='en')

                class_list.append('shuffle1')
                main_list.append(main[:-1])
                view1.append('-'.join(answer_list[0]))
                view2.append('-'.join(answer_list[1]))
                view3.append('-'.join(answer_list[2]))
                view4.append('-'.join(answer_list[3]))
                view5.append('-'.join(answer_list[4]))
                awr.append(answer_list.index(answer)+1)
                commentary.append(outStr.text)
                
                # result = {"Q{}".format(count+1) :
                #     {"main" : main[:-1], ##개행문자 제거
                #     "view1": '-'.join(answer_list[0]),
                #     "view2": '-'.join(answer_list[1]),
                #     "view3": '-'.join(answer_list[2]),
                #     "view4": '-'.join(answer_list[3]),
                #     "view5": '-'.join(answer_list[4]),
                #     "answer": answer_list.index(answer)+1,
                #     "commentary": outStr.text}}
            except:
                continue
            print(count, '번째 작업 중')
        
    js_dict = {}
    js_dict['class'] = class_list
    js_dict['main'] = main_list
    js_dict['view1'] = view1
    js_dict['view2'] = view2
    js_dict['view3'] = view3
    js_dict['view4'] = view4
    js_dict['view5'] = view5
    js_dict['answer'] = awr
    js_dict['commentary'] = commentary

    tmp = pd.DataFrame.from_dict(js_dict)

    
    ##저장
    if not os.path.exists(output_path):
        tmp.to_csv(output_path, index=False, mode='w', encoding='utf-8-sig')
    else:
        tmp.to_csv(output_path, index=False, mode='a', encoding='utf-8-sig', header=False)



