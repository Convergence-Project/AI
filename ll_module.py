from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain import HuggingFacePipeline
from langchain import PromptTemplate,  LLMChain


from transformers import AutoModel
import torch
import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM

import json
import textwrap

from transformers import pipeline


tokenizer = AutoTokenizer.from_pretrained("NousResearch/Llama-2-7b-chat-hf")
model = AutoModelForCausalLM.from_pretrained("NousResearch/Llama-2-7b-chat-hf",
                                             device_map='auto',
                                             torch_dtype=torch.float16,
                                             load_in_4bit=True,
                                             bnb_4bit_quant_type="nf4",
                                             bnb_4bit_compute_dtype=torch.float16)



pipe = pipeline("text-generation",
                model=model,
                tokenizer= tokenizer,
                torch_dtype=torch.float16,
                device_map="auto",
                max_new_tokens = 512,
                do_sample=True,
                top_k=30,
                num_return_sequences=1,
                eos_token_id=tokenizer.eos_token_id
                )



B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<>\n", "\n<>\n\n"
DEFAULT_SYSTEM_PROMPT = """\
You are a member of the English committee of the Korean Scholastic Ability Test.
Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.
If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.Just say you don't know and you are sorry!"""



def get_prompt(instruction, new_system_prompt=DEFAULT_SYSTEM_PROMPT, citation=None):
    SYSTEM_PROMPT = B_SYS + new_system_prompt + E_SYS
    prompt_template =  B_INST + SYSTEM_PROMPT + instruction + E_INST

    if citation:
        prompt_template += f"\n\nCitation: {citation}"  # Insert citation here

    return prompt_template

def cut_off_text(text, prompt):
    cutoff_phrase = prompt
    index = text.find(cutoff_phrase)
    if index != -1:
        return text[:index]
    else:
        return text

def remove_substring(string, substring):
    return string.replace(substring, "")

def generate(text, citation=None):
    prompt = get_prompt(text, citation=citation)
    inputs = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(**inputs,
                                 max_length=512,
                                 eos_token_id=tokenizer.eos_token_id,
                                 pad_token_id=tokenizer.eos_token_id,
                                 )
        final_outputs = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
        final_outputs = cut_off_text(final_outputs, '')
        final_outputs = remove_substring(final_outputs, prompt)

    return final_outputs

def parse_text(text):
    wrapped_text = textwrap.fill(text, width=100)
    print(wrapped_text + '\n\n')


def talk_2_llama():
    # text = "My life sucks, what do you suggest? Please don't tell me to medidate"
    llm = HuggingFacePipeline(pipeline = pipe, model_kwargs = {'temperature':0.7,'max_length': 256, 'top_k' :50})

    system_prompt = "You are a member of the English committee of the Korean Scholastic Ability Test."
    instruction = "You should ask blank inference questions. I'll give you step-by-step instructions to help you get the right answer. Please provide only the answers to step 1, step 2, step 3, and step 4.:\n\n {text}"
    template = get_prompt(instruction, system_prompt)
    # print(template)

    prompt = PromptTemplate(template=template, input_variables=["text"])

    llm_chain = LLMChain(prompt=prompt, llm=llm, verbose = False)

    

    response = llm_chain.run(step="""Step 1: In this step, you must provide a sentence of at least 800 characters.
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
    response = eval(response)
    return response