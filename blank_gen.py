from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup as bs
import csv
import pandas as pd
import numpy as np
import re
from selenium.webdriver.common.keys import Keys
import pyperclip
from selenium.webdriver.common.action_chains import ActionChains
from nltk.tokenize import word_tokenize, sent_tokenize, WhitespaceTokenizer, wordpunct_tokenize ##문장 토크나이저
import random 
from transformers import pipeline
import re
from googletrans import Translator
import logging
import os

logging.getLogger("transformers.modeling_utils").setLevel(logging.ERROR)


##POS_TAG (CLAW7 tagset) 품사 리스트
tag = 'APPGE,AT,AT1,BCL,CC,CCB,CS,CSA,CSN,CST,CSW,DA,DA1,DA2,DAR,DAT,DB,DB2,DD,DD1,DD2,DDQ,DDQGE,DDQV,EX,FO,FU,FW,GE,IF,II,IO,IW,JJ,JJR,JJT,JK,MC,MC1,MC2,MCGE,MCMC,MD,MF,ND1,NN,NN1,NN2,NNA,NNB,NNL1,NNL2,NNO,NNO2,NNT1,NNT2,NNU,NNU1,NNU2,NP,NP1,NP2,NPD1,NPD2,NPM1,NPM2,PN,PN1,PNQO,PNQS,PNQV,PNX1,PPGE,PPH1,PPHO1,PPHO2,PPHS1,PPHS2,PPIO1,PPIO2,PPIS1,PPIS2,PPX1,PPX2,PPY,RA,REX,RG,RGQ,RGQV,RGR,RGT,RL,RP,RPK,RR,RRQ,RRQV,RRR,RRT,RT,TO,UH,VB0,VBDR,VBDZ,VBG,VBI,VBM,VBN,VBR,VBZ,VD0,VDD,VDG,VDI,VDN,VDZ,VH0,VHD,VHG,VHI,VHN,VHZ,VM,VMK,VV0,VVD,VVG,VVGK,VVI,VVN,VVNK,VVZ,XX,ZZ1,ZZ2'
taglist = tag.split(',')

##각 품사의 뜻
raw = '''$possessive pronoun, pre-nominal (e.g. my, your, our)$article (e.g. the, no)$singular article (e.g. a, an, every)$before-clause marker (e.g. in order (that),in order (to))$coordinating conjunction (e.g. and, or)$adversative coordinating conjunction ( but)$subordinating conjunction (e.g. if, because, unless, so, for)$as (as conjunction)$than (as conjunction)$that (as conjunction)$whether (as conjunction)$after-determiner or post-determiner capable of pronominal function (e.g. such, former, same)$singular after-determiner (e.g. little, much)$plural after-determiner (e.g. few, several, many)$comparative after-determiner (e.g. more, less, fewer)$superlative after-determiner (e.g. most, least, fewest)$before determiner or pre-determiner capable of pronominal function (all, half)$plural before-determiner ( both)$determiner (capable of pronominal function) (e.g any, some)$singular determiner (e.g. this, that, another)$plural determiner ( these,those)$wh-determiner (which, what)$wh-determiner, genitive (whose)$wh-ever determiner, (whichever, whatever)$existential there$formula$unclassified word$foreign word$germanic genitive marker - (' or's)$for (as preposition)$general preposition$of (as preposition)$with, without (as prepositions)$general adjective$general comparative adjective (e.g. older, better, stronger)$general superlative adjective (e.g. oldest, best, strongest)$catenative adjective (able in be able to, willing in be willing to)$cardinal number,neutral for number (two, three..)$singular cardinal number (one)$plural cardinal number (e.g. sixes, sevens)$genitive cardinal number, neutral for number (two's, 100's)$hyphenated number (40-50, 1770-1827)$ordinal number (e.g. first, second, next, last)$fraction,neutral for number (e.g. quarters, two-thirds)$singular noun of direction (e.g. north, southeast)$common noun, neutral for number (e.g. sheep, cod, headquarters)$singular common noun (e.g. book, girl)$plural common noun (e.g. books, girls)$following noun of title (e.g. M.A.)$preceding noun of title (e.g. Mr., Prof.)$singular locative noun (e.g. Island, Street)$plural locative noun (e.g. Islands, Streets)$numeral noun, neutral for number (e.g. dozen, hundred)$numeral noun, plural (e.g. hundreds, thousands)$temporal noun, singular (e.g. day, week, year)$temporal noun, plural (e.g. days, weeks, years)$unit of measurement, neutral for number (e.g. in, cc)$singular unit of measurement (e.g. inch, centimetre)$plural unit of measurement (e.g. ins., feet)$proper noun, neutral for number (e.g. IBM, Andes)$singular proper noun (e.g. London, Jane, Frederick)$plural proper noun (e.g. Browns, Reagans, Koreas)$singular weekday noun (e.g. Sunday)$plural weekday noun (e.g. Sundays)$singular month noun (e.g. October)$plural month noun (e.g. Octobers)$indefinite pronoun, neutral for number (none)$indefinite pronoun, singular (e.g. anyone, everything, nobody, one)$objective wh-pronoun (whom)$subjective wh-pronoun (who)$wh-ever pronoun (whoever)$reflexive indefinite pronoun (oneself)$nominal possessive personal pronoun (e.g. mine, yours)$3rd person sing. neuter personal pronoun (it)$3rd person sing. objective personal pronoun (him, her)$3rd person plural objective personal pronoun (them)$3rd person sing. subjective personal pronoun (he, she)$3rd person plural subjective personal pronoun (they)$1st person sing. objective personal pronoun (me)$1st person plural objective personal pronoun (us)$1st person sing. subjective personal pronoun (I)$1st person plural subjective personal pronoun (we)$singular reflexive personal pronoun (e.g. yourself, itself)$plural reflexive personal pronoun (e.g. yourselves, themselves)$2nd person personal pronoun (you)$adverb, after nominal head (e.g. else, galore)$adverb introducing appositional constructions (namely, e.g.)$degree adverb (very, so, too)$wh- degree adverb (how)$wh-ever degree adverb (however)$comparative degree adverb (more, less)$superlative degree adverb (most, least)$locative adverb (e.g. alongside, forward)$prep. adverb, particle (e.g about, in)$prep. adv., catenative (about in be about to)$general adverb$wh- general adverb (where, when, why, how)$wh-ever general adverb (wherever, whenever)$comparative general adverb (e.g. better, longer)$superlative general adverb (e.g. best, longest)$quasi-nominal adverb of time (e.g. now, tomorrow)$infinitive marker (to)$interjection (e.g. oh, yes, um)$be, base form (finite i.e. imperative, subjunctive)$were$was$being$be, infinitive (To be or not... It will be ..)$am$been$are$is$do, base form (finite)$did$doing$do, infinitive (I may do... To do...)$done$does$have, base form (finite)$had (past tense)$having$have, infinitive$had (past participle)$has$modal auxiliary (can, will, would, etc.)$modal catenative (ought, used)$base form of lexical verb (e.g. give, work)$past tense of lexical verb (e.g. gave, worked)$-ing participle of lexical verb (e.g. giving, working)$-ing participle catenative (going in be going to)$infinitive (e.g. to give... It will work...)$past participle of lexical verb (e.g. given, worked)$past participle catenative (e.g. bound in be bound to)$-s form of lexical verb (e.g. gives, works)$not, n't$singular letter of the alphabet (e.g. A,b)$plural letter of the alphabet (e.g. A's, b's)$'''
raw_list = raw.split('$') 
##품사에 대한 정보
tag_comment = {} ##품사 : 품사 정보 묶은 딕셔너리
for a,b in zip(taglist,raw_list):
    tag_comment[a]=b



