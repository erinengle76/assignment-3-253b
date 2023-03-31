# complete imports
from flask import Flask, request, Response, jsonify
from urllib.parse import urljoin
import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@db:5432/chatbot"
db = SQLAlchemy(app)

class Commands(db.Model):
    command = db.Column(db.String(20), primary_key=True)
    server_url = db.Column(db.String(200))

    def to_dict(self):
        return {
            'command': self.command,
            'server_url': self.server_url
        }
    
# Helper function to return data in json format    
def returnMessage(command,message):
    return jsonify({
        "data": {"command": command, "message": message}
    })

# '/message' route - accepts POST call with message and command from terminal chatbot in json format
@app.route("/message", methods = ["POST"])
def handleInput():
    try:
        requestJSON = request.get_json()
        requestMessage = requestJSON["data"]["message"]
        requestMessage = requestMessage.strip()
        if len(requestMessage) != 0:
            if requestMessage[0] == "/":
                splitCommand = requestMessage.split(' ', 1)
                inputCommand = splitCommand[0][1:]
                try:
                    message = splitCommand[1]
                    url = Commands.query.filter_by(command=inputCommand).first()
                    if url:
                        url = url.to_dict()
                        found_url = url["server_url"]
                        full_url = urljoin(found_url, "/execute")
                        raw_data = {}
                        raw_data["data"] = {"command": inputCommand, "message": message}
                        try:
                            r = requests.post(full_url, json=raw_data)
                            r.raise_for_status()
                            serverData = r.json()
                            return serverData, 200
                        except requests.exceptions.ConnectionError:
                            return returnMessage("error", "connection error")
                        except requests.exceptions.HTTPError:
                            return returnMessage("error", "http error")
                    # if separate server does not exist to handle command
                    else:
                        return returnMessage(inputCommand, message), 200
                # if message is blank
                except IndexError:
                    return returnMessage(inputCommand,"Message cannot be blank"), 404
    #       if message does not start with "/"
            else:
                command = None
                message = requestMessage
                return returnMessage(command,message), 201
    #   response if message is empty
        else:
            return returnMessage(None, "Message cannot be empty"), 404
    # # if improper input is sent by the client
    except KeyError:
        return returnMessage(None,"Request is missing a valid message or command"), 404

# 'register' route - accepts POST call with json 
@app.route("/register", methods = ["POST"])
def registerInput():
    try:
        requestJSON = request.get_json()
        command = requestJSON["data"]["command"]
        associatedServer = requestJSON["data"]["server_url"]
        # ensure command is not empty
        if len(command) != 0:
            # ensure route is not empty
            if len(associatedServer) != 0:
                new_command = Commands(command=command, server_url=associatedServer)
                db.session.add(new_command)
                try:
                    db.session.commit()
                    return returnMessage(command, "saved"), 201
                except IntegrityError:
                    db.session.rollback()
                    existing_address = Commands.query.filter_by(command=command).first()
                    originalServer = existing_address.server_url
                    existing_address.command = command
                    existing_address.server_url = associatedServer
                    db.session.commit()
                    return returnMessage(command, f"The command sent already exists in the dictionary. The associated server address has been updated from {originalServer} to {associatedServer}"), 200
            else:
                return "Associated server cannot be empty", 404
        else:
            return "Command cannot be empty", 404
    except KeyError:
        return "The input provided was missing valid input for the data, command, or server_url fields. Please update your input and try again.", 404


