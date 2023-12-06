import pandas as pd
from transformers import BertTokenizer ##버트 토크나이저 임포트
from nltk.tokenize import word_tokenize, sent_tokenize ##문장 토크나이저
from transformers import pipeline
import random
import logging


df = pd.read_csv(r"D:/9_project/generate/csv/full1500.csv")
def send_blank():

    tokenizer = BertTokenizer.from_pretrained("bert-base-cased")

    logging.getLogger("transformers.modeling_utils").setLevel(logging.ERROR)
    js_dict = {}
    tmp = {}
    choice_list=[]
    answers = []
    js_list=[]
    replaced_content=[]
    for count in range(len(df[:10])):
        passage = df['content'][count]
        tokens = tokenizer.tokenize(passage) ##버트 토크나이저를 이용한 인코딩
        if len(tokens) > 512:
            tokens = tokens[:512]
        #ids = tokenizer.convert_tokens_to_ids(tokens) ## 정수인코딩
    ### 빈칸 만들기 

        for j in range(0,len(tokens)):
            num = random.randrange(0,len(tokens)) ##난수 생성
            if len(tokens[num])>2 and ('#' not in tokens[num]) and (tokens[num]!='the') and (tokens[num]!='The'): ##불용어 처리
                break
        lis = [] ##본문 토큰 리스트
        answer = [] ##추출한 빈칸
        for cnt, i in enumerate(tokens):
            if cnt == num and ("#" not in i) and (len(i)>2) and (tokens[num]!='the' and (tokens[num]!='The')) :
                lis.append("_____")
                answer.append(i)
            else:
                lis.append(i)

        word = ""
        for i in lis:
            if word.endswith('-'):
                if '##' in i:
                    word+=i.replace('##','')
                else :
                    word+=i
            elif word.endswith('”'):
                if '##' in i:
                    word+=i.replace('##','')
                else :
                    word+=i
            elif word.endswith('“'):
                if '##' in i:
                    word+=i.replace('##','')
                else :
                    word+=i
            # if word.endswith('’'):
            #     if '##' in i:
            #         word+=i.replace('##','')
            #     else :
            #         word+=i

                    
            else:
                if '##' in i:
                    word+=i.replace('##','')
                elif i in ['-', '.',',',"'",'"','’']:
                    word+=i
                else:
                    word+=" "+i

        ###문장단위 토크나이징            


        sentences = sent_tokenize(word)

        ## 빈칸이 속한 문장 위치 파악
        for cnt,a in enumerate(sentences):
            try:
                loc = a.index('_____') ##문자열 인덱스
                num_loc = cnt ##문장 인덱스
            except:
                pass
        new_sen = sentences[num_loc].replace('_____','[MASK]')

        unmasker = pipeline('fill-mask', model='bert-base-cased', top_k = 30)

        exam = []
        for i in unmasker(new_sen):
            if (len(i['token_str'])>3) and (i['token_str']!=answer[0]) and ('#' not in i['token_str']) and (i['token_str'] not in exam) and (i['token_str'].lower() not in exam): ##답이랑 같거나 단어 길이가 2보다 작은 경우 제외
                exam.append(i['token_str'])
            else:
                pass

        k_num =4
        answer_list = []
        while len(answer_list) < 5:
            try:
                new_exam = random.sample(exam, k=k_num)
                answer_list = new_exam+answer
            except:
                for i in range(len(tokens)):
                    sub = random.choice(tokens)
                    if (sub != answer) and (len(sub)>3) and ('#' not in sub) and (sub not in answer_list) and (sub.lower() not in answer_list) :
                        answer.append(sub)
                        break
                    else:
                        continue
                        
                k_num -=1
                answer_list = answer_list + answer


        random.shuffle(answer_list)
        # print('answerlist :', answer_list)
        # print('answer:' ,answer)
        # print('num::', answer_list.index(answer[0])+1)

        answers.append(answer_list.index(answer[0])+1)
        choice_list.append(answer_list)
        replaced_content.append(word)
        print(count, "번째 작업중")
        



        result = {"Q{}".format(count+1) :
            {"main": word,
            "view1": answer_list[0],
            "view2": answer_list[1],
            "view3": answer_list[2],
            "view4": answer_list[3],
            "view5": answer_list[4],
            "answer": answer_list.index(answer[0])+1}}
        js_list.append(result)

    js_dict['blank'] = js_list

    return js_dict


#     if count == 1000 :
#         tmp['replaced_content'] = replaced_content
#         tmp['choice'] = choice_list
#         tmp['answer'] = answers
#         tmp = pd.DataFrame.from_dict(tmp)
#         tmp.to_csv(f'C:/Users/user/Desktop/project9/dataset_merge{count}.csv', index=False, encoding='utf-8-sig')

# tmp['replaced_content'] = replaced_content
# tmp['choice'] = choice_list
# tmp['answer'] = answers
# tmp = pd.DataFrame.from_dict(tmp)
# tmp.to_csv(f'C:/Users/user/Desktop/project9/dataset_merge{count}.csv', index=False, encoding='utf-8-sig')