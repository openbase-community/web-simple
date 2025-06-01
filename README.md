## Setup

- Create `.env` in `web-simple`. Put `OPENAI_OPENAI_KEY` in there and `GEMINI_API_KEY` or any other keys.
- Make a new `venv` and activate it
- `pip3 install -r ./requirements.txt`
- Then `cd` into `elder-events-api` and run `pip3 install -e .`

## Running

- `cd web-simple` for all below:
- Run server:
  `python3 manage.py runserver`

- Run Redis (for TaskIQ):
  `docker-compose up -d`

- Run NGINX:
  Build if you haven't already:
  `cd web-simple/nginx`
  `docker build . -t nginx-dev-proxy`
  `./dev_proxy.sh`

- Run Task IQ, Django server, and react frontend from VS Code "Build and run" tab
