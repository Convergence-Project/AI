from transformers import BertTokenizer ##버트 토크나이저 임포트
import random
from nltk.tokenize import word_tokenize, sent_tokenize
from transformers import pipeline

def send_generate_black():
    ##사용할 본문
    passage = 'Invasions of natural communities by non-indigenous species are currently rated as one of the most important global-scale environmental problems. The loss of biodiversity has generated concern over the consequences for ecosystem functioning and thus understanding the relationship between both has become a major focus in ecological research during the last two decades. The “biodiversity-invasibility hypothesis” by Elton suggests that high diversity increases the competitive environment of communities and makes them more difficult to invade. Numerous biodiversity experiments have been conducted since Elton’s time and several mechanisms have been proposed to explain the often observed negative relationship between diversity and invasibility. Beside the decreased chance of empty ecological niches but the increased probability of competitors that prevent invasion success, diverse communities are assumed to use resources more completely and, therefore, limit the ability of invaders to establish. Further, more diverse communities are believed to be more stable because they use a broader range of niches than species-poor communities.'

    tokenizer = BertTokenizer.from_pretrained("bert-base-cased")
    tokens = tokenizer.tokenize(passage) ##버트 토크나이저를 이용한 인코딩
    ids = tokenizer.convert_tokens_to_ids(tokens) ## 정수인코딩

    for j in range(0,len(tokens)):
        num = random.randrange(0,len(tokens)) ##난수 생성
        if len(tokens[num])>2:
            break
    lis = [] ##본문 토큰 리스트
    answer = [] ##추출한 빈칸
    for cnt, i in enumerate(tokens):
        if cnt == num:
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


    sentences = sent_tokenize(word)

    for cnt,a in enumerate(sentences):
        try:
            loc = a.index('_____') ##문자열 인덱스
            num_loc = cnt ##문장 인덱스
        except:
            pass

    sentences[num_loc][loc:loc+5]

    sentences[num_loc]

    new_sen = sentences[num_loc].replace('_____','[MASK]')

    unmasker = pipeline('fill-mask', model='bert-base-cased', top_k = 20)

    exam = []
    for i in unmasker(new_sen):
        if len(i['token_str'])<3 or i['token_str']==answer[0]:
            pass
        else:
            exam.append(i['token_str'])

    new_exam = random.sample(exam, k=4)

    answer_list = new_exam+answer

    random.shuffle(answer_list)

    result = { "main" : word,
            "view1": answer_list[0],
            "view2": answer_list[1],
            "view3": answer_list[2],
            "view4": answer_list[3],
            "view5": answer_list[4],
            "answer": answer_list.index(answer[0])+1}
    
    return result