def blank_gen(num, file_path,output_path):

    df = pd.read_csv(file_path) ## 사용 데이터셋
     

    translator = Translator() ##번역기 객체 생성


    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

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
                url = 'https://ucrel-api.lancaster.ac.uk/claws/free.html'
                driver.get(url)
                time.sleep(3)


                c7_select = driver.find_element(By.CSS_SELECTOR, 'body > div.container > form > input[type=radio]:nth-child(5)').click()
                time.sleep(1)

                text_select = driver.find_element(By.CSS_SELECTOR, 'body > div.container > form > textarea').click()
                ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()   
                time.sleep(1)

                example = df['content'][count]
                
                pyperclip.copy(example)
                ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()


                translate_start = driver.find_element(By.CSS_SELECTOR, 'body > div.container > form > input[type=SUBMIT]:nth-child(15)').click()

                translate_sentence = driver.find_element(By.CSS_SELECTOR, 'body > div.container > pre')
                translate_sentence = translate_sentence.text
                # else :
                #     translate_sentence = translate_sentence[59:].split('._.')[:-2]

                # print(translate_sentence)
                tmp = {}
                choice_list=[]
                answers = []

                replaced_content=[]
                answer=[]
                sentence_list = sent_tokenize(example)

                lis = []
                token_list = []
                for cnt, i in enumerate(translate_sentence.split('._.')):
                    i = i.strip()
                    i = i.replace('\n', "")
                    pos_tuple = i.split(' ')
                    sentence_num_list = []
                    for j in pos_tuple:
                        j = j.split('_') 
                        if j[-1] in taglist:
                            a,b = j
                            sentence_num_list.append((a,b,cnt))
                            token_list.append((a,b,cnt))
                    if len(sentence_num_list) :
                        lis.append(sentence_num_list)


                for j in range(len(lis)):
                    num_of_sentence = random.randint(0, len(lis)-1) ## 문장 번호 randint 는 (start,end) end 이하의 숫자가 나오기 때문에 -1
                    num_of_word = random.randint(0, len(lis[num_of_sentence])-1) ## 단어 번호
                    chosen = lis[num_of_sentence][num_of_word] ## 바꿀 위치 선택
                    if chosen[1] not in ['JJ','JJR','JJT','JK','ND1','MF','NN','NN1','NN2','NP','NP1','NP2','PN','PN1','VV0','VVD','VVG','VVGK','VVI','VVN','VVNK','VVZ']:
                        continue    
                    else:
                        break

                chosen_index = sentence_list[chosen[2]].index(chosen[0]) ## 단어 위치(시작점)
                chosen_word = sentence_list[chosen[2]][chosen_index:chosen_index+len(chosen[0])] ## 슬라이싱을 이용한 단어 추출

                replaced_sentence = sentence_list[chosen[2]].replace(chosen_word,'_____',1)
                sentence_list[chosen[2]]=replaced_sentence

                content = ''.join(sentence_list)
                content = re.sub(r'[\']+', '\u2019',content) ##____ 변환된 본문 
                answer.append(chosen[0]) ##정답

                fill_sentence = sentence_list[chosen[2]].replace('_____','[MASK]')

                unmasker = pipeline('fill-mask', model='bert-base-cased', top_k = 10, device=0)

                puntuation_list = ['.',',','"','\\','-','?',':','!',';',"'"] ## 구두점 리스트

                exam = []
                for i in unmasker(fill_sentence):
                    if (len(i['token_str'])>1) and (i['token_str'].lower()!=answer[0]) and (i['token_str']!=answer[0]) and ('#' not in i['token_str']) and (i['token_str'] not in exam) and (i['token_str'].lower() not in exam and i['token_str'] not in puntuation_list): ##답이랑 같은 경우 제외
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
                        for i in range(len(token_list)): ## 토큰 리스트의 길이만큼 반복
                            sub = random.randint(0,len(token_list)-1) ##랜덤 인덱스 추출
                            sub = token_list[i][0] ## 인덱스를 바탕으로 단어 추출
                            if token_list[i][2] == chosen[2]: 
                                if (sub != answer) and (len(sub)>1) and ('#' not in sub) and (sub not in answer_list) and (sub.lower() not in answer_list) :
                                    answer.append(sub)
                                    break
                                else:
                                    continue
                                
                        k_num -=1
                        answer_list = answer_list + answer


                random.shuffle(answer_list)   ## 정답 선지 랜덤으로 섞어줌
                if content and answer_list[0] and answer_list[1] and answer_list[2] and answer_list[3] and answer_list[4] and answer_list.index(answer[0])+1 and translator.translate(example, src = 'en', dest= 'ko').text:
                    class_list.append('blank')
                    main_list.append(content)
                    view1.append(answer_list[0])              
                    view2.append(answer_list[1])     
                    view3.append(answer_list[2])    
                    view4.append(answer_list[3])  
                    view5.append(answer_list[4])  
                    awr.append(answer_list.index(answer[0])+1)
                    commentary.append(f"""본문 :  {translator.translate(example, src = 'en', dest= 'ko').text} \n 
                            해당 문장 : {sentence_list[num_of_sentence]} \n
                            1번 : {answer_list[0]} {translator.translate(answer_list[0], src = 'en', dest= 'ko').text} \n
                            2번 : {answer_list[1]} {translator.translate(answer_list[1], src = 'en', dest= 'ko').text} \n
                            3번 : {answer_list[2]} {translator.translate(answer_list[2], src = 'en', dest= 'ko').text} \n
                            4번 : {answer_list[3]} {translator.translate(answer_list[3], src = 'en', dest= 'ko').text} \n
                            5번 : {answer_list[4]} {translator.translate(answer_list[4], src = 'en', dest= 'ko').text} \n
                            """)
                else:
                    pass 


                # result = {"Q{}".format(count+1) :
                #         {"main": content,
                #         "view1": answer_list[0],
                #         "view2": answer_list[1],
                #         "view3": answer_list[2],
                #         "view4": answer_list[3],
                #         "view5": answer_list[4],
                #         "answer": answer_list.index(answer[0])+1,
                #         "commentary": f"""본문 :  {translator.translate(example, src = 'en', dest= 'ko').text} \n 
                #         해당 문장 : {sentence_list[num_of_sentence]} \n
                #         1번 : {answer_list[0]} {translator.translate(answer_list[0], src = 'en', dest= 'ko').text} \n
                #         2번 : {answer_list[1]} {translator.translate(answer_list[1], src = 'en', dest= 'ko').text} \n
                #         3번 : {answer_list[2]} {translator.translate(answer_list[2], src = 'en', dest= 'ko').text} \n
                #         4번 : {answer_list[3]} {translator.translate(answer_list[3], src = 'en', dest= 'ko').text} \n
                #         5번 : {answer_list[4]} {translator.translate(answer_list[4], src = 'en', dest= 'ko').text} \n
                #         """}}
                # js_list.append(result)
                print(count,'번 작업 끝')
            except:
                continue
        
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




blank_gen(100,r"C:\Users\user\Desktop\project9\full1500.csv", 'd:/test3.csv')