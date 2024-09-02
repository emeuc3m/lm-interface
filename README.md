
# LM-INTERFACE

This project builds a web application to interact with a small language model to translate, spell check and generate storys with the user's input.



## Architecture
It uses a microservice architecture with 3 production-ready separataded docker containers:
- web_app (_frontend_): builds a React application on a Nginx server that acts as a reverse proxy, load-balancer and rate-limiter. Run on port 8080.
- api_run (_backend_): builds a Flask application run with Gunicorn WSGI server that serves the front-end on port 8090.
- lm_api_run (_model-microservice_): builds a Flask application run with Gunicorn WSGI that runs a small llama language model on port 3000.
## Demo Quickstart

To run the application, you'll need:
- docker: recommended version 2.17.3 or higher, older versions might not work.
- docker compose: version 24.0.7 or higher, older versions might not work.
- git lfs.
- Linux environment: also works on window's WSL.
- Internet connection.

To run the tool, execute the following command inside the root folder of the project:
`sh run.sh`

Or copy the docker compose command and run it manually in the same folder.

If you are having trouble running the script, try to replace `docker compose` for `docker-compose` (this dependes on your docker / docker compose version)

The application runs on localhost:8080 .

The username and password for the demo are:
- username: default_username
- password: default_password

That's it!
## API Reference

The documentation of both the backend and model-microservice endpoints can be accessed via swagger on:
- backend: localhost:8090/api/docs/
- model-microservice: localhost:5000/api/docs/


## Run for development
I recommend to create virtual environments on each directory with `python3 -m venv .venv`
and installing the necessary requirements with `pip install -r requirements.txt` for the Flask services.

For the frontend, I recommend to have npm installed and use `npm i` inside the frontend directory. 

To run the development servers you can:
- backend: `cd backend && python3 run.py`
- lm_service: `cd lm_service && python3 run.py`
- frontend: `cd frontend && npm start`

If running backend on development server (or simply not in the docker container), please change the value of API_URL in backend.src.constants.py from `http://lm_api_run:5000/` to `http://localhost:5000/`