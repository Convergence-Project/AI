import os
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from googletrans import Translator
import time
import pandas as pd
# from langchain import ConversationChain
# from langchain.schema import (
#     AIMessage,
#     HumanMessage,
#     SystemMessage
# )

OPENAI_API_KEY = ""

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

chat = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.2)

translator = Translator()


def title():
    result = ''
    prompt = PromptTemplate(
        input_variables=["step", "json_schema"],
        template="""You are a member of the English Language Arts section committee for the South Korean National Assessment.
        You need to create a question to find the title of the passage below.
        We've provided step-by-step instructions to help you create the question.
        Only enter answers for steps 1, 2, 3, and 4.
    
        {step}
    
        Finally, respond with the following JSON schema:
    
        {json_schema}
        """
    )

    chain = LLMChain(llm=chat, prompt=prompt)

    result = chain.run(step="""Step 1: In this step, you must enter a sentence of at least 800 characters that is the source of the question you want to find the title for.
    Step 2: Create a multiple choice question to find the title based on the sentence in step 1 with 5 options and 1 correct answer.
    Step 3: In step 3, enter the correct answers one by one (for example, 1, 2, 3, 4, 5).
    """,
    json_schema ="""{
        "class": "title",
        "main" : "{step 1}",
        "view1": "{step 2[0]}",
        "view2": "{step 2[1]}",
        "view3": "{step 2[2]}",
        "view4": "{step 2[3]}",
        "view5": "{step 2[4]}",
        "answer": "{step 3}"
    }
    """)

    result = eval(result)

    result2 = translator.translate(result['main'], src='en', dest='ko')
    result['commentary'] = result2.text 



    return result

def topic():
    result = ''
    prompt = PromptTemplate(
        input_variables=["step", "json_schema"],
        template="""You are a member of the English Language Arts section committee for the South Korean National Assessment. You need to create a question that finds the topic of the passage below.
        I'll give you step-by-step instructions to help you get the right answer.
        Please provide only the answers to step 1, step 2, step 3, and step 4.

        {step}

        Finally, respond with the following JSON schema:

        {json_schema}
        """
    )

    chain = LLMChain(llm=chat, prompt=prompt)

    result = chain.run(step="""Step 1: In this step, you need to generate a sentence of at least 800 characters that is the source of the question you want to find a topic for.
    Step 2: Create a multiple-choice question with five options and one correct answer to find a topic based on the sentence in step 1.
    Step 3: In step 3, enter the correct answers one by one (for example, 1, 2, 3, 4, 5).
    """,
              json_schema="""{
        "class": "topic",
        "main" : "{step 1}",
        "view1": "{step 2[0]}",
        "view2": "{step 2[1]}",
        "view3": "{step 2[2]}",
        "view4": "{step 2[3]}",
        "view5": "{step 2[4]}",
        "answer": "{step 3}"
    }
    """)

    result = eval(result)

    result2 = translator.translate(result['main'], src='en', dest='ko')
    result['commentary'] = result2.text 

    return result

def blank():
    result = ''
    prompt = PromptTemplate(
        input_variables=["step", "json_schema"],
        template="""You are a member of the English committee of the Korean Scholastic Ability Test. You should ask blank inference questions.
        I'll give you step-by-step instructions to help you get the right answer.
        Please provide only the answers to step 1, step 2, step 3, and step 4.

        {step}

        Finally, respond with the following JSON schema:

        {json_schema}
        """
    )

    chain = LLMChain(llm=chat, prompt=prompt)

    result = chain.run(step="""Step 1: In this step, you must provide a sentence of at least 800 characters.
    Step 2: Replace only one specific word or grammar in the passage with "___" and combine the sentence from step 1 with the passage from step 2 to display the full sentence.
    Step 3: Create a multiple-choice question to find replacement words based on the passage with five options. One of the options is the replaced answer from step 2, and the other four options are distractions.
    Step 4: Please provide the correct answers (example: 1, 2, 3, 4, 5) obtained through step 3.
    """,
              json_schema="""{
        "class": "blank",
        "content" : "{step 1}",
        "main": "{step 2}",
        "view1": "{step 3[0]}",
        "view2": "{step 3[1]}",
        "view3": "{step 3[2]}",
        "view4": "{step 3[3]}",
        "view5": "{step 3[4]}",
        "answer": "{step 4}"
    }
    """)

    result = eval(result)

    result2 = translator.translate(result['main'], src='en', dest='ko')
    result['commentary'] = result2.text 

    return result


#######여기 밑에는 주석해야함############
# asdasd = 50
# cnt = 0
# while True:
#     cnt += 1
#     # if cnt <= 20:
#     #     dic_title = title()
#     #     print(dic_title)

#     #     # 딕셔너리를 데이터프레임으로 변환
#     #     df = pd.DataFrame.from_dict(dic_title, orient='index').T

#     #     # 데이터프레임을 CSV 파일로 저장
#     #     df.to_csv('./csv/dic_title.csv', mode='a', index=False, encoding='utf-8')
#     # if cnt <= 20:
#     #     dic_blank = blank()
#     #     print(dic_blank)

#     #     df = pd.DataFrame.from_dict(dic_blank, orient='index').T
#     #     df.to_csv('./csv/dic_blank.csv', mode='a', index=False, encoding='utf-8')
#     if cnt <= asdasd:
#         dic_topic = topic()
#         print(dic_topic)

#         df = pd.DataFrame.from_dict(dic_topic, orient='index').T
#         df.to_csv('./csv/dic_topic.csv', mode='a', index=False, encoding='utf-8')

#     if cnt%2==0:
#         time.sleep(60)
#     elif cnt == asdasd+1:
#         break