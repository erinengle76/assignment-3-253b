# complete imports
from flask import Flask, request, Response, jsonify
import json

app = Flask(__name__)

# single route '/execute' accepting POST method
@app.route("/execute", methods = ["POST"])
def handleShrug():
    # pull data from request body
    try:
        requestJSON = request.get_json()
        requestCommand = requestJSON["data"]["command"]
        requestMessage = requestJSON["data"]["message"]
        # strip whitespace
        requestMessage = requestMessage.strip()
        if requestCommand == "shrug":
            # if message isn't empty, add shrug to message and return as JSON
            if len(requestMessage) != 0:
                requestMessage = requestMessage + "¯\_(ツ)_/¯"
                return jsonify({
                    "data": {"command": "shrug", "message": requestMessage}
                })
            # if message is empty, return 404 error
            else:
                return "Request message cannot be empty", 404
        else:
            return "This server can only handle shrug requests", 400
    except KeyError:
        return "The data provided is missing data, command, or message inputs.", 404