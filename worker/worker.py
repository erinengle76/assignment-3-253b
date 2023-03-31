import os
from flask import jsonify
from celery import Celery
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

broker_url = os.environ.get("CELERY_BROKER_URL"),
res_backend = os.environ.get("CELERY_RESULT_BACKEND")

celery_app = Celery(name='worker',
                    broker=broker_url,
                    result_backend=res_backend)

@celery_app.task
def sendEmailTask(in_command, to_email, email_subject, email_message):
    try:
        message = Mail(
            from_email=os.environ.get('SENDGRID_FROM_EMAIL'),
            to_emails=to_email,
            subject=email_subject,
            html_content=email_message
        )
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        sg.send(message)
        response = {"data": {"command": in_command, "message": "Email has been sent"}}
        return jsonify(response)
    except Exception as e:
        return jsonify(e)