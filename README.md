## Setup

## Running

`cd web-simple` for all below:

Run server
`python3 manage.py runserver`

Run Redis (for TaskIQ):
`docker-compose up -d`

Run Task IQ
`taskiq worker --log-level=INFO --reload config.taskiq_config:broker config.taskiq_tasks`

Run NGINX:
Build if you haven't already:
`cd web-simple/nginx`
`docker build . -t nginx-dev-proxy`
`./dev_proxy.sh`

Run frontend:
`npm run dev`

`Go to http://localhost` (no port)
