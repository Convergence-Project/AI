from flask import Flask, jsonify, request
from test import send_blank
from langchain_module import title, topic, blank
from pymongo_db import load_db
from typing_extensions import Annotated
import ast
app = Flask(__name__)
app.config['JSON_AS_ASCII']=False

@app.route('/')
def GG():
    return 'GG!'

@app.route('/blank')
def blank():
    result = load_db('blank')
    result = ast.literal_eval(result)
    return result

@app.route('/shuffle1')
def shuffle1():
    result = load_db('shuffle1')
    result = ast.literal_eval(result)
    return result

@app.route('/shuffle2')
def shuffle2():
    result = load_db('shuffle2')
    result = ast.literal_eval(result)
    return result

@app.route('/title')
def title():
    result = load_db('title')
    result = ast.literal_eval(result)
    return result

@app.route('/topic')
def topic():
    result = load_db('topic')
    result = ast.literal_eval(result)
    return result

# @app.route('/quiz')
# def send_quiz():
#     result = send_blank()
#     return jsonify(result)

# @app.route('/gpt_title')
# def gpt_title():
#     result = title()
#     return jsonify(result)

# @app.route('/gpt_topic')
# def gpt_topic():
#     result = topic()
#     return jsonify(result)

# @app.route('/gpt_blank')
# def gpt_blank():
#     result = blank()
#     return jsonify(result)



# @app.route('/blank', methods=['POST'])
# def db_q_a():
#     text = request.form.get('text')
#     print(text)
#     result = load_db(text)
#     return jsonify(result)