import os
from dotenv import load_dotenv
load_dotenv()
import openai
openai.api_key = os.environ.get('OPENAI_KEY')
completion = openai.Completion()

logs = open("whatsapp_bot.log", "r")
global_chat_log = logs.read()

def log_append(log):
    with open("whatsapp_bot.log", "a") as myfile:
        myfile.write(log)

def ask_davinci(question, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    chat_log = (chat_log[:1000] + '..') if len(chat_log) > 1000 else chat_log
    prompt = f'{chat_log}Human: {question}\nDavinci:'
    response = completion.create(
        prompt=prompt, engine="davinci", stop=['\Human'], temperature=0.9,
        top_p=1, frequency_penalty=0, presence_penalty=0.6, best_of=1,
        max_tokens=150)
    answer = response.choices[0].text.strip()
    return answer

def append_interaction_to_chat_log(question, answer, chat_log=None, questioner='Human', responder='Davinci'):
    if chat_log is None:
        chat_log = start_chat_log
    log_append(f'{questioner}: {question}\n{responder}: {answer}\n')
    return f'{chat_log}{questioner}: {question}\n{responder}: {answer}\n'

