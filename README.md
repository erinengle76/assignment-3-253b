# Assignment-3 253B
## Main Branch (incl. Extra Credit Async Task Queues)

### Author: Erin Jones
### Course: INFO 253B Spring 2023
### Submission Date: 3/30/2023 (using late-submit pass #2)

**Notes:
- docker-compose file must be updated to include a send from email and sendgrid api key under both the worker and email_command services
- a plain version not including the extra credit is included in a secondary branch

**Description:
- **Chatbot parser:** Designed to accept input from the terminal-chatbot application in json format and parse; if a server exists in the 'registration' database to handle a given command the parser sends the request to the given server; contains a /register endpoint for registering new command servers in a postgres image via POST call; contains a /message endpoint that accepts POST input from terminal-chatbot; runs on port 5050 (local host)
- **Shrug command:** Designed to handle shrug commands from the terminal-chatbot application; contains an /execute endpoint that adds the shrug emoji to the message and hands the data back to the chatbot parser; runs on port 5051 i.e. http://shrug_command:5051
- **Email command:** Designed to accept input from chatbot parser; contains an /execute endpoint for parsing email commands that sends commands to the worker, adding the command to the asynchronous queue supported by redis; runs on port 5052 i.e. http://email_command:5052 
- **worker:** Runs a celery application that functions in tandem with the email command server to listen and accept jobs and execute via sending an email via sendgrid
