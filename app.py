import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, session, jsonify
from twilio.rest import Client
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
    question = request.values['Body']
    from_number = request.values['From']
    if question == 'Hi' or question == 'HI' or question == 'hi':
        client = Client(TWILIO_AUTH_KEY, TWILIO_AUTH_SECRET)
        message = client.messages.create(
                              body="Hi, my name is Davinci and I am an advanced AI",
                              from_='whatsapp:'+TWILIO_PHONENUMBER,
                              to=from_number
                          )
        print(message.sid)
    else: 
        # use the incoming message to generate the response here

        global global_chat_log
        # GET QUESTION FROM TWILIO
        answer = ask_davinci(f'{question}', global_chat_log)
        
        app.logger.info(f'AI: {answer}')
        global_chat_log = append_interaction_to_chat_log(question, answer, global_chat_log, 'Human', 'Davinci')
        # SEND ANSWER TO TWILIO
        
        client = Client(TWILIO_AUTH_KEY, TWILIO_AUTH_SECRET)
        message = client.messages.create(
                              body=answer,
                              from_='whatsapp:'+TWILIO_PHONENUMBER,
                              to=from_number
                          )
        print(message.sid)
        
    return 'SENT';

if __name__ == "__main__":
    app.run(host='0.0.0.0')