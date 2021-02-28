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
        start_chat_log = 'Human: Hello, who are you?\nDavinci: I am doing great. How can I help you today?\n'

        splitNumber = from_number.split(':')[1]
        file = f'{splitNumber}.log'
        mode_read = 'r' if os.path.exists(file) else 'w+'
        if os.path.exists(file) == False:
            mode_append = 'a' if os.path.exists(file) else 'w+'
            with open(file, mode_append) as logfile:
                logfile.write(f'{start_chat_log}')
        logs = open(file, mode_read)
        global_chat_log = logs.read()

        # GET QUESTION FROM TWILIO
        answer = ask_davinci(f'{question}', global_chat_log)
        print(from_number)
        print(answer)
        global_chat_log = append_interaction_to_chat_log(question, answer, global_chat_log, 'Human', 'Davinci',splitNumber)
        
        # SEND ANSWER TO TWILIO
        client = Client(TWILIO_AUTH_KEY, TWILIO_AUTH_SECRET)
        message = client.messages.create(
                              body=answer,
                              from_='whatsapp:'+TWILIO_PHONENUMBER,
                              to=from_number
                          )
        
    return 'SENT';

if __name__ == "__main__":
    app.run(host='0.0.0.0')