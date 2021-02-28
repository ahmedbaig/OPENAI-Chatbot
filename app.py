import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, session, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from chat import ask_davinci, append_interaction_to_chat_log
TWILIO_AUTH_KEY = os.environ.get('TWILIO_AUTH_KEY')
TWILIO_AUTH_SECRET = os.environ.get('TWILIO_AUTH_SECRET')
TWILIO_PHONENUMBER = os.environ.get('TWILIO_PHONENUMBER')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'

logs = open("whatsapp_bot.log", "r")
global_chat_log = logs.read()

@app.route('/', methods=['GET'])
def index():
    return 'Silence is golden'
    
@app.route('/health', methods=['GET'])
def health():
    # return jsonify(TWILIO_AUTH_KEY=TWILIO_AUTH_KEY,TWILIO_AUTH_SECRET=TWILIO_AUTH_SECRET,TWILIO_PHONENUMBER=TWILIO_PHONENUMBER)
    return jsonify(success='ok')

@app.route('/bot', methods=['POST'])
def bot():
    global global_chat_log
    # GET QUESTION FROM TWILIO
    answer = ask_davinci(f'{question}?', global_chat_log)
    print(f'Davinci: {answer}')
    global_chat_log = append_interaction_to_chat_log(question, answer, global_chat_log, 'Human', 'Davinci')
    # SEND ANSWER TO TWILIO
    
    # message = client.messages.create(
    #                           body=answer,
    #                           from_='whatsapp:+14155238886',
    #                           to='whatsapp:+15005550006'
    #                       )
    # print(message.sid)