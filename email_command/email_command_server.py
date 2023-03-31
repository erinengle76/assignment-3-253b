from flask import Flask, request, jsonify
import json
import logging
import os
from flask_sqlalchemy import SQLAlchemy
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from worker import sendEmailTask


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/execute', methods = ['POST'])
def send_message():
    
    if request.headers.get("Content-Type") == 'application/json':
        try:
            raw_data = request.get_json()
            in_command = raw_data["data"]["command"]
            in_message = raw_data["data"]["message"]
            in_message = in_message.strip()
            index_message = in_message.split(' ', 2)
            to_email = index_message[0]
            email_subject = index_message[1]
            email_message = index_message[2]
            if not in_command or not to_email or not email_subject or not email_message:
                response = {"message": "Please provide an email, subject and message to proceed"}
                response_code = 400
            else:
                if in_command == "email":
                    emailAsyncTask = sendEmailTask.delay(in_command, to_email, email_subject, email_message)
                    response = {"data": {"command": in_command, "message": "Your email has been queued"}}
                    response_code = 200
                else:
                    response = {"message": "This server only accepts email commands"}
                    response_code = 400      
        except IndexError:
            response = {"message": "Please provide an email, subject and message to proceed"}
            response_code = 400
        except KeyError:
            response = {"message": "Please provide an email, subject and message to proceed"}
            response_code = 400
    else:
        response = {"message": "Endpoint requires json input"}
        response_code = 400
    
    return json.dumps(response), response_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5052, debug=True)