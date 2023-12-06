import pandas as pd
import nltk
# from transformers import BertTokenizer ##버트 토크나이저 임포트
from nltk.tokenize import word_tokenize, sent_tokenize ##문장 토크나이저
# from transformers import pipeline
import random
from nltk.tokenize import word_tokenize
import numpy as np
import itertools
from googletrans import Translator
import os

translator = Translator() ##구글 번역기 객체 생성
##사용할 본문

def shuffle2_gen(num, file_path, output_path):

    df = pd.read_csv(file_path)

    class_list = [] #문제유형
    main_list = [] #본문
    view1 = []  #보기1
    view2 = []  #보기2
    view3 = []  #보기3
    view4 = []  #보기4
    view5 = []  #보기5
    awr = []    #정답번호
    commentary = [] #해설

    for count in range(len(df[:num])):
        main = df['content'][count].strip()
        if len(main)>2500:
            continue
        else:
            try:
                main = df['content'][count].strip()
                sentences = sent_tokenize(df['content'][count])

                sentence_num_of_answer = random.randint(0,len(sentences)-1) ##정답 문장 순번
                answer_sentence = sentences.pop(sentence_num_of_answer) ##정답 문장


                options = []
                odd_list = [i for i in range(1,(len(sentences)*2)+1,2)]
                even_list = [i for i in range(0,(len(sentences)*2)+1,2)]
                random.shuffle(odd_list)
                random.shuffle(even_list)

                ##경우의 수 [1, ~~~~] , [2,~~~]


                if sentence_num_of_answer == len(sentences): ##마지막 문장일 경우
                    options.append(len(sentences)*2)
                else:
                    options.append(random.choice((sentence_num_of_answer*2, sentence_num_of_answer*2+1)))

                while len(options)!=5: 

                    if len(options)==0 :
                        options.append(random.randint(1,len(sentences)*2))
                    else:
                        if options[0]%2==1:
                            num = odd_list.pop()
                            if num not in options:
                                options.append(num)
                        else:
                            num = even_list.pop()
                            if num not in options:
                                options.append(num)
                            # print("넣었다")
                            # print(options)
                    if (0 in options) and (2 in options):
                        options.remove(2)

                    options = sorted(options) ##정렬


                if sentence_num_of_answer*2 in options :
                    answer_num = sentence_num_of_answer*2
                elif (sentence_num_of_answer*2)+1 in options:
                    answer_num = (sentence_num_of_answer*2)+1
                    
                            

                residual = []
                num_list = sorted([i for i in range(1,(len(sentences)*2)+1)], reverse=True)


                for i in sentences:
                    i = f'({num_list.pop()}) '+ i +f' ({num_list.pop()})'
                    residual.append(i)


                res = []
                for i in options: ##정답번호 추출
                    if i%2==0 :
                        if i ==0:
                            i_cop = residual[0].replace('(2)',"")
                            res.append(i_cop)
                        else:
                            i_cop = residual[(i//2)-1].replace((f'({i-1})'),'')
                            res.append(i_cop)
                    elif i%2==1 :
                        i_cop = residual[i//2].replace((f'({i+1})'),"")
                        res.append(i_cop)

                res = ''.join(res)
                for i in range(5):
                    res = res.replace(f'({options[i]})', f'({i+1})')

                if (sentence_num_of_answer*2 == answer_num) or (sentence_num_of_answer*2+1 == answer_num) and (answer_num in options):
                    print(answer_num, options)
                    print(sentence_num_of_answer)
                    print("정답: ", options.index(answer_num)+1)

                    outStr = translator.translate(main, dest='ko', src='en')

                    class_list.append('shuffle2')
                    main_list.append(main)
                    view1.append('1')
                    view2.append('2')
                    view3.append('3')
                    view4.append('4')
                    view5.append('5')
                    awr.append(str(options.index(answer_num)+1))
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
                    print(count, "번째 작업중")
            except:
                pass
            
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


