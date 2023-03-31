FROM python:3.9-alpine

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
EXPOSE 5051

ENTRYPOINT ["python3"]
CMD ["-m", "flask", "--app", "shrug_command_server.py", "run", "--host=0.0.0.0", "--port=5051"]
