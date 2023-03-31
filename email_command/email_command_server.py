from flask import Flask, request, jsonify
import json
import logging
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

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
                    to_send = Mail(
                        from_email=os.environ.get('SENDGRID_FROM_EMAIL'),
                        to_emails= to_email,
                        subject = email_subject,
                        html_content = email_message
                    )
                    try:
                        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                        sg.send(to_send)
                        response = {"data": {"command": in_command, "message": "Email has been sent"}}
                        response_code = 200
                    except Exception as e:
                        return jsonify(e)
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